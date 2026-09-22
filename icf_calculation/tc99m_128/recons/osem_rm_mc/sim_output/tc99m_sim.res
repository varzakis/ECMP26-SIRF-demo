


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: tc99m_sim         
 Phantom B : bone      BackScatt.: pmt       OutputFile: tc99m_sim         
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: tc99m_sim_src     
 Cover.....: al        ScoreRout.: scattwin  DensityImg: tc99m_sim_dns     
------------------------------------------------------------------------------
 PhotonEnergy.......: 140          tc99m     PhotonsPerProj....: 251945         
 EnergyResolution...: 12           Spectra   Activity..........: 3084           
 MaxScatterOrder....: 3            ge-megp   DetectorLenght....: 20             
 DetectorWidth......: 27           SPECT     DetectorHeight....: 0.9525         
 UpperEneWindowTresh: 210          x-rays    Distance to det...: 11.942         
 LowerEneWindowTresh: 70           Random    ShiftSource X.....: 0              
 PixelSize  I.......: 0.442        Cover     ShiftSource Y.....: 0              
 PixelSize  J.......: 0.442        Phantom   ShiftSource Z.....: 0              
 HalfLength S.......: 28.288       Resolut   HalfLength P......: 28.288         
 HalfWidth  S.......: 28.288       Header    HalfWidth  P......: 28.288         
 HalfHeight S.......: 28.288                 HalfHeight P......: 28.288         
 SourceType.........: Integer2Map            PhantomType.......: Integer2Map  
------------------------------------------------------------------------------
 GENERAL DATA
 keV/channel........: 0.5                    CutoffEnergy......: 0              
 Photons/Bq.........: 0.88524                StartingAngle.....: 0              
 CameraOffset X.....: 0                      CoverThickness....: 0.1            
 CameraOffset Y.....: 0                      BackscatterThickn.: 0              
 MatrixSize I.......: 128                    IntrinsicResolut..: 0.55           
 MatrixSize J.......: 128                    AcceptanceAngle...: 4.02754        
 Emission type......: 2                      Initial Weight....: 10836.03411    
 NN ScalingFactor...: 0.01                   Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: tc99m_sim.cor
                                                                              
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
  Scattwin results: Window file: tc99m_sim.win       
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    126.5 - 154.6   1.000
   2       1    126.5 - 154.6   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.203E+08 0.505E+07 0.152E+08 0.332E+00 0.249E+00 0.547E+02
   2   0.203E+08 0.505E+07 0.152E+08 0.332E+00 0.249E+00 0.547E+02
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   85.6% 13.0%  1.5%
   2   85.6% 13.0%  1.5%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.5430E+06     
 MaxValue projection: 250.0          
 CountRate spectrum.: 0.3438E+06     
 CountRate E-Window.: 0.3256E+06     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.36906        
 Scatter/Total......: 0.57789        
 Scatter order 1....: 51.18 %        
 Scatter order 2....: 31.7  %        
 Scatter order 3....: 17.12 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.8939         
 Efficiency spectrum: 0.9437         
 Sensitivity Cps/MBq: 105.5849       
 Sensitivity Cpm/uCi: 234.3984       
                                                                              
 Simulation started.: 2026:09:21 00:12:56
 Simulation stopped.: 2026:09:21 00:33:20
 Elapsed time.......: 0 h, 20 m and 24 s
 DetectorHits.......: 466795         
 DetectorHits/CPUsec: 381            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: tc99m_sim.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: tc99m_sim tc99m_sim /NN:0.01/FI:tc99m/CC:ge-megp/RR:12345/PX:0.4420000076293945
