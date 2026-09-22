


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: lu177_simulation  
 Phantom B : bone      BackScatt.: pmt       OutputFile: lu177_simulation  
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: lu177_simulation_s
 Cover.....: al        ScoreRout.: scattwin  DensityImg: lu177_simulation_d
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 92897          
 EnergyResolution...: 12           Spectra   Activity..........: 2584.6         
 MaxScatterOrder....: 3            ge-megp   DetectorLenght....: 20             
 DetectorWidth......: 27           SPECT     DetectorHeight....: 0.9525         
 UpperEneWindowTresh: 312          x-rays    Distance to det...: 17.022         
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
 Emission type......: 2                      Initial Weight....: 6298.89308     
 NN ScalingFactor...: 0.1                    Energy Channels...: 512            
                                                                              
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
   1   0.105E+07 0.352E+06 0.703E+06 0.500E+00 0.333E+00 0.340E+01
   2   0.489E+06 0.470E+06 0.187E+05 0.252E+02 0.962E+00 0.158E+01
   3   0.220E+05 0.725E+04 0.148E+05 0.491E+00 0.329E+00 0.709E-01
   4   0.220E+05 0.725E+04 0.148E+05 0.491E+00 0.329E+00 0.709E-01
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   4   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   85.2% 13.4%  1.4%
   2   58.6% 33.3%  8.1%
   3   75.4% 20.5%  4.1%
   4   75.4% 20.5%  4.1%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.7552E+05     
 MaxValue projection: 129.3          
 CountRate spectrum.: 0.5504E+05     
 CountRate E-Window.: 0.2978E+05     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.85143        
 Scatter/Total......: 0.6493         
 Scatter order 1....: 51.41 %        
 Scatter order 2....: 32.95 %        
 Scatter order 3....: 15.64 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4682         
 Efficiency spectrum: 0.8653         
 Sensitivity Cps/MBq: 11.5227        
 Sensitivity Cpm/uCi: 25.5805        
                                                                              
 Simulation started.: 2026:09:22 15:59:59
 Simulation stopped.: 2026:09:22 16:08:53
 Elapsed time.......: 0 h, 8 m and 54 s
 DetectorHits.......: 248782         
 DetectorHits/CPUsec: 466            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: lu177_simulation.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: lu177_simulation lu177_simulation /NN:0.1/FI:lu177/CC:ge-megp/RR:12345/PX:0.4420000076293945
