import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "/home/jovyan/sirf-demo/.packages")

import sirf.STIR as spect
from simind_python_connector import StirSimindAdaptor
import stir_simind_utils as utils

mc_sc_flag = True

demo1_path = Path("/home/jovyan/sirf-demo/SIRF-demo-1")
demo2_path = Path("/home/jovyan/sirf-demo/SIRF-demo-2")

sim_dir = demo1_path / "simind_data" / "lu177_128"
input_dir = sim_dir / "input"
tomo_dir = sim_dir / "tomo"
mc_dir = demo2_path / "mc_scatter"
mc_dir.mkdir(parents=True, exist_ok=True)

# Change these paths if required for the measured dataset
measured_path = tomo_dir / "lu177_simulation_em_noisy.hs"
ctac_path = input_dir / "nema_lu_ctac.hv"

measured_data = spect.AcquisitionData(str(measured_path))
attenuation_map = spect.ImageData(str(ctac_path))

matrix_size = (128,) * 3
voxel_size = (4.42,) * 3

initial_image = spect.ImageData(measured_data)
initial_image.initialise(matrix_size, vsize=voxel_size)
initial_image.set_modality("NM")
initial_image.fill(1)

# STIR attenuation-map orientation
attenuation_map_stir = attenuation_map.clone()
attenuation_map_stir.fill(
    np.flip(attenuation_map.as_array(), axis=2)
)

sigma_0 = 2.35598  # mm
slope = 0.01771

acq_model_matrix = spect.SPECTUBMatrix()
acq_model_matrix.set_keep_all_views_in_cache(True)
acq_model_matrix.set_attenuation_image(attenuation_map_stir)
#acq_model_matrix.set_resolution_model(
#    float(sigma_0),
#    float(slope),
#    full_3D=False
#)

acq_model = spect.AcquisitionModelUsingMatrix(
    acq_model_matrix
)
if mc_sc_flag:
    scatter_estimate = spect.AcquisitionData(str(mc_dir / "lu177_mc_scatter_sca_w1.hs"))
    acq_model.set_additive_term(scatter_estimate)
acq_model.set_up(measured_data, initial_image)

subiterations = 100
subsets = 2
if mc_sc_flag:
    save_interval = 10
    name_prefix = "lu177_mc_recon"

obj_fun = spect.make_Poisson_loglikelihood(measured_data)
obj_fun.set_acquisition_model(acq_model)

recon = spect.OSMAPOSLReconstructor()
recon.set_num_subiterations(subiterations)
if mc_sc_flag:
    recon.set_save_interval(save_interval)
    recon.enable_output()
    recon.set_output_filename_prefix(str(mc_dir / name_prefix))
recon.set_num_subsets(subsets)
recon.set_objective_function(obj_fun)

recon_image = initial_image.clone()

recon.set_up(recon_image)
recon.reconstruct(recon_image)

if not mc_sc_flag:
    recon_image.write(str(mc_dir / "initial_reconstruction"))