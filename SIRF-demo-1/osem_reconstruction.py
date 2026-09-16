import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "/home/jovyan/sirf-demo/.packages")
#%% Import SIRF
import sirf.STIR as spect
import numpy as np
from simind_python_connector import StirSimindAdaptor
from pathlib import Path

demo_path = Path("/home/jovyan/sirf-demo/SIRF-demo-1")

nuclide = "tc99m"
#nuclide = "lu177"
recon_type = "osem"
#recon_type = "osem_rm"

config_dict = {
    "tc99m": {
        "simind_dir": "tc99m_128",
        "tomo_name": "tc99m_simulation_dew.hs",
        "ctac_name": "nema_tc_ctac.hv",
    },
    "lu177": {
        "simind_dir": "lu177_128",
        "tomo_name": "lu177_simulation_tew.hs",
        "ctac_name": "nema_lu_ctac.hv",
    }

}

sigma_0 = 2.35598 #mm
slope = 0.01771

sim_dir = demo_path / "simind_data" / config_dict[nuclide]["simind_dir"]
tomo_cor = sim_dir / "tomo" / config_dict[nuclide]["tomo_name"]
ctac = sim_dir / "input" / config_dict[nuclide]["ctac_name"]
recon_dir = sim_dir / "recons" / recon_type
recon_dir.mkdir(parents=True, exist_ok=True)
name_prefix = f"{nuclide}_sim_{recon_type}"

acquisition_data = spect.AcquisitionData(str(tomo_cor))
matrix_size = (128,) * 3
voxel_size = (4.42,) * 3
subiterations = 100
subsets = 2
save_interval = 10

attenuation_map = spect.ImageData(str(ctac))
keep_views_in_cache = True

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
acq_model_matrix.set_resolution_model(float(sigma_0), float(slope), full_3D=False)

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
