


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: lu177_sim         
 Phantom B : bone      BackScatt.: pmt       OutputFile: lu177_sim         
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: lu177_sim_src     
 Cover.....: al        ScoreRout.: scattwin  DensityImg: lu177_sim_dns     
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 159787         
 EnergyResolution...: 12           Spectra   Activity..........: 3077.6         
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
 Emission type......: 2                      Initial Weight....: 4360.57054     
 NN ScalingFactor...: 0.01                   Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: lu177_sim.cor
                                                                              
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
  Scattwin results: Window file: lu177_sim.win       
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    187.2 - 228.8   1.000
   2       1    187.2 - 228.8   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.152E+07 0.317E+06 0.120E+07 0.264E+00 0.209E+00 0.410E+01
   2   0.152E+07 0.317E+06 0.120E+07 0.264E+00 0.209E+00 0.410E+01
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   88.5% 10.5%  1.0%
   2   88.5% 10.5%  1.0%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.1076E+06     
 MaxValue projection: 35.69          
 CountRate spectrum.: 0.7016E+05     
 CountRate E-Window.: 0.3766E+05     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 0.9902         
 Scatter/Total......: 0.49754        
 Scatter order 1....: 59.1  %        
 Scatter order 2....: 29.29 %        
 Scatter order 3....: 11.61 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4617         
 Efficiency spectrum: 0.8602         
 Sensitivity Cps/MBq: 12.2377        
 Sensitivity Cpm/uCi: 27.1677        
                                                                              
 Simulation started.: 2026:09:21 00:48:00
 Simulation stopped.: 2026:09:21 01:00:10
 Elapsed time.......: 0 h, 12 m and 10 s
 DetectorHits.......: 276230         
 DetectorHits/CPUsec: 379            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: lu177_sim.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: lu177_sim lu177_sim /NN:0.01/FI:lu177/CC:ge-megp/RR:12345/PX:0.4420000076293945
