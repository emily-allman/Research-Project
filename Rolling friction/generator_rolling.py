"""
@author: Emily Allman, based off code of J.Grogan
"""

#------------------------------------------------------------------------------------------
# Calling in Libraries
#------------------------------------------------------------------------------------------

import gmsh                    # mesh generation
import numpy as np             # for numerical operations
import os                      # for file operations
import sympy                   # for symbolic mathematics
from jinja2 import Template    # for templating
import glob                    # for file pattern matching
from natsort import natsorted  # for natural sorting
import toml                    # for configuration

if gmsh.isInitialized():
    gmsh.finalize()
gmsh.initialize()


#------------------------------------------------------------------------------------------
# Specifying RAM geometry
#------------------------------------------------------------------------------------------

# cylinder dimensions
z0_cylinder         = 0                 #m
x0_cylinder         = 0                 #m
y0_cylinder         = 0                 #m
lc_cylinder         = 1e-7              #-
cylinder_height     = 0.08              #m  (80 mm)

# inface dimensions
z0_inface           = 0.065      #      #m  - insertion just below cylinder top
x0_inface           = 0                 #m
y0_inface           = 0                 #m
lc_inface           = 1e-7              #-

# Mesh Configuration
cylinder_mesh_max   = 0.005             #-
cylinder_mesh_min   = 0.0               #- 

inface_mesh_max     = 0.05              #- 
inface_mesh_min     = 0.0               #-

#------------------------------------------------------------------------------------------
# Simulation parameters
#------------------------------------------------------------------------------------------

timestep            = 0.5e-5            #s
dumptime            = 0.1               #s
ontime              = 12.5              #s
filltime            = 2                 #s
settletime          = 2                 #s
w                   = 392.322           #rad/s (62.44hz)

density             = 1580              #kg/m^3
youngs_modulus      = 5e6               #Pa
poisson_ratio       = 0.4               #-

sliding_pp          = 0.720222          #-
sliding_pw          = 0.720222          #-

num_studies         = 8                 #-

number_of_seeds     = 5

restitution_pp      = 0.4
restitution_pw      = 0.4
       
fricRollPW = 0.043350  
fricRollPP_min = 0.1
fricRollPP_max = 0.8

corPP = 0.664838           
corPW = 0.664838                   

cohPP = 0             
cohPW = 0             

#------------------------------------------------------------------------------------------
# Job specifications
#------------------------------------------------------------------------------------------

job_runtime         = "100:00:00"        # hr:min:sec
ntasks              = int(8)

#------------------------------------------------------------------------------------------
# Preliminary Calculations
#------------------------------------------------------------------------------------------

input_ontime        = np.round(np.ceil(ontime/timestep)*timestep,8)
input_filltime      = np.round(np.ceil(filltime/timestep)*timestep,8)
input_settletime    = np.round(np.ceil(settletime/timestep)*timestep,8)
oscillation_period  = 2*np.pi/w

cylinder_radii      = np.round(0.03, 8)
inface_radii        = np.round(cylinder_radii - 0.0005,8)

fricRollPP          = np.linspace(fricRollPP_min, fricRollPP_max, num_studies)

seeds = [0]*number_of_seeds

for k in range(number_of_seeds):
    seeds[k] = sympy.prime(2000 + k)

#------------------------------------------------------------------------------------------
# Open Files
#------------------------------------------------------------------------------------------

with open(os.path.join("mesh1", "cylinder.geo"), 'r') as f:
    cylinder = f.read()

with open(os.path.join("mesh1", "inface.geo"), 'r') as f:
    inface = f.read()

with open(os.path.join("mesh1","shake.sim"), 'r') as f:
    simulation = f.read()

with open(os.path.join("mesh1","batch_launch.sh"), 'r') as f:
    batch_launch = f.read()

with open(os.path.join("mesh1", "particles.sim"), 'r') as f:
    particles = f.read()

#------------------------------------------------------------------------------------------
# File Generation
#------------------------------------------------------------------------------------------
# List of N values to iterate over
N_values = [17850, 35700, 53550, 71400, 89250, 107100, 124950, 142800, 160650, 178500]
# calculated number of particles given particle radii distrubtion for fill heights 10-100%

#------------------------------------------------------------------------------------------
# Updated File Generation with N values
#-------------------------
for N in N_values:
    input_ontime = np.round(np.ceil(ontime/timestep)*timestep,8)
    input_filltime = np.round(np.ceil(filltime/timestep)*timestep,8)
    input_settletime = np.round(np.ceil(settletime/timestep)*timestep,8)
    oscillation_period = 2*np.pi/w
    cylinder_radii = np.round(0.03, 8)
    inface_radii = np.round(cylinder_radii - 0.0005, 8)
    fricRollPP = np.linspace(fricRollPP_min, fricRollPP_max, num_studies)
    seeds = [0] * number_of_seeds
    for k in range(number_of_seeds):
        seeds[k] = sympy.prime(2000 + k)
    
    for seed in seeds:
        j2_cylinder = [0] * num_studies
        j2_inface = [0] * num_studies
        j2_simulation = [0] * num_studies
        j2_batch_launch = [0] * num_studies
        j2_particles = [0] * num_studies 
        newpath = [0] * num_studies # added
        for i in range(num_studies):
            # setting up jinja dictionaries for text replacement of template files
            cylinder_mesh_data = { "cylinder_height": cylinder_height,
                                   "cylinder_radius": cylinder_radii,
                                   "z_0": z0_cylinder, 
                                   "y_0": y0_cylinder,
                                   "x_0": x0_cylinder,
                                   "lc": lc_cylinder,
                                   "mesh_max": cylinder_mesh_max,
                                   "mesh_min": cylinder_mesh_min,
                                   "Algor": 6
                                   }
            
            inface_mesh_data = { "inface_radius": inface_radii, 
                                "z_0": z0_inface, 
                                "y_0": y0_inface, 
                                "x_0": x0_inface, 
                                "lc": lc_inface, 
                                "mesh_max": inface_mesh_max, 
                                "mesh_min": inface_mesh_min, 
                                "Algor": 6 }
            simulation_data = { "timestep": timestep, 
                               "dumptime": dumptime, 
                               "filltime": input_filltime, 
                               "ontime": input_ontime, 
                               "settletime": input_settletime, 
                               "number_particles": N,  
                               "youngs_modulus": youngs_modulus, 
                               "poisson_ratio": poisson_ratio,
                               "sliding_pp": sliding_pp, 
                               "sliding_pw": sliding_pw, 
                               "fricRollPP": fricRollPP[i], 
                               "fricRollPW": fricRollPW, 
                               "restitution_pp": restitution_pp, 
                               "restitution_pw": restitution_pw, 
                               "cohPP": cohPP, 
                               "cohPW": cohPW, 
                               "seed": seed, 
                               "period": oscillation_period }
            
            particles_data = {"restitution_pp": restitution_pp, 
                              "restitution_pw": restitution_pw,
                              "sliding_pp": sliding_pp,
                              "sliding_pw": sliding_pw,
                              "corPP": corPP,
                              "corPW": corPW,
                              "cohPP": cohPP,
                              "cohPW": cohPW,
                              }

            batch_launch_data = { "runtime": job_runtime, 
                                 "ntasks": ntasks }
            post_processing_data = { "cylinder_radii": cylinder_radii, 
                                    "fricRollPP": fricRollPP[i] }
            j2_cylinder[i] = Template(cylinder)
            j2_inface[i] = Template(inface)
            j2_simulation[i] = Template(simulation)
            j2_batch_launch[i] = Template(batch_launch)
            j2_particles[i] = Template(particles) 
            
            # Creating file paths
            study_directory = os.path.join(f"{N:.0f}_particles", f"seed_{seed}")
            if not os.path.exists(study_directory):
                os.makedirs(study_directory)
            simulation_newpath = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}")
            if not os.path.exists(simulation_newpath):
                os.makedirs(simulation_newpath)
            batch_launch_newpath = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}")
            if not os.path.exists(batch_launch_newpath):
                os.makedirs(batch_launch_newpath)
            mesh_newpath = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}", "mesh")
            if not os.path.exists(mesh_newpath):
                os.makedirs(mesh_newpath)
            inface_newpath = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}", "mesh")
            if not os.path.exists(inface_newpath):
                os.makedirs(inface_newpath)
            toml_path = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}")
            if not os.path.exists(toml_path):
                os.makedirs(toml_path)
            particles_newpath = os.path.join(study_directory, f"rolling_{fricRollPP[i]:.2f}", "mesh")
            if not os.path.exists(particles_newpath):
                os.makedirs(particles_newpath)
            
            # Creating new simulation files
            cylinder_geo_file_new = os.path.join(mesh_newpath, "shake_cylinder.geo")
            inface_geo_file_new = os.path.join(inface_newpath, "inface.geo")
            simulation_file_new = os.path.join(simulation_newpath, "shake.sim")
            batch_launch_file_new = os.path.join(batch_launch_newpath, "batch_launch.sh")
            toml_file = os.path.join(toml_path, "data.toml")
            particles_sim_file_new = os.path.join(particles_newpath, "particles.sim")
            
            # Writing parameters to new files
            with open(cylinder_geo_file_new, 'w') as f:
                f.write(j2_cylinder[i].render(cylinder_mesh_data))
            with open(inface_geo_file_new, 'w') as f:
                f.write(j2_inface[i].render(inface_mesh_data))
            with open(simulation_file_new, 'w') as f:
                f.write(j2_simulation[i].render(simulation_data))
            with open(batch_launch_file_new, 'w') as f:
                f.write(j2_batch_launch[i].render(batch_launch_data))
            with open(toml_file, 'w') as f:
                toml.dump(post_processing_data, f)
            with open(particles_sim_file_new, 'w') as f:
                f.write(j2_particles[i].render(particles_data))  # added
            
            # Creating STL files from the gmsh geo files
            gmsh.open(cylinder_geo_file_new)
            gmsh.open(inface_geo_file_new)
        
        #--------------------------------
        # Launch Slurm Jobs
        #- 
        glob_input = os.path.join(study_directory, "rolling_*")
        directories = natsorted([k for k in glob.glob(glob_input)])
        for directory in directories:
            launch_file = os.path.join(directory, "batch_launch.sh")
            cmd = f"sbatch --output={directory}/slurm-%j.out {launch_file} {directory}"
            print(cmd)
            os.system(cmd)
