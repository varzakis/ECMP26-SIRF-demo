


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: lu177_simulation  
 Phantom B : bone      BackScatt.: pmt       OutputFile: lu177_simulation  
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: lu177_simulation_s
 Cover.....: al        ScoreRout.: scattwin  DensityImg: lu177_simulation_d
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 364469         
 EnergyResolution...: 12           Spectra   Activity..........: 3147.3         
 MaxScatterOrder....: 3            ge-megp   DetectorLenght....: 20             
 DetectorWidth......: 27           SPECT     DetectorHeight....: 0.9525         
 UpperEneWindowTresh: 312          x-rays    Distance to det...: 11.979         
 LowerEneWindowTresh: 104          Random    ShiftSource X.....: 0              
 PixelSize  I.......: 0.442        Cover     ShiftSource Y.....: 0              
 PixelSize  J.......: 0.442        Phantom   ShiftSource Z.....: 0              
 HalfLength S.......: 28.288       Resolut   HalfLength P......: 28.288         
 HalfWidth  S.......: 28.288       Header    HalfWidth  P......: 28.288         
 HalfHeight S.......: 28.288                 HalfHeight P......: 28.288         
 SourceType.........: Integer2Map            PhantomType.......: Integer2Map  
------------------------------------------------------------------------------
 GENERAL DATA
 keV/channel........: 1                      CutoffEnergy......: 0              
 Photons/Bq.........: 0.2264                 StartingAngle.....: 0              
 CameraOffset X.....: 0                      CoverThickness....: 0.1            
 CameraOffset Y.....: 0                      BackscatterThickn.: 0              
 MatrixSize I.......: 128                    IntrinsicResolut..: 0.55           
 MatrixSize J.......: 128                    AcceptanceAngle...: 4.02754        
 Emission type......: 2                      Initial Weight....: 1955.01517     
 NN ScalingFactor...: 0.01                   Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: lu177_simulation.cor
                                                                              
 COLLIMATOR DATA FOR ROUTINE: Analytical          
 CollimatorCode.....: ge-megp                CollimatorType....: Parallel 
 HoleSize X.........: 0.25                   Distance X........: 0.03           
 HoleSize Y.........: 0.28868                Distance Y........: 0.17032        
 CenterShift X......: 0.14                   X-Ray flag........: T              
 CenterShift Y......: 0.24249                CollimThickness...: 4.1            
 HoleShape..........: Hexagonal              Space Coll2Det....: 0              
 CollDepValue [57]..: 0                      CollDepValue [58].: 0              
 CollDepValue [59]..: 0                      CollDepValue [60].: 0              
                                                                              
 IMAGE-BASED PHANTOM DATA
 RotationCentre.....:  65, 65                Bone definition...: 1170           
 CT-Pixel size......: 0.442                  Slice thickness...: 0.442          
 StartImage.........: 1                      No of CT-Images...: 128            
 MatrixSize I.......: 128                    CTmapOrientation..: 0              
 MatrixSize J.......: 128                    StepSize..........: 0.44167        
 CenterPoint I......: 65                     ShiftPhantom X....: 0              
 CenterPoint J......: 65                     ShiftPhantom Y....: 0              
 CenterPoint K......: 65                     ShiftPhantom Z....: 0              
                                                                              
------------------------------------------------------------------------------
  Scattwin results: Window file: lu177_simulation.win
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    187.2 - 228.8   1.000
   2       0    156.4 - 183.6   1.000
   3       0    229.4 - 258.6   1.000
   4       1    229.4 - 258.6   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.193E+07 0.405E+06 0.152E+07 0.266E+00 0.210E+00 0.510E+01
   2   0.589E+06 0.549E+06 0.405E+05 0.136E+02 0.931E+00 0.156E+01
   3   0.392E+05 0.802E+04 0.312E+05 0.257E+00 0.205E+00 0.104E+00
   4   0.392E+05 0.802E+04 0.312E+05 0.257E+00 0.205E+00 0.104E+00
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   4   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   88.5% 10.5%  0.9%
   2   67.3% 27.2%  5.6%
   3   80.7% 16.8%  2.5%
   4   80.7% 16.8%  2.5%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.1369E+06     
 MaxValue projection: 38.52          
 CountRate spectrum.: 0.8946E+05     
 CountRate E-Window.: 0.4797E+05     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 0.99363        
 Scatter/Total......: 0.4984         
 Scatter order 1....: 59.23 %        
 Scatter order 2....: 29.21 %        
 Scatter order 3....: 11.56 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4612         
 Efficiency spectrum: 0.8601         
 Sensitivity Cps/MBq: 15.2423        
 Sensitivity Cpm/uCi: 33.838         
                                                                              
 Simulation started.: 2026:09:20 22:06:15
 Simulation stopped.: 2026:09:20 22:40:41
 Elapsed time.......: 0 h, 34 m and 26 s
 DetectorHits.......: 787017         
 DetectorHits/CPUsec: 381            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: lu177_simulation.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: lu177_simulation lu177_simulation /NN:0.01/FI:lu177/CC:ge-megp/RR:12345/PX:0.4420000076293945
