import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "/home/jovyan/sirf-demo/.packages")
#%% Import SIRF
import sirf.STIR as spect
import numpy as np
from simind_python_connector import StirSimindAdaptor
from pathlib import Path

demo_path = Path("/home/jovyan/sirf-demo/SIRF-demo-1")

sim_dir = demo_path / "simind_data" / "lu177_128"
#sim_dir = demo_path / "simind_data" / "tc99m_128"
tomo_cor = sim_dir / "tomo" / "lu177_simulation_tew.hs"
#tomo_cor = sim_dir / "tomo" / "tc99m_simulation_dew.hs"
ctac = sim_dir / "input" / "nema_lu_ctac.hv"
#ctac = sim_dir / "input" / "nema_tc_ctac.hv"

acquisition_data = spect.AcquisitionData(str(tomo_cor))
matrix_size = (128,) * 3
voxel_size = (4.42,) * 3
subiterations = 100
subsets = 2
save_interval = 10
recon_dir = sim_dir / "recons" / "osem"
recon_dir.mkdir(parents=True, exist_ok=True)
name_prefix = "tc99m_sim_osem"
attenuation_map = spect.ImageData(str(ctac))
keep_views_in_cache = False
    
sigma_0 = 2.35598 #mm
slope = 0.01771

# create a template for the reconstructed image
initial_image = spect.ImageData(acquisition_data)
initial_image.initialise(matrix_size, vsize=voxel_size)
initial_image.set_modality("NM")
initial_image.fill(1)

# set up the acquisition model matrix
acq_model_matrix = spect.SPECTUBMatrix()

# keep all views in cache to speed up reconstruction
acq_model_matrix.set_keep_all_views_in_cache(keep_views_in_cache)

# ---- attenuation correction (triggered by presence of attenuation_map) ----
# attenuation map needs to be flipped due to a STIR bug
flipped_attenuation_map = attenuation_map.clone()
flipped_attenuation_map.fill(np.flip(attenuation_map.as_array(), axis=2))
acq_model_matrix.set_attenuation_image(flipped_attenuation_map)

# ---- PSF modelling (triggered only if both params provided) ----
#acq_model_matrix.set_resolution_model(float(sigma_0), float(slope), full_3D=False)

# feed projections and initial estimate into the model
am = spect.AcquisitionModelUsingMatrix(acq_model_matrix)
am.set_up(acquisition_data, initial_image)

# set up the objective function
obj_fun = spect.make_Poisson_loglikelihood(acquisition_data)
obj_fun.set_acquisition_model(am)

# keep initial_image intact as only reconstructed_image will be updated with every subiteration
reconstructed_image = initial_image

# setup reconstructor and reconstruct
recon = spect.OSMAPOSLReconstructor()
recon.set_num_subiterations(subiterations)
recon.set_save_interval(save_interval)
recon.enable_output()
recon.set_output_filename_prefix(str(recon_dir / name_prefix))
recon.set_objective_function(obj_fun)
recon.set_num_subsets(subsets)

recon.set_up(reconstructed_image)
recon.reconstruct(reconstructed_image)
# %%
