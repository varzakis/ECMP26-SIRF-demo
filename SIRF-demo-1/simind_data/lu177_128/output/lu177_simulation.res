


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: lu177_simulation  
 Phantom B : bone      BackScatt.: pmt       OutputFile: lu177_simulation  
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: lu177_simulation_s
 Cover.....: al        ScoreRout.: scattwin  DensityImg: lu177_simulation_d
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 92890          
 EnergyResolution...: 12           Spectra   Activity..........: 11110          
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
 Emission type......: 2                      Initial Weight....: 27078.06847    
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
   1   0.451E+07 0.151E+07 0.301E+07 0.500E+00 0.333E+00 0.339E+01
   2   0.209E+07 0.201E+07 0.804E+05 0.250E+02 0.962E+00 0.157E+01
   3   0.948E+05 0.313E+05 0.636E+05 0.492E+00 0.330E+00 0.711E-01
   4   0.948E+05 0.313E+05 0.636E+05 0.492E+00 0.330E+00 0.711E-01
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   4   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   85.1% 13.4%  1.5%
   2   58.6% 33.4%  8.1%
   3   76.2% 19.7%  4.1%
   4   76.2% 19.7%  4.1%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.3259E+06     
 MaxValue projection: 561.6          
 CountRate spectrum.: 0.2361E+06     
 CountRate E-Window.: 0.1277E+06     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.85064        
 Scatter/Total......: 0.6492         
 Scatter order 1....: 51.38 %        
 Scatter order 2....: 32.92 %        
 Scatter order 3....: 15.7  %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4677         
 Efficiency spectrum: 0.8649         
 Sensitivity Cps/MBq: 11.49          
 Sensitivity Cpm/uCi: 25.5077        
                                                                              
 Simulation started.: 2026:09:11 15:12:05
 Simulation stopped.: 2026:09:11 15:20:59
 Elapsed time.......: 0 h, 8 m and 54 s
 DetectorHits.......: 248415         
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
