"""
Helper functions used by the ECMP26 SIRF workshop notebooks.

Visualisation
    display_arr                      show a 2D slice of one or more 3D arrays
Projection data
    acq_poisson_noise                add Poisson counting noise to projections
    scatter_correction               DEW / TEW scatter estimation and correction
    smooth_acquisition_data          Gaussian smoothing within each projection
Quantitative analysis
    recovery_coefficients            NEMA sphere recovery coefficients, one image
    calculate_recovery_coefficients  ... for a series of OSEM subiterations
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sirf.STIR as spect
from scipy.ndimage import gaussian_filter


################################################################################
#   VISUALISATION
################################################################################

def display_arr(
    arr_3d,
    idx: tuple,
    *,
    cmap="inferno",
    vmin=None,
    vmax=None,
    titles=None,
):
    """
    Display a 2D slice of one or more 3D arrays side by side.

    Parameters
    ----------
    arr_3d : np.ndarray or list of np.ndarray
        3D volume(s) to display. A list is shown as a row of panels.
    idx : tuple
        NumPy index selecting a 2D plane from each volume, e.g.
        ``(56, slice(None), slice(None))`` for transverse slice 56.
    cmap, vmin, vmax : single value or list, optional
        A single value is used for every panel; a list gives one value per
        panel. A limit of ``None`` is taken from that panel's own min/max.
    titles : str or list of str, optional
        Panel title(s).

    Returns
    -------
    fig, axes
        ``axes`` is a single Axes when one volume is given.
    """
    volumes = [arr_3d] if isinstance(arr_3d, np.ndarray) else list(arr_3d)
    n = len(volumes)
    if n == 0:
        raise ValueError("Nothing to display.")

    def _per_panel(param, name):
        if isinstance(param, Sequence) and not isinstance(param, str):
            if len(param) != n:
                raise ValueError(
                    f"`{name}` must be a single value or a list of length {n}."
                )
            return list(param)
        return [param] * n

    panels = zip(
        volumes,
        _per_panel(cmap, "cmap"),
        _per_panel(vmin, "vmin"),
        _per_panel(vmax, "vmax"),
        _per_panel(titles, "titles"),
    )

    fig, axes = plt.subplots(1, n, squeeze=False, figsize=(6 * n, 5))
    axes = axes[0]

    for ax, (vol, cmap_i, vmin_i, vmax_i, title) in zip(axes, panels):
        img = np.squeeze(np.asarray(vol)[idx])
        if img.ndim != 2:
            raise ValueError(
                f"idx={idx} selects shape {img.shape} from a volume of shape "
                f"{np.shape(vol)}; it must select a 2D plane."
            )

        im = ax.imshow(
            img,
            cmap=cmap_i,
            vmin=np.min(img) if vmin_i is None else vmin_i,
            vmax=np.max(img) if vmax_i is None else vmax_i,
        )
        ax.set_axis_off()
        if title is not None:
            ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.tight_layout()
    return fig, (axes[0] if n == 1 else axes)


################################################################################
#   INTERFILE HEADERS
################################################################################

def _read_header_value(hdr_file: str | Path, tag: str) -> str | None:
    """Return the value of `tag` in an Interfile header, or None if absent."""
    value = None
    for line in Path(hdr_file).read_text().splitlines():
        if tag in line and "= " in line:
            value = line.split("= ", 1)[1].strip()
    return value


def _insert_header_line(hdr_file: str | Path, key: str, value: str, before_tag: str):
    """Insert ``key := value`` into an Interfile header before `before_tag`."""
    hdr_file = Path(hdr_file)
    lines = []
    for line in hdr_file.read_text().splitlines(keepends=True):
        if before_tag in line:
            lines.append(f"{key} := {value}\n")
        lines.append(line)
    hdr_file.write_text("".join(lines))


################################################################################
#   PROJECTION DATA
################################################################################

def acq_poisson_noise(
    hs_file: str | Path,
    save_path: str | Path,
    seed: int | None = None,
) -> spect.AcquisitionData:
    """
    Apply Poisson noise to SPECT acquisition data stored as STIR Interfile.

    Each projection bin is treated as the expected value of an independent
    Poisson distribution, and one noisy realisation is written to `save_path`.

    The original ``.hs`` header is kept, with these fields updated to point
    at the new data file:

    - ``!name of data file`` -> output ``.s`` file name
    - ``;patient name``      -> output ``.s`` file name
    - ``;!study ID``         -> output file name without extension

    Parameters
    ----------
    hs_file : str or Path
        Input STIR Interfile header (``.hs``).
    save_path : str or Path
        Output header (``.hs``). The binary data are written alongside it
        with an ``.s`` extension.
    seed : int or None, optional
        Seed for the random number generator, for a reproducible realisation.

    Returns
    -------
    spect.AcquisitionData
        The noisy acquisition data.
    """
    hs_file = Path(hs_file)
    save_path = Path(save_path)

    if not hs_file.exists():
        raise FileNotFoundError(f"Input header not found: {hs_file}")
    if save_path.suffix.lower() != ".hs":
        raise ValueError("save_path must have a '.hs' extension.")

    save_path.parent.mkdir(parents=True, exist_ok=True)

    acq_data = spect.AcquisitionData(str(hs_file))
    acq_array = acq_data.as_array()

    if np.any(acq_array < 0):
        raise ValueError(
            "Acquisition data contain negative values and cannot be used "
            "as Poisson expectations."
        )

    rng = np.random.default_rng(seed)
    noisy_acq = acq_data.clone()
    noisy_acq.fill(rng.poisson(acq_array))

    # SIRF/STIR writes the .s data file; the header is then replaced by the
    # original one so that the SIMIND-derived keys are preserved.
    noisy_acq.write(str(save_path))

    data_filename = save_path.with_suffix(".s").name
    study_id = save_path.stem

    header = hs_file.read_text()
    for key, value in (
        (r"!name of data file", data_filename),
        (r";patient name", data_filename),
        (r";!study ID", study_id),
    ):
        header = re.sub(
            rf"(?im)^(\s*{re.escape(key)}\s*:=\s*).*$",
            rf"\g<1>{value}",
            header,
        )
    save_path.write_text(header)

    return noisy_acq


def scatter_correction(
    PP_hdr: str | Path,
    SC1_hdr: str | Path,
    SC2_hdr: str | Path | None = None,
    sigma: float = 2.0,
    save_filepath: str | Path | None = None,
) -> tuple[spect.AcquisitionData, spect.AcquisitionData]:
    """
    Scatter correction with the Dual Energy Window (DEW) method or, if
    `SC2_hdr` is given, the Triple Energy Window (TEW) method.

    The scatter windows are smoothed, scaled by window width to estimate the
    scatter in the photopeak window, and subtracted. Negative values are
    clipped to zero.

    Parameters
    ----------
    PP_hdr : str or Path
        Header of the photopeak window.
    SC1_hdr : str or Path
        Header of the scatter window (DEW) or first scatter window (TEW).
    SC2_hdr : str or Path, optional
        Header of the second scatter window (TEW). If None, DEW is used.
    sigma : float
        Gaussian smoothing applied to the scatter window(s), in projection bins.
    save_filepath : str or Path, optional
        If given, the corrected data are written here (``.hs``) and the scatter
        estimate alongside it as ``<name>_scatter.hs``.

    Returns
    -------
    corrected : spect.AcquisitionData
        Scatter-corrected projections, negative values clipped to zero.
    scatter : spect.AcquisitionData
        Estimated scatter contribution in the photopeak window.
    """
    if sigma is None or not np.isfinite(float(sigma)) or float(sigma) < 0:
        raise ValueError(f"sigma must be a finite non-negative float. Got {sigma}.")

    PP_hdr = str(PP_hdr)
    SC1_hdr = str(SC1_hdr)
    tew = SC2_hdr is not None

    def _window_width(hdr_file: str, label: str) -> float:
        lo = _read_header_value(hdr_file, "energy window lower level[1]")
        hi = _read_header_value(hdr_file, "energy window upper level[1]")
        if lo is None or hi is None:
            raise ValueError(f"Energy window limits not found in {label} header: {hdr_file}")
        width = float(hi) - float(lo)
        if width <= 0:
            raise ValueError(f"{label} window width must be > 0. Got lo={lo}, hi={hi}.")
        return width

    def _smoothed(hdr_file: str) -> np.ndarray:
        arr = spect.AcquisitionData(hdr_file).as_array()
        return gaussian_filter(arr, sigma=(0.0, sigma, 0.0, sigma), mode="nearest")

    # ---- load data ----
    acq_data_PP = spect.AcquisitionData(PP_hdr)
    SC1_arr = _smoothed(SC1_hdr)
    if tew:
        SC2_hdr = str(SC2_hdr)
        SC2_arr = _smoothed(SC2_hdr)
        print("Second Scatter Window present. Performing TEW...")

    # ---- window widths ----
    width_PP = _window_width(PP_hdr, "Photopeak")
    width_SC1 = _window_width(SC1_hdr, "Scatter window 1")
    print(f"Photopeak window width: {round(width_PP, 2)}")

    # ---- estimate scatter under the photopeak ----
    if tew:
        width_SC2 = _window_width(SC2_hdr, "Scatter window 2")
        print(f"Scatter window 1 width: {round(width_SC1, 2)}")
        print(f"Scatter window 2 width: {round(width_SC2, 2)}")
        scatter_arr = (SC1_arr / width_SC1 + SC2_arr / width_SC2) * width_PP / 2.0
    else:
        print(f"Scatter window width: {round(width_SC1, 2)}")
        print(f"Scatter fraction: {round((width_PP / width_SC1) / 2.0, 2)}")
        scatter_arr = (SC1_arr / width_SC1) * width_PP / 2.0

    # ---- subtract and clip ----
    corrected = acq_data_PP.clone()
    corrected.fill(np.clip(acq_data_PP.as_array() - scatter_arr, 0, None))

    scatter = acq_data_PP.clone()
    scatter.fill(scatter_arr)

    if save_filepath is not None:
        save_filepath = Path(save_filepath).with_suffix(".hs")
        scatter_filepath = save_filepath.with_name(f"{save_filepath.stem}_scatter.hs")

        corrected.write(str(save_filepath))
        scatter.write(str(scatter_filepath))

        # SIMIND-derived headers use one of two spellings for this key.
        image_duration = (
            _read_header_value(PP_hdr, "!image duration (sec)[1]")
            or _read_header_value(PP_hdr, "image duration (sec) [1]")
        )
        if image_duration is None:
            raise ValueError(f"Image duration not found in photopeak header: {PP_hdr}")

        _insert_header_line(save_filepath, "number of time frames", "1", "!extent of rotation")
        _insert_header_line(
            save_filepath, "!image duration (sec)[1]", str(float(image_duration)), "!extent of rotation"
        )

        print("Scatter correction completed successfully!")

    return corrected, scatter


def smooth_acquisition_data(
    acq_data: spect.AcquisitionData,
    sigma: float = 1.0,
) -> spect.AcquisitionData:
    """
    Apply Gaussian smoothing within each projection (not across views).

    Parameters
    ----------
    acq_data : spect.AcquisitionData
        Input projection data.
    sigma : float
        Gaussian standard deviation in projection bins.

    Returns
    -------
    spect.AcquisitionData
        Smoothed projection data.
    """
    # Array axes: (TOF/energy, axial, views, tangential)
    smoothed = acq_data.clone()
    smoothed.fill(gaussian_filter(acq_data.as_array(), sigma=(0, sigma, 0, sigma)))
    return smoothed


################################################################################
#   QUANTITATIVE ANALYSIS
################################################################################

def recovery_coefficients(
    source,
    image,
    masks_dict,
    icf=1.0,
    sphere_numbers=range(1, 7),
):
    """
    Recovery coefficient of each NEMA sphere in one image.

    RC = (activity in the sphere mask in `image` / icf) / (true activity in the mask)

    Parameters
    ----------
    source : np.ndarray
        Reference activity distribution in MBq/voxel.
    image : np.ndarray
        Reconstructed image. Use the default ``icf=1`` if it is already
        calibrated to activity.
    masks_dict : dict
        Sphere masks named 'sphere_1', 'sphere_2', etc.
    icf : float, optional
        Image calibration factor converting reconstructed values to activity.
    sphere_numbers : iterable, optional
        Sphere numbers to include. Default is spheres 1 to 6.

    Returns
    -------
    np.ndarray
        One recovery coefficient per sphere.
    """
    rc = []
    for sp_n in sphere_numbers:
        mask = masks_dict[f"sphere_{sp_n}"]
        reconstructed_activity = np.sum(image * mask) / icf
        true_activity = np.sum(source * mask)
        rc.append(reconstructed_activity / true_activity)
    return np.asarray(rc)


def calculate_recovery_coefficients(
    source,
    recon_dict,
    masks_dict,
    subiterations,
    icf,
    sphere_numbers=range(1, 7),
    verbose=False,
):
    """
    Calculate recovery coefficients for each sphere and reconstruction
    using a predefined image calibration factor.

    Parameters
    ----------
    source : np.ndarray
        Reference activity distribution in MBq/voxel.
    recon_dict : dict
        Reconstructed images, keyed by subiteration (as a string).
    masks_dict : dict
        Sphere masks named 'sphere_1', 'sphere_2', etc.
    subiterations : array-like
        OSEM subiterations to evaluate.
    icf : float
        Image calibration factor converting reconstructed values to activity.
    sphere_numbers : iterable, optional
        Sphere numbers to include. Default is spheres 1 to 6.
    verbose : bool, optional
        Print the calculated recovery coefficients.

    Returns
    -------
    np.ndarray
        Recovery coefficients, shape (number of subiterations, number of spheres).
    """
    if verbose:
        print(f"Image calibration factor: {icf:.4f}\n")

    rc_data = []
    for subit in subiterations:
        rc = recovery_coefficients(source, recon_dict[str(subit)], masks_dict, icf, sphere_numbers)
        rc_data.append(rc)

        if verbose:
            print(f"SUBITERATION {subit}")
            for sp_n, rc_n in zip(sphere_numbers, rc):
                print(f"Sphere {sp_n}: {rc_n:.4f}")
            print()

    return np.asarray(rc_data)
