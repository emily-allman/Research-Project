# Information about the code #
The following code are examples of that used to investigate the effects of particle-particle properties and fill height on the mixing efficiency in the simulated RAM. The following code was generated for use in DEM simulations using BlueBEAR. 

The particle-particle properties investigated for this research project were restitution, rolling friction and sliding friction. 

## Run order ##
simulation_launch.sh, generator.py
Simulations also used a particle file 

## Curve fitting ##
To calculate the mixing rate, a sigmoidal curve was fitted to each simulation mixing curve, using the file: sigmoidal_curve_fitting.py 
The mixing time was then calculated using the file: calculation_of_mixing_time.py - which analyses the fitted sigmoidal curve to estimate the mixing time for each simulation


## Software used ##
### BlueBEAR ###
Information about BlueBEAR and submitting jobs are as follows: https://docs.bear.bham.ac.uk/bluebear/jobs/

### ParaView ###
ParaView was used during this project to provide visual outputs of the DEM simulations. More information about ParaView can be found using: https://www.paraview.org/ 

