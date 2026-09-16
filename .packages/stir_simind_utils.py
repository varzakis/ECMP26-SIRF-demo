from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import os
import shutil
import sirf.STIR as spect
import numpy as np
import numexpr as ne
ne.set_num_threads(16) # use only 16 threads
import sys
import math as m
from pathlib import Path
from scipy.ndimage import gaussian_filter
from dataclasses import dataclass
from tempfile import TemporaryDirectory
import warnings
import pydicom
import re
from collections.abc import Sequence


def display(images, slc=0, plane=0, cmap='inferno', _min=0, _max=0):
    '''
    Display images/acquisition data for a specific slice/projection and plane.

    Parameters:
    images (list of ImageData or AcquisitionData or ndarray): The input image data.
    row (int, optional): The row to be displayed (default is 0).
    cmap (str, optional): The colormap for the displayed images (default is 'inferno').
    _min (float, optional): The minimum value to be displayed (default is 0 which displays the image's own minimum).
    _max (float, optional): The maximum value to be displayed (default is 0 which displays the image's own maximum).
        
    Returns: --
    '''
    try:
        n_plots = len(images)
    except TypeError:
        n_plots = 1

    if n_plots == 1:
        im_arr = image_to_image2d(images, slc, plane)
        if (_min, _max) == (0, 0):
            _min, _max = np.amin(im_arr), np.amax(im_arr)
    else:
        im_arr = [image_to_image2d(im, slc, plane) for im in images]
        if (_min, _max) == (0, 0):
            combined_data = np.array(im_arr)
            _min, _max = np.amin(combined_data), np.amax(combined_data)
    
    fig, axes = plt.subplots(1, n_plots)
    fig.set_figheight(6)
    fig.set_figwidth(18)

    fig.suptitle(f'Display slice/projection [{slc}]', color='black', weight='bold', fontsize=20)
    if n_plots == 1:
        ax_im = axes.imshow(im_arr, cmap=cmap, vmin=_min, vmax=_max)
        fig.colorbar(ax_im)
    else:
        for i, ax in enumerate(axes.flat):
            ax_im = ax.imshow(im_arr[i], cmap=cmap, vmin=_min, vmax=_max)
            fig.colorbar(ax_im)


def image_to_image2d(img_acq, slc_or_proj:int=0, plane:int=0) -> np.array:
    '''
    Generate a 2D array from an image/acquisition data given a slice/projection and a plane. 

    Parameters:
    img_acq (ImageData or AcquisitionData or ndarray): The input image or projections.
    slc_or_proj (int, optional): The slice or projection to be displayed (default is 0).
    plane (int, optional): The plane to be displayed (0: transverse, 1: coronal, 2: sagittal, default is 0).
    
    Returns (2D ndarray): Array to be displayed.
    '''
    if type(img_acq) is np.ndarray:
        img_acq_arr = img_acq.copy()
    else:        
        img_acq_arr = img_acq.as_array()        

    image_data = False
    if img_acq_arr.ndim == 3:
        image_data = True

    if image_data:
        orientation = {
            0   :   'transverse',
            1   :   'coronal',
            2   :   'sagittal'
        }

        if plane not in orientation:
            plane = 0
            print('Display plane does not exist. Defaulting to transverse!')

        if slc_or_proj > img_acq_arr.shape[plane]:
            print(f'Total number of {orientation[plane]} slices in image is: {img_acq_arr.shape[plane]}')
            slc_or_proj = img_acq_arr.shape[plane]      

        if plane == 0:
            image2D = img_acq_arr[slc_or_proj-1,:,:]
        elif plane == 1:
            image2D = img_acq_arr[:,slc_or_proj-1,:]
        elif plane == 2:
            image2D = img_acq_arr[:,:,slc_or_proj-1]

    else:
        if plane != 0:
            print('This is acquisition data. There are no planes to display!')

        if slc_or_proj > img_acq_arr.shape[2]:
            print(f'Total projections of dataset is: {img_acq_arr.shape[2]}')
            slc_or_proj = img_acq_arr.shape[2]

        image2D = img_acq_arr[0,:,slc_or_proj-1,:]

    return image2D


def extract_header_info(hdr, tag_str:str) -> str:
    '''
    Extracts the information from header of image/acquisition data for a given tag.

    Parameters:
    hdr (ImageData or AcquisitionData or str): The ImageData, AcquisitionData or filepath of the header file.
    tag_str (str): The tag for which the value is to be extracted.
    
    Returns (str): The value of the tag.
    ''' 
    tag_value = None
    
    if type(hdr) is str:
        lines = open(hdr, 'rt')
        for line in lines:
            if line.find(tag_str) != -1:
                tag_value = line.split('= ')[1]
        lines.close()

    else:
        header = hdr.get_info()
        lines = header.split('\n')
        for line in lines:
            if line.find(tag_str) != -1:
                if len(line.split(':= ')) == 2:
                    tag_value = line.split(':= ')[1]
                elif len(line.split(': ')) == 2:
                    tag_value = line.split(': ')[1]
    
    if not tag_value:
        print(f'Tag {tag_str} not found!')
        tag_value = 'no_value'
    
    return tag_value


def replace_header_info(hdr_file:str, tag_str:str, replace_value:str):
    '''
    Changes the value for a certain tag in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str (str): The tag for which the value is to be extracted.
    replace_value (str): The new value for the given tag.
    
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str) != -1:
            line = i

    # replace the value if the line number is found above
    if line:
        header_file = open(hdr_file, 'wt')
        lines[line] = tag_str + ' := ' + replace_value + '\n'
        header_file.writelines(lines)
    else:
        print('Tag not found!')

    header_file.close()


def replace_header_tag(hdr_file:str, tag_str_old:str, tag_str_new:str):
    '''
    Replaces a certain tag name with another in a header file, leaving the value intact.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str_old (str): The old tag.
    tag_str_new (str): The new tag.
    
    Returns: --
    '''
    old_str_value = extract_header_info(hdr_file,tag_str_old)

    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str_old) != -1:
            line = i

    if line:
        header_file = open(hdr_file, 'wt') 
        lines[line] = tag_str_new + ' := ' + old_str_value# + '\n'
        header_file.writelines(lines)

    header_file.close()


def remove_header_info(hdr_file:str, tag_str:str):
    '''
    Removes a certain tag and value in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_str (str): The tag to be removed.
        
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    for i in range(len(lines)):
        if lines[i].find(tag_str) != -1:
            line = i

    if line:
        header_file = open(hdr_file, 'wt')  
        lines[line] = '\n'
        header_file.writelines(lines)
    else:
        print('Tag not found!')

    header_file.close()


def add_header_info(hdr_file:str, tag_name:str, tag_value:str, place_before_tag:str='!END OF INTERFILE :='):
    '''
    Adds a certain tag and its value in a header file.

    Parameters:
    hdr_file (str): The header filepath.
    tag_name (str): The tag name to be added.
    tag_value (str): The tag value to be added
        
    Returns: --
    ''' 
    # open the file and read all lines in a list
    header_file = open(hdr_file, 'rt')
    lines = header_file.readlines()
    
    # look for field_str in lines and identify the line number
    line = None
    lines_new = []
    for i in range(len(lines)):
        if lines[i].find(place_before_tag) != -1:
            lines_new.append(f'{tag_name} := {tag_value}\n')
        lines_new.append(lines[i])

    header_file = open(hdr_file, 'wt')
    header_file.writelines(lines_new)
    header_file.close()


def convert_simind_to_stir(simind_header_fp:str,contour_file=None):
    if not simind_header_fp.endswith('.h00'):
        print("This doesn't seem to be a simind header file. It should end with .h00!")
        sys.exit()

    stir_header_fp = f'{simind_header_fp[:-4]}.hs'
    shutil.copyfile(simind_header_fp,stir_header_fp)
    
    replace_header_tag(stir_header_fp,'program author',';program author')
    replace_header_tag(stir_header_fp,'program version',';program version')
    replace_header_tag(stir_header_fp,'original institution',';original institution')
    replace_header_tag(stir_header_fp,'contact person',';contact person')
    replace_header_tag(stir_header_fp,'patient name',';patient name')
    replace_header_tag(stir_header_fp,'!study ID',';!study ID')
    replace_header_tag(stir_header_fp,'data description',';data description')
    replace_header_tag(stir_header_fp,'exam type',';exam type')
    replace_header_tag(stir_header_fp,'!patient ID',';!patient ID')
    replace_header_tag(stir_header_fp,'patient position',';patient position')
    replace_header_tag(stir_header_fp,'patient orientation',';patient orientation')
    replace_header_tag(stir_header_fp,'patient orientation',';patient orientation')
    replace_header_tag(stir_header_fp,';energy window lower level','energy window lower level[1]')
    replace_header_tag(stir_header_fp,';energy window upper level','energy window upper level[1]')
    replace_header_tag(stir_header_fp,'!total number of images',';!total number of images')
    replace_header_info(stir_header_fp,'!number format', 'float')
    replace_header_tag(stir_header_fp,'number of detector heads',';number of detector heads')
    replace_header_tag(stir_header_fp,'!number of images/energy window',';!number of images/energy window')
    replace_header_tag(stir_header_fp,'!time per projection (sec)',';!time per projection (sec)')
    add_header_info(stir_header_fp,'number of time frames','1','image duration (sec)')
    replace_header_tag(stir_header_fp,'image duration (sec)','image duration (sec) [1]')
    if extract_header_info(simind_header_fp,'orbit') == 'noncircular\n':
        replace_header_info(stir_header_fp,'orbit','non-circular')
        countour_f = open(contour_file,'rt')
        radii_from_file = countour_f.readlines()
        radial_position = []
        for angle in radii_from_file:
            radial_position.append(float(angle.split('      ')[1].split('  ')[0])*10)
        radial_position_string = ','.join(map(str, radial_position))
        radial_position_string = '{' + radial_position_string + '}'
        countour_f.close()    
    add_header_info(stir_header_fp,'Radii',radial_position_string,'acquisition mode')
    replace_header_tag(stir_header_fp,'acquisition mode',';acquisition mode')
    replace_header_info(stir_header_fp,'start angle','180')


def scatter_correction(
    PP_hdr: str,
    SC1_hdr: str,
    SC2_hdr: Optional[str] = None,
    sigma: float = 2.0,
    save_filepath: Optional[str | Path] = None,
) -> tuple[spect.AcquisitionData, spect.AcquisitionData]:
    """
    Performs scatter correction with the Dual Energy Window (DEW) method or,
    if SC2_hdr is provided, the Triple Energy Window (TEW) method.
    Negative values are clipped after subtraction.

    Parameters
    ----------
    PP_hdr : str
        Header filepath of the photopeak window.
    SC1_hdr : str
        Header filepath of the scatter window (DEW) or first scatter window (TEW).
    SC2_hdr : str | None
        Header filepath of the second scatter window (TEW). If None, DEW is used.
    sigma : float
        Sigma for Gaussian smoothing applied to scatter window(s) before correction.
        Interpreted in *bins* of the acquisition array.
    save_filepath : str | None
        If provided, writes the corrected acquisition data to this path.

    Returns
    -------
    acq_data_corr_clipped : spect.AcquisitionData
        Scatter-corrected acquisition data with negative values clipped to zero.
    acq_data_scatter : spect.AcquisitionData
        Estimated scatter contribution in the photopeak window.

    """

    # ---- validate inputs ----
    if not isinstance(PP_hdr, str):
        raise TypeError(f"PP_hdr must be a string (file path to header). Got {type(PP_hdr).__name__}.")
    if not isinstance(SC1_hdr, str):
        raise TypeError(f"SC1_hdr must be a string (file path to header). Got {type(SC1_hdr).__name__}.")
    if SC2_hdr is not None and not isinstance(SC2_hdr, str):
        raise TypeError(f"SC2_hdr must be a string (file path to header). Got {type(SC2_hdr).__name__}.")
    if sigma is None or not np.isfinite(float(sigma)) or float(sigma) < 0:
        raise ValueError(f"sigma must be a finite non-negative float. Got {sigma}.")

    tew_flag = SC2_hdr is not None

    # ---- load acquisition data ----
    acq_data_PP = spect.AcquisitionData(PP_hdr)
    acq_data_PP_arr = acq_data_PP.as_array()

    sigma_xy = (0.0, sigma, 0.0, sigma)

    acq_data_SC1 = spect.AcquisitionData(SC1_hdr)
    acq_data_SC1_arr = gaussian_filter(acq_data_SC1.as_array(), sigma=sigma_xy, mode="nearest")

    if tew_flag:
        acq_data_SC2 = spect.AcquisitionData(SC2_hdr)
        acq_data_SC2_arr = gaussian_filter(acq_data_SC2.as_array(), sigma=sigma_xy, mode="nearest")
        print("Second Scatter Window present. Performing TEW...")

    # ---- header tags ----
    lo_tag = "energy window lower level[1]"
    hi_tag = "energy window upper level[1]"

    def _window_width(hdr_path: str, label: str) -> float:
        try:
            lo = float(extract_header_info(hdr_path, lo_tag))
            hi = float(extract_header_info(hdr_path, hi_tag))
        except Exception as e:
            raise ValueError(f"Failed to extract energy window tags from {label} header: {hdr_path}.") from e
        w = hi - lo
        if not np.isfinite(w) or w <= 0:
            raise ValueError(f"{label} window width must be > 0. Got lo={lo}, hi={hi}, width={w}.")
        return w

    window_width_PP = _window_width(PP_hdr, "Photopeak")
    print(f"Photopeak window width: {round(window_width_PP, 2)}")

    window_width_SC1 = _window_width(SC1_hdr, "Scatter window 1")

    if tew_flag:
        print(f"Scatter window 1 width: {round(window_width_SC1, 2)}")
        window_width_SC2 = _window_width(SC2_hdr, "Scatter window 2")
        print(f"Scatter window 2 width: {round(window_width_SC2, 2)}")
    else:
        print(f"Scatter window width: {round(window_width_SC1, 2)}")

    # ---- estimate scatter under photopeak ----
    if tew_flag:
        acq_data_scatter_arr = (
            (acq_data_SC1_arr / window_width_SC1) + (acq_data_SC2_arr / window_width_SC2)
        ) * window_width_PP / 2.0
    else:
        acq_data_scatter_arr = (acq_data_SC1_arr / window_width_SC1) * window_width_PP / 2.0
        print(f"Scatter fraction: {round((window_width_PP / window_width_SC1) / 2.0, 2)}")

    # ---- subtract + clip ----
    acq_data_corr_arr = acq_data_PP_arr - acq_data_scatter_arr
    acq_data_corr_clipped_arr = np.clip(acq_data_corr_arr, a_min=0, a_max=None)

    # ---- create output AcquisitionData ----
    acq_data_corr_clipped = acq_data_PP.clone()
    acq_data_corr_clipped.fill(acq_data_corr_clipped_arr)

    acq_data_scatter = acq_data_PP.clone()
    acq_data_scatter.fill(acq_data_scatter_arr)

    if save_filepath is not None:
        if not isinstance(save_filepath, (str, Path)):
            raise TypeError(
                f"save_filepath must be a str, Path, or None. "
                f"Got {type(save_filepath).__name__}."
            )

        save_filepath = Path(save_filepath)

        if save_filepath.suffix != ".hs":
            save_filepath = save_filepath.with_suffix(".hs")

        acq_data_corr_clipped.write(str(save_filepath))

        image_duration = float(
            extract_header_info(PP_hdr, "!image duration (sec)[1]")
        )

        add_header_info(
            str(save_filepath),
            "number of time frames",
            "1",
            "!extent of rotation"
        )

        add_header_info(
            str(save_filepath),
            "!image duration (sec)[1]",
            str(image_duration),
            "!extent of rotation"
        )

        print(f"Image Duration = {image_duration} sec")
        print("Scatter correction completed successfully!")

    return acq_data_corr_clipped, acq_data_scatter


def dicom_extract_radial_position(
    tomo_dcm:str, 
    ge_flag:bool=True
) -> str:
    '''
    Extracts the radial positions of the detector heads in a SPECT acquisition from a dicom tomo file.
    
    Parameters:
    tomo_dcm (str): The filepath of the dicom tomo acquisition.
    ge (boolean, optional): GE scanners store the information differnetly from other manufacturers (default is True).

    Returns (str): A comma delimited string with a all radial positions. The string is also placed in braces ready to insert in an interfile.
    '''

    dicom_dataset = pydicom.dcmread(tomo_dcm)

    if ge_flag:
 
        rot_info_sequence_tag = (0x0054, 0x0052)
        mean_radial_position_tag = (0x0018, 0x1142)
        det_info_seq_tag = (0x0055, 0x1022)
        tomo_view_offset_tag = (0x0013, 0x101e)

        if rot_info_sequence_tag in dicom_dataset:
            rot_info_sequence = dicom_dataset[rot_info_sequence_tag].value
            for item in rot_info_sequence:
                if mean_radial_position_tag in item:
                    mean_radial_position = float(item[mean_radial_position_tag].value)

        if det_info_seq_tag in dicom_dataset:
            det_info_sequence = dicom_dataset[det_info_seq_tag].value
            for item in det_info_sequence:
                if tomo_view_offset_tag in item:
                    radial_position_offset = item[tomo_view_offset_tag].value

        radial_position = []
        for i in range(2,360,3):
            radial_position.append(mean_radial_position + radial_position_offset[i])

    else:
    
        det_info_sequence_tag = (0x0054, 0x0022)
        radial_position_tag = (0x0018, 0x1142)

        radial_position = []
        if det_info_sequence_tag in dicom_dataset:
            det_info_sequence = dicom_dataset[det_info_sequence_tag].value
            for item in det_info_sequence:
                if radial_position_tag in item:
                    radial_position_temp = item[radial_position_tag].value
                    radial_position.extend(radial_position_temp)
    
    radial_position_string = ','.join(map(str, radial_position))
    radial_position_string = '{' + radial_position_string + '}'
    
    return radial_position_string


################################################################################
#   SPECT ACQUISITION DATA STRUCTURE
################################################################################

def _sanitize_name(name: str) -> str:
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9._-]", "", name)
    return name


@dataclass
class SPECTEnergyWindow:
    """
    Data associated with one SPECT energy window.
    """

    name: str
    acquisition_data: spect.AcquisitionData
    header: dict[str, str]
    lower_keV: float | None = None
    upper_keV: float | None = None

    @property
    def central_energy_keV(self) -> float | None:
        if self.lower_keV is None or self.upper_keV is None:
            return None

        return (self.lower_keV + self.upper_keV) / 2.0

    def __getitem__(self, key: str) -> str:
        """
        Access Interfile header entries directly.

        Example:
            window["radii"]
            window["start angle"]
        """
        return self.header[key]

    def get(self, key: str, default=None):
        return self.header.get(key, default)


class AcquisitionDataSPECT:
    """
    Multi-energy SPECT acquisition-data container.

    Construct from a Nuclear Medicine DICOM using:

        data = AcquisitionDataSPECT.from_dicom("scan.dcm")

    Energy windows can then be accessed using:

        data["Photopeak"]
        data[0]

    and AcquisitionData using:

        data["Photopeak"].acquisition_data

    Interfile header fields are accessible using:

        data["Photopeak"]["radii"]
    """

    def __init__(self):
        self._windows: dict[str, SPECTEnergyWindow] = {}
        self.dicom_path: Path | None = None

    # ================================================================
    # Construction from DICOM
    # ================================================================

    @classmethod
    def from_dicom(
        cls,
        dicom_path: str | Path,
        header_overrides: dict | None = None,
    ) -> AcquisitionDataSPECT:

        dicom_path = Path(dicom_path)

        ds = pydicom.dcmread(str(dicom_path))

        obj = cls()
        obj.dicom_path = dicom_path

        # ------------------------------------------------------------
        # 1. Base STIR Interfile header
        # ------------------------------------------------------------

        base_header = {
            "!INTERFILE": "",
            "!imaging modality": "nucmed",
            "!version of keys": "3.3",
            "name of data file": "temp.s",
            "data offset in bytes": "0",
            "!GENERAL IMAGE DATA": "",
            "!type of data": "Tomographic",
            "imagedata byte order": "LITTLEENDIAN",
            "!number format": "float",
            "!number of bytes per pixel": "4",
            "calibration factor": "-1",
            "number of energy windows": "",
            "energy window lower level[1]": "0",
            "energy window upper level[1]": "0",
            "!SPECT STUDY (General)": "",
            "number of dimensions": "2",
            "matrix axis label [2]": "axial coordinate",
            "!matrix size [2]": "",
            "!scaling factor (mm/pixel) [2]": "",
            "matrix axis label [1]": "bin coordinate",
            "!matrix size [1]": "",
            "!scaling factor (mm/pixel) [1]": "",
            "!number of projections": "",
            "number of time frames": "1",
            "!image duration (sec)[1]": "",
            "!extent of rotation": "",
            "!process status": "acquired",
            "!SPECT STUDY (acquired data)": "",
            "!direction of rotation": "",
            "start angle": "",
            "orbit": "non-circular",
            "radii": "{}",
            "!END OF INTERFILE": "",
        }

        if header_overrides:
            base_header.update(header_overrides)

        # ------------------------------------------------------------
        # 2. Basic projection geometry
        # ------------------------------------------------------------

        try:
            base_header["!matrix size [1]"] = str(ds.Rows)
            base_header["!matrix size [2]"] = str(ds.Columns)
        except Exception:
            warnings.warn(
                "Rows/Columns not found in DICOM."
            )

        try:
            ps = ds.PixelSpacing

            base_header[
                "!scaling factor (mm/pixel) [1]"
            ] = str(ps[0])

            base_header[
                "!scaling factor (mm/pixel) [2]"
            ] = str(ps[1])

        except Exception:
            warnings.warn(
                "PixelSpacing not found in DICOM."
            )

        # Detector-to-centre distance / radial position
        base_header["radii"] = str(
            dicom_extract_radial_position(dicom_path)
        )

        # ------------------------------------------------------------
        # 3. Energy-window metadata
        # ------------------------------------------------------------

        ewi_tag = (0x0054, 0x0012)
        rwr_tag = (0x0054, 0x0013)
        lower_tag = (0x0054, 0x0014)
        upper_tag = (0x0054, 0x0015)
        name_tag = (0x0054, 0x0018)

        if ewi_tag not in ds:
            raise ValueError(
                "Energy Window Information Sequence "
                "not found in DICOM."
            )

        energy_windows = []

        for index, ewi_item in enumerate(ds[ewi_tag].value):

            ew_name = None
            ew_lower = None
            ew_upper = None

            if name_tag in ewi_item:
                ew_name = str(
                    ewi_item[name_tag].value
                )

            if rwr_tag in ewi_item:

                for rwr_item in ewi_item[rwr_tag].value:

                    lo = rwr_item.get(
                        lower_tag,
                        None,
                    )

                    hi = rwr_item.get(
                        upper_tag,
                        None,
                    )

                    if lo is not None and hi is not None:
                        ew_lower = float(lo.value)
                        ew_upper = float(hi.value)
                        break

            if ew_lower is None or ew_upper is None:
                raise ValueError(
                    f"Could not determine limits for "
                    f"energy window {index + 1}."
                )

            if ew_name is None:
                ew_name = (
                    f"{ew_lower:g}_{ew_upper:g}"
                )

            ew_name = _sanitize_name(ew_name)

            energy_windows.append(
                {
                    "name": ew_name,
                    "lower": ew_lower,
                    "upper": ew_upper,
                }
            )

        n_windows = len(energy_windows)

        # ------------------------------------------------------------
        # 4. Rotation / acquisition information
        # ------------------------------------------------------------

        ris_tag = (0x0054, 0x0052)
        arc_tag = (0x0018, 0x1143)
        dur_tag = (0x0018, 0x1242)
        rtd_tag = (0x0018, 0x1140)
        nfr_tag = (0x0054, 0x0053)
        sta_tag = (0x0054, 0x0200)

        if ris_tag not in ds:
            raise ValueError(
                "Rotation Information Sequence "
                "not found in DICOM."
            )

        for ris_item in ds[ris_tag].value:

            arc = ris_item.get(
                arc_tag,
                None,
            )

            if arc is not None:
                base_header[
                    "!extent of rotation"
                ] = str(arc.value)

            dur = ris_item.get(
                dur_tag,
                None,
            )

            nfr = ris_item.get(
                nfr_tag,
                None,
            )

            if dur is not None and nfr is not None:

                frame_duration = (
                    float(dur.value) / 1000.0
                )

                number_frames = int(
                    nfr.value
                )

                base_header[
                    "!image duration (sec)[1]"
                ] = str(
                    number_frames
                    * frame_duration
                )

            rtd = ris_item.get(
                rtd_tag,
                None,
            )

            if rtd is not None:

                if str(rtd.value) == "CC":
                    rtd_str = "CCW"
                else:
                    rtd_str = "CW"

                base_header[
                    "!direction of rotation"
                ] = rtd_str

            sta = ris_item.get(
                sta_tag,
                None,
            )

            if sta is not None:
                base_header[
                    "start angle"
                ] = str(sta.value)

        # ------------------------------------------------------------
        # 5. Read projection data
        # ------------------------------------------------------------

        pixel_array = ds.pixel_array

        if pixel_array.ndim != 3:
            raise ValueError(
                "Expected DICOM pixel data with shape "
                "(frames, rows, columns)."
            )

        total_frames = pixel_array.shape[0]

        if total_frames % n_windows != 0:
            raise ValueError(
                "Number of DICOM frames is not divisible "
                "by the number of energy windows."
            )

        frames_per_window = (
            total_frames // n_windows
        )

        # ------------------------------------------------------------
        # 6. Split projection data into energy windows
        # ------------------------------------------------------------

        window_blocks = [
            pixel_array[
                i * frames_per_window:
                (i + 1) * frames_per_window
            ]
            for i in range(n_windows)
        ]

        # ------------------------------------------------------------
        # 7. Construct one SIRF AcquisitionData per energy window
        # ------------------------------------------------------------

        #
        # This is important because otherwise SIRF normally creates
        # scratch-file backed AcquisitionData objects.
        #
        previous_storage_scheme = (
            spect.AcquisitionData.get_storage_scheme()
        )

        spect.AcquisitionData.set_storage_scheme(
            "memory"
        )

        try:

            with TemporaryDirectory() as tmpdir:

                tmpdir = Path(tmpdir)

                for idx, ew in enumerate(
                    energy_windows
                ):

                    header = dict(base_header)

                    header[
                        "!number of projections"
                    ] = str(frames_per_window)

                    header[
                        "!number of energy windows"
                    ] = str(n_windows)

                    header[
                        "energy window lower level[1]"
                    ] = str(ew["lower"])

                    header[
                        "energy window upper level[1]"
                    ] = str(ew["upper"])

                    # ----------------------------------------------
                    # Projection orientation
                    # ----------------------------------------------

                    block = window_blocks[idx]

                    block = np.transpose(
                        block,
                        (2, 0, 1),
                    )

                    block = np.rot90(
                        block,
                        3,
                        axes=(0, 2),
                    )

                    block = np.expand_dims(
                        block,
                        axis=0,
                    )

                    block = block.astype(
                        np.float32
                    )

                    # ----------------------------------------------
                    # Temporary Interfile
                    # ----------------------------------------------

                    temp_header = (
                        tmpdir
                        / f"window_{idx}.hs"
                    )

                    temp_raw = (
                        tmpdir
                        / f"window_{idx}.s"
                    )

                    header[
                        "name of data file"
                    ] = temp_raw.name

                    block.tofile(temp_raw)

                    with open(
                        temp_header,
                        "w",
                        encoding="utf-8",
                    ) as f:

                        for key, value in header.items():
                            f.write(
                                f"{key} := {value}\n"
                            )

                    # ----------------------------------------------
                    # Construct STIR AcquisitionData
                    # ----------------------------------------------

                    template = spect.AcquisitionData(
                        str(temp_header)
                    )

                    flipped = np.flip(
                        block,
                        axis=-1,
                    )

                    acq = (
                        template
                        .clone()
                        .fill(flipped)
                    )

                    # ----------------------------------------------
                    # Store in the container
                    # ----------------------------------------------

                    obj._windows[
                        ew["name"]
                    ] = SPECTEnergyWindow(
                        name=ew["name"],
                        acquisition_data=acq,
                        header=header,
                        lower_keV=ew["lower"],
                        upper_keV=ew["upper"],
                    )

        finally:

            spect.AcquisitionData.set_storage_scheme(
                previous_storage_scheme
            )

        return obj

    # ================================================================
    # Access
    # ================================================================

    def __getitem__(
        self,
        key: str | int,
    ) -> SPECTEnergyWindow:

        if isinstance(key, str):
            return self._windows[key]

        if isinstance(key, int):
            return list(
                self._windows.values()
            )[key]

        raise TypeError(
            "Key must be an energy-window name "
            "or integer index."
        )

    def __len__(self) -> int:
        return len(self._windows)

    def __iter__(self):
        return iter(
            self._windows.values()
        )

    @property
    def energy_windows(self) -> list[str]:
        return list(
            self._windows.keys()
        )

    # ================================================================
    # Write Interfiles
    # ================================================================

    def write(
        self,
        output_dir: str | Path,
        prefix: str,
    ) -> list[Path]:
        """
        Write one .hs/.s pair for every energy window.

        Returns
        -------
        list[Path]
            Paths of the generated .hs files.
        """

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        written_headers = []

        for window in self:

            if window.central_energy_keV is not None:

                central_energy = int(
                    round(
                        window.central_energy_keV
                    )
                )

                base_name = (
                    f"{prefix}_"
                    f"{window.name}_"
                    f"{central_energy}"
                )

            else:

                base_name = (
                    f"{prefix}_"
                    f"{window.name}"
                )

            header_path = (
                output_dir
                / f"{base_name}.hs"
            )

            raw_path = (
                output_dir
                / f"{base_name}.s"
            )

            # ------------------------------------------------------
            # Write AcquisitionData using STIR
            # ------------------------------------------------------

            window.acquisition_data.write(
                str(header_path)
            )

            # ------------------------------------------------------
            # Preserve our DICOM-derived Interfile header
            # ------------------------------------------------------

            header = dict(
                window.header
            )

            header[
                "name of data file"
            ] = raw_path.name

            #
            # SIRF/STIR has just written the raw .s data.
            # We replace only the .hs file with our stored header.
            #
            with open(
                header_path,
                "w",
                encoding="utf-8",
            ) as f:

                for key, value in header.items():
                    f.write(
                        f"{key} := {value}\n"
                    )

            written_headers.append(
                header_path
            )

        return written_headers



def acq_poisson_noise(
    hs_file: str | Path,
    save_path: str | Path,
    seed: int | None = None,
) -> spect.AcquisitionData:
    """
    Apply Poisson noise to SPECT acquisition data stored as STIR Interfile.

    The acquisition data are read from an input ``.hs`` file. Each projection
    bin is treated as the expected value of an independent Poisson
    distribution. A noisy realization is generated and written to a new
    Interfile acquisition-data pair.

    The original ``.hs`` header is preserved, except for the following fields:

    - ``!name of data file`` is replaced by the name of the output ``.s`` file.
    - ``;patient name`` is replaced by the name of the output ``.s`` file.
    - ``;!study ID`` is replaced by the name of the output ``.s`` file without
      the ``.s`` extension.

    Parameters
    ----------
    hs_file : str or pathlib.Path
        Path to the input STIR Interfile header (``.hs``).

    save_path : str or pathlib.Path
        Path of the output Interfile header. This should normally have an
        ``.hs`` extension. The corresponding binary projection-data file is
        written with the same base name and an ``.s`` extension.

        For example, if ``save_path`` is::

            /data/noisy_projection.hs

        then the header fields are set to::

            !name of data file := noisy_projection.s
            ;patient name := noisy_projection.s
            ;!study ID := noisy_projection

    seed : int or None, optional
        Seed used to initialize the NumPy random number generator.
        If provided, the Poisson realization is reproducible.
        Default is None.

    Returns
    -------
    spect.AcquisitionData
        The noisy acquisition data.

    Raises
    ------
    FileNotFoundError
        If ``hs_file`` does not exist.

    ValueError
        If the input acquisition data contain negative values.
    """

    hs_file = Path(hs_file)
    save_path = Path(save_path)

    if not hs_file.exists():
        raise FileNotFoundError(f"Input header not found: {hs_file}")

    if save_path.suffix.lower() != ".hs":
        raise ValueError("save_path must have a '.hs' extension.")

    save_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Read acquisition data
    # ------------------------------------------------------------------

    acq_data = spect.AcquisitionData(str(hs_file))
    acq_array = acq_data.as_array()

    if np.any(acq_array < 0):
        raise ValueError(
            "Acquisition data contain negative values and cannot be used "
            "as Poisson expectations."
        )

    # ------------------------------------------------------------------
    # Generate Poisson realization
    # ------------------------------------------------------------------

    rng = np.random.default_rng(seed)
    noisy_array = rng.poisson(acq_array)

    noisy_acq = acq_data.clone()
    noisy_acq.fill(noisy_array)

    # ------------------------------------------------------------------
    # Write noisy acquisition data using SIRF/STIR
    # ------------------------------------------------------------------

    noisy_acq.write(str(save_path))

    # ------------------------------------------------------------------
    # Construct output filenames
    # ------------------------------------------------------------------

    noisy_s_file = save_path.with_suffix(".s")

    data_filename = noisy_s_file.name       # e.g. noisy_projection.s
    study_id = noisy_s_file.stem            # e.g. noisy_projection

    # ------------------------------------------------------------------
    # Read the ORIGINAL header
    # ------------------------------------------------------------------

    header = hs_file.read_text()

    # ------------------------------------------------------------------
    # Replace only the requested fields
    # ------------------------------------------------------------------

    header = re.sub(
        r"(?im)^(\s*!name of data file\s*:=\s*).*$",
        rf"\g<1>{data_filename}",
        header,
    )

    header = re.sub(
        r"(?im)^(\s*;patient name\s*:=\s*).*$",
        rf"\g<1>{data_filename}",
        header,
    )

    header = re.sub(
        r"(?im)^(\s*;!study ID\s*:=\s*).*$",
        rf"\g<1>{study_id}",
        header,
    )

    # ------------------------------------------------------------------
    # Replace SIRF/STIR-generated header with modified original header
    # ------------------------------------------------------------------

    save_path.write_text(header)

    return noisy_acq


def superimpose_arr(
    img_3d,
    ct_3d,
    idx: tuple,
    *,
    cmap_list=["inferno", "gray"],
    alpha_list=[1.0, 0.5],
    img_vmin=None,
    img_vmax=None,
    ct_vmin=None,
    ct_vmax=None,
    titles=None,
    squeeze: bool = True,
    robust: bool = False,
    img_p_low: float = 1,
    img_p_high: float = 99,
    ct_robust: bool = False,
    ct_p_low: float = 1,
    ct_p_high: float = 99,
    cbar_kwargs: dict | None = None,
):
    """
    Display 3D volume(s) with CT background using tuple index `idx`.

    Accepted `img_3d` and `ct_3d` (must match structure):
      - single 3D np.ndarray
      - 1D list of 3D np.ndarray
      - 2D list (list of lists) of 3D np.ndarray

    Overlay:
      - CT shown first (background)
      - img_3d shown on top

    cmap_list:
      [img_cmap, ct_cmap]  (default ["inferno", "gray"])

    alpha_list:
      [img_alpha, ct_alpha] (default [1.0, 0.5])

    Figure sizing:
      - each row = 5 inches
      - each column = 6 inches

    Colorbars:
      - individual colorbar per panel for img_3d only
    """

    # -------------------------
    # defaults
    # -------------------------
    row_size = 5 # inches
    col_size = 6 # inches

    if not (isinstance(cmap_list, list) and len(cmap_list) == 2):
        raise ValueError("`cmap_list` must be a list of length 2.")
    if not (isinstance(alpha_list, list) and len(alpha_list) == 2):
        raise ValueError("`alpha_list` must be a list of length 2.")

    img_cmap, ct_cmap = cmap_list
    img_alpha, ct_alpha = alpha_list

    if not (0.0 <= img_alpha <= 1.0):
        raise ValueError("img_alpha must be in [0,1].")
    if not (0.0 <= ct_alpha <= 1.0):
        raise ValueError("ct_alpha must be in [0,1].")

    # -------------------------
    # idx validation
    # -------------------------
    if not isinstance(idx, tuple):
        raise TypeError("`idx` must be a tuple.")

    allowed = (slice, int, type(None))
    for item in idx:
        if item is Ellipsis:
            continue
        if not isinstance(item, allowed):
            raise TypeError("`idx` elements must be slice/int/None/Ellipsis.")

    # -------------------------
    # helpers
    # -------------------------
    def _is_3d_array(x):
        return isinstance(x, np.ndarray) and x.ndim == 3

    def _as_2d(vol, label):
        if not _is_3d_array(vol):
            raise TypeError(f"{label} must be 3D numpy array.")
        try:
            out = vol[idx]
        except Exception as e:
            raise IndexError(f"{label}: indexing failed: {e}") from e
        out = np.asarray(out)
        if squeeze:
            out = np.squeeze(out)
        if out.ndim != 2:
            raise ValueError(f"{label}: indexing must yield 2D slice.")
        return out

    def _container_kind(x):
        if isinstance(x, np.ndarray):
            return "array"
        if not isinstance(x, list):
            return "other"
        if len(x) == 0:
            return "empty"
        return "list2" if any(isinstance(el, list) for el in x) else "list1"

    def _validate_container(x, label):
        kind = _container_kind(x)
        if kind == "other":
            raise TypeError(f"{label} must be ndarray or list.")
        if kind == "empty":
            raise ValueError(f"{label} is empty list.")
        if kind == "array":
            if x.ndim != 3:
                raise TypeError(f"{label} ndarray must be 3D.")
            return "array", (1, 1)
        if kind == "list1":
            for el in x:
                if isinstance(el, list) or not _is_3d_array(el):
                    raise TypeError(f"{label} contains invalid element.")
            return "list1", (1, len(x))
        # list2
        nrows = len(x)
        ncols = len(x[0])
        for i, row in enumerate(x):
            if len(row) > ncols:
                raise ValueError(f"{label} row {i} longer than first row.")
            for el in row:
                if isinstance(el, list) or not _is_3d_array(el):
                    raise TypeError(f"{label} contains invalid grid element.")
        return "list2", (nrows, ncols)

    def _structures_match(a_kind, a_shape, b_kind, b_shape):
        if a_kind != b_kind:
            raise ValueError("img_3d and ct_3d must have same structure.")
        if a_shape != b_shape:
            raise ValueError("img_3d and ct_3d must have same grid shape.")

    def _collect_slices(container, label):
        kind = _container_kind(container)
        if kind == "array":
            return [_as_2d(container, label)]
        if kind == "list1":
            return [_as_2d(el, label) for el in container]
        if kind == "list2":
            slices = []
            for row in container:
                for el in row:
                    slices.append(_as_2d(el, label))
            return slices
        return []

    def _global_vmin_vmax(slices, do_robust, lo, hi):
        if do_robust:
            vals = np.concatenate([s.ravel() for s in slices])
            return np.percentile(vals, lo), np.percentile(vals, hi)
        return min(np.min(s) for s in slices), max(np.max(s) for s in slices)

    # -------------------------
    # Validate containers
    # -------------------------
    img_kind, img_shape = _validate_container(img_3d, "img_3d")
    ct_kind, ct_shape = _validate_container(ct_3d, "ct_3d")
    _structures_match(img_kind, img_shape, ct_kind, ct_shape)

    # -------------------------
    # Global scaling
    # -------------------------
    if img_vmin is None or img_vmax is None:
        img_slices = _collect_slices(img_3d, "img_3d")
        vmin_g, vmax_g = _global_vmin_vmax(img_slices, robust, img_p_low, img_p_high)
        img_vmin = img_vmin if img_vmin is not None else vmin_g
        img_vmax = img_vmax if img_vmax is not None else vmax_g

    if ct_vmin is None or ct_vmax is None:
        ct_slices = _collect_slices(ct_3d, "ct_3d")
        ct_vmin_g, ct_vmax_g = _global_vmin_vmax(ct_slices, ct_robust, ct_p_low, ct_p_high)
        ct_vmin = ct_vmin if ct_vmin is not None else ct_vmin_g
        ct_vmax = ct_vmax if ct_vmax is not None else ct_vmax_g

    if cbar_kwargs is None:
        cbar_kwargs = {}
    cbar_fraction = cbar_kwargs.pop("fraction", 0.046)
    cbar_pad = cbar_kwargs.pop("pad", 0.04)

    # -------------------------
    # Plot helper
    # -------------------------
    def _plot_pair(ax, img_vol, ct_vol, title=None):
        ct_img = _as_2d(ct_vol, "ct_3d")
        img_img = _as_2d(img_vol, "img_3d")

        im = ax.imshow(img_img, cmap=img_cmap, vmin=img_vmin, vmax=img_vmax, alpha=img_alpha)
        ct = ax.imshow(ct_img, cmap=ct_cmap, vmin=ct_vmin, vmax=ct_vmax, alpha=ct_alpha)

        ax.set_axis_off()
        if title is not None:
            ax.set_title(title)

        fig.colorbar(im, ax=ax, fraction=cbar_fraction, pad=cbar_pad, **cbar_kwargs)

    # -------------------------
    # Plot cases
    # -------------------------
    if img_kind == "array":
        fig, ax = plt.subplots(1, 1, figsize=(col_size, row_size))
        _plot_pair(ax, img_3d, ct_3d, titles if isinstance(titles, str) else None)
        fig.tight_layout()
        return fig, ax

    if img_kind == "list1":
        n = img_shape[1]
        fig, axes = plt.subplots(1, n, squeeze=False, figsize=(col_size * n, row_size))
        axes = axes[0]
        for j in range(n):
            title = titles[j] if isinstance(titles, list) else None
            _plot_pair(axes[j], img_3d[j], ct_3d[j], title)
        fig.tight_layout()
        return fig, axes

    # grid
    nrows, ncols = img_shape
    fig, axes = plt.subplots(nrows, ncols, squeeze=False, figsize=(col_size * ncols, row_size * nrows))
    for i in range(nrows):
        for j in range(ncols):
            ax = axes[i, j]
            if j < len(img_3d[i]):
                title = titles[i][j] if isinstance(titles, list) else None
                _plot_pair(ax, img_3d[i][j], ct_3d[i][j], title)
            else:
                ax.set_axis_off()
    fig.tight_layout()
    return fig, axes


#################################################################################################
def display_arr(
    arr_3d,
    idx: tuple,
    *,
    cmap: str | list = "inferno",
    vmin=None,
    vmax=None,
    titles=None,
    squeeze: bool = True,
    robust: bool = False,
    p_low: float = 1,
    p_high: float = 99,
    cbar_kwargs: dict | None = None,
):
    """
    Display 3D volume(s) using a NumPy-style tuple index `idx` that should yield a 2D slice.

    Accepted `arr_3d`:
      - a single 3D np.ndarray
      - a 1D list of 3D np.ndarray (displayed side-by-side)
      - a 2D list (list of lists) of 3D np.ndarray (displayed in a grid)

    cmap / vmin / vmax:
      - single value -> broadcast to all panels
      - 1D list for 1D arr_3d
      - 2D list for 2D arr_3d

    Scaling:
      - if a panel's vmin/vmax is None, it is computed from that panel
      - if robust=True, percentiles are used for that panel
    """

    row_size = 5
    col_size = 6

    # -------------------------
    # idx validation
    # -------------------------
    if not isinstance(idx, tuple):
        raise TypeError(
            f"`idx` must be a tuple (e.g. (slice(...), 95, slice(...))). Got {type(idx).__name__}."
        )

    allowed = (slice, int, type(None))
    for k, item in enumerate(idx):
        if item is Ellipsis:
            continue
        if not isinstance(item, allowed):
            raise TypeError(
                f"`idx[{k}]` must be slice/int/None/Ellipsis. Got {type(item).__name__}."
            )

    # -------------------------
    # helpers
    # -------------------------
    def _is_3d_array(x) -> bool:
        return isinstance(x, np.ndarray) and x.ndim == 3

    def _as_2d(vol: np.ndarray) -> np.ndarray:
        if not _is_3d_array(vol):
            if isinstance(vol, np.ndarray):
                raise TypeError(f"Expected a 3D array (ndim==3), got ndim=={vol.ndim}.")
            raise TypeError(f"Expected np.ndarray, got {type(vol).__name__}.")

        try:
            out = vol[idx]
        except Exception as e:
            raise IndexError(
                f"Indexing with idx={idx} failed for volume shape={vol.shape}: {e}"
            ) from e

        out = np.asarray(out)
        if squeeze:
            out = np.squeeze(out)

        if out.ndim != 2:
            raise ValueError(
                f"Indexing must yield a 2D array for plotting. Got shape {out.shape} (ndim={out.ndim}). "
                f"Use an idx that selects a 2D plane, e.g. (slice(None), 95, slice(None)) or (..., 60)."
            )
        return out

    def _panel_limits(img: np.ndarray, vmin_i, vmax_i):
        if vmin_i is not None and vmax_i is not None:
            return vmin_i, vmax_i

        if robust:
            vals = img.ravel()
            auto_vmin = float(np.percentile(vals, p_low))
            auto_vmax = float(np.percentile(vals, p_high))
        else:
            auto_vmin = float(np.min(img))
            auto_vmax = float(np.max(img))

        if vmin_i is None:
            vmin_i = auto_vmin
        if vmax_i is None:
            vmax_i = auto_vmax

        return vmin_i, vmax_i

    def _is_seq(x):
        return isinstance(x, Sequence) and not isinstance(x, (str, bytes))

    def _normalize_param(param, arr_3d, name: str):
        """
        Broadcast or validate cmap/vmin/vmax so it matches arr_3d structure.

        Returns:
          - scalar for single ndarray
          - 1D list for 1D arr_3d
          - 2D list for 2D arr_3d
        """
        # Single array
        if isinstance(arr_3d, np.ndarray):
            return param

        # Must be list from here
        if not isinstance(arr_3d, list) or len(arr_3d) == 0:
            return param

        is_2d = any(isinstance(el, list) for el in arr_3d)

        # 1D list case
        if not is_2d:
            n = len(arr_3d)

            if not _is_seq(param):
                return [param] * n

            if len(param) != n:
                raise ValueError(
                    f"For a 1D arr_3d list, `{name}` must be a scalar or a list of length {n}."
                )
            return list(param)

        # 2D grid case
        nrows = len(arr_3d)
        row_lengths = [len(row) for row in arr_3d]

        if not _is_seq(param):
            return [[param] * row_lengths[i] for i in range(nrows)]

        # If it's 2D already
        if all(_is_seq(row) for row in param):
            if len(param) != nrows:
                raise ValueError(
                    f"For a 2D arr_3d grid, `{name}` must have {nrows} rows."
                )
            out = []
            for i, row in enumerate(param):
                if len(row) != row_lengths[i]:
                    raise ValueError(
                        f"For row {i}, `{name}` must have length {row_lengths[i]}."
                    )
                out.append(list(row))
            return out

        raise ValueError(
            f"For a 2D arr_3d grid, `{name}` must be either a scalar or a 2D list matching arr_3d."
        )

    # default colorbar kwargs
    if cbar_kwargs is None:
        cbar_kwargs = {}
    cbar_fraction = cbar_kwargs.pop("fraction", 0.046)
    cbar_pad = cbar_kwargs.pop("pad", 0.04)

    # Normalize cmap/vmin/vmax to match layout
    cmap_n = _normalize_param(cmap, arr_3d, "cmap")
    vmin_n = _normalize_param(vmin, arr_3d, "vmin")
    vmax_n = _normalize_param(vmax, arr_3d, "vmax")

    # -------------------------
    # Case 1: single 3D array
    # -------------------------
    if isinstance(arr_3d, np.ndarray):
        if arr_3d.ndim != 3:
            raise TypeError(f"Input is a numpy array but not 3D (ndim={arr_3d.ndim}).")

        img = _as_2d(arr_3d)
        vmin_i, vmax_i = _panel_limits(img, vmin_n, vmax_n)

        fig, ax = plt.subplots(1, 1, squeeze=True, figsize=(col_size, row_size))
        im = ax.imshow(img, cmap=cmap_n, vmin=vmin_i, vmax=vmax_i)
        ax.set_axis_off()

        if isinstance(titles, str):
            ax.set_title(titles)

        fig.colorbar(im, ax=ax, fraction=cbar_fraction, pad=cbar_pad, **cbar_kwargs)
        fig.tight_layout()
        return fig, ax

    # -------------------------
    # Must be list from here
    # -------------------------
    if not isinstance(arr_3d, list):
        raise TypeError(f"Expected np.ndarray or list, got {type(arr_3d).__name__}.")

    if len(arr_3d) == 0:
        raise ValueError("Input list is empty; nothing to display.")

    is_2d = any(isinstance(el, list) for el in arr_3d)

    # -------------------------
    # Case 2: 1D list of 3D arrays
    # -------------------------
    if not is_2d:
        for k, el in enumerate(arr_3d):
            if isinstance(el, list):
                raise ValueError("List nesting > 2 detected (unexpected list inside 1D list).")
            if not _is_3d_array(el):
                raise TypeError(f"Element {k} is not a 3D numpy array.")

        n = len(arr_3d)
        fig, axes = plt.subplots(1, n, squeeze=False, figsize=(col_size * n, row_size))
        axes = axes[0]

        if titles is not None and not (isinstance(titles, list) and len(titles) == n):
            raise ValueError("For a 1D list, `titles` must be None or a list of length N.")

        for j, vol in enumerate(arr_3d):
            img = _as_2d(vol)
            vmin_j, vmax_j = _panel_limits(img, vmin_n[j], vmax_n[j])

            im = axes[j].imshow(
                img,
                cmap=cmap_n[j],
                vmin=vmin_j,
                vmax=vmax_j,
            )
            axes[j].set_axis_off()
            if titles is not None:
                axes[j].set_title(titles[j])
            fig.colorbar(im, ax=axes[j], fraction=cbar_fraction, pad=cbar_pad, **cbar_kwargs)

        fig.tight_layout()
        return fig, axes

    # -------------------------
    # Case 3: 2D list (grid) of 3D arrays
    # -------------------------
    if not all(isinstance(row, list) for row in arr_3d):
        raise TypeError("Mixed structure: expected a list of lists for the 2D case.")

    nrows = len(arr_3d)
    ncols = len(arr_3d[0])
    if ncols == 0:
        raise ValueError("First row is empty; nothing to display.")

    for i, row in enumerate(arr_3d):
        if len(row) > ncols:
            raise ValueError(
                f"Row {i} has length {len(row)} which is longer than first row length {ncols}."
            )
        for j, el in enumerate(row):
            if isinstance(el, list):
                raise ValueError("List nesting > 2 detected (list inside grid cell).")
            if not _is_3d_array(el):
                raise TypeError(f"Grid element ({i},{j}) is not a 3D numpy array.")

    if titles is not None:
        if not (isinstance(titles, list) and all(isinstance(r, list) for r in titles)):
            raise ValueError("For a grid, `titles` must be None or a list of lists.")
        if len(titles) != nrows:
            raise ValueError("For a grid, `titles` must have the same number of rows as arr_3d.")
        for i in range(nrows):
            if len(titles[i]) > len(arr_3d[i]):
                raise ValueError(f"Titles row {i} is longer than arr_3d row {i}.")

    fig, axes = plt.subplots(
        nrows,
        ncols,
        squeeze=False,
        figsize=(col_size * ncols, row_size * nrows),
    )

    for i in range(nrows):
        for j in range(ncols):
            ax = axes[i, j]
            if j < len(arr_3d[i]):  # allow shorter rows
                img = _as_2d(arr_3d[i][j])
                vmin_ij, vmax_ij = _panel_limits(img, vmin_n[i][j], vmax_n[i][j])

                im = ax.imshow(
                    img,
                    cmap=cmap_n[i][j],
                    vmin=vmin_ij,
                    vmax=vmax_ij,
                )
                if titles is not None and j < len(titles[i]):
                    ax.set_title(titles[i][j])
                fig.colorbar(im, ax=ax, fraction=cbar_fraction, pad=cbar_pad, **cbar_kwargs)
            ax.set_axis_off()

    fig.tight_layout()
    return fig, axes


from scipy.interpolate import make_interp_spline


def calculate_recovery_coefficients(
    source,
    recon_dict,
    masks_dict,
    subiterations,
    sphere_numbers=range(1, 7),
    calibration_subit="100",
    verbose=False
):
    """
    Calculate recovery coefficients for each sphere and reconstruction.

    Parameters
    ----------
    source : np.ndarray
        Reference activity distribution.

    recon_dict : dict
        Dictionary containing reconstructed images, indexed by subiteration.

    masks_dict : dict
        Dictionary containing sphere masks named 'sphere_1', 'sphere_2', etc.

    subiterations : array-like
        OSEM subiterations to evaluate.

    sphere_numbers : iterable, optional
        Sphere numbers to include.

    calibration_subit : str, optional
        Reconstruction used to calculate the image calibration factor.

    verbose : bool, optional
        Print calculated values.

    Returns
    -------
    rc_data : np.ndarray
        Recovery coefficients with shape
        (number of subiterations, number of spheres).

    icf : float
        Image calibration factor.
    """

    # Image calibration factor
    icf = (
        np.sum(recon_dict[calibration_subit])
        / np.sum(source)
    )

    if verbose:
        print(f"Image calibration factor: {icf:.4f}\n")

    rc_data = []

    for subit in subiterations:

        if verbose:
            print(f"SUBITERATION {subit}")

        rc_sub_data = []

        for sp_n in sphere_numbers:

            mask = masks_dict[f"sphere_{sp_n}"]

            rc = (
                np.sum(recon_dict[str(subit)] * mask)
                / icf
                / np.sum(source * mask)
            )

            rc_sub_data.append(rc)

            if verbose:
                print(f"Sphere {sp_n}: {rc:.4f}")

        rc_data.append(rc_sub_data)

        if verbose:
            print()

    return np.asarray(rc_data), icf


def plot_recovery_coefficients(
    subiterations,
    rc_data,
    diameters_mm,
    title=None,
    smooth=True
):
    """
    Plot recovery coefficient as a function of OSEM subiterations.
    """

    subiterations = np.asarray(subiterations)
    rc_data = np.asarray(rc_data)

    if smooth:
        subit_plot = np.linspace(
            subiterations.min(),
            subiterations.max(),
            500
        )

        spline = make_interp_spline(
            subiterations,
            rc_data,
            k=3
        )

        rc_plot = spline(subit_plot)

    else:
        subit_plot = subiterations
        rc_plot = rc_data

    plt.figure(figsize=(8, 6))

    for i, diameter in enumerate(diameters_mm):

        plt.plot(
            subit_plot,
            rc_plot[:, i],
            label=f"{diameter} mm"
        )

        plt.scatter(
            subiterations,
            rc_data[:, i]
        )

    if title:
        plt.title(title, fontsize=14)

    plt.xlabel("Subiterations", fontsize=12)
    plt.ylabel("Recovery coefficient", fontsize=12)

    plt.xlim(0, subiterations.max())
    plt.ylim(0, 1.0)

    plt.xticks(
        np.arange(0, subiterations.max() + 1, 10)
    )
    plt.yticks(
        np.arange(0, 1.01, 0.1)
    )

    plt.grid(axis="y", alpha=0.7)

    plt.legend(
        title="Sphere diameter",
        loc="lower center",
        bbox_to_anchor=(0.5, 0.02),
        ncol=3
    )

    plt.show()


## MC SCATTER RECOSNTRUCTION

def divide(a, b, eps=1e-8):
    return (a + eps) / (b + eps)

def osem_step(acq_model, acq_data, current_image, sensitivity_image, scatter):
    fp = acq_model.forward(current_image) + scatter
    bpr = acq_model.backward(divide(acq_data, fp))
    return divide(current_image * bpr, sensitivity_image)

def run_osem(acq_model, acq_data, initial_image, iterations, subsets, scatter=0):
    current_image = initial_image.clone()
    sensitivity_images = []
    one_sino = acq_data.get_uniform_copy(1)

    for i in range(iterations):
        for s in range(subsets):
            print("#############################")
            print(f"Computing Iteration {i} and Subset {s}")
            acq_model.subset_num = s

            if len(sensitivity_images) < subsets:
                sensitivity_images.append(
                    acq_model.backward(one_sino)
                )

            current_image = osem_step(
                acq_model,
                acq_data,
                current_image,
                sensitivity_images[s],
                scatter
            )

    return current_image