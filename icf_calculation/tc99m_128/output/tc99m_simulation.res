


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: tc99m_simulation  
 Phantom B : bone      BackScatt.: pmt       OutputFile: tc99m_simulation  
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: tc99m_simulation_s
 Cover.....: al        ScoreRout.: scattwin  DensityImg: tc99m_simulation_d
------------------------------------------------------------------------------
 PhotonEnergy.......: 140          tc99m     PhotonsPerProj....: 360899         
 EnergyResolution...: 12           Spectra   Activity..........: 3116.4         
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
 Emission type......: 2                      Initial Weight....: 7644.15096     
 NN ScalingFactor...: 0.01                   Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: tc99m_simulation.cor
                                                                              
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
  Scattwin results: Window file: tc99m_simulation.win
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    114.0 - 126.0   1.000
   2       0    126.5 - 154.6   1.000
   3       1    126.5 - 154.6   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.526E+07 0.461E+07 0.647E+06 0.712E+01 0.877E+00 0.141E+02
   2   0.239E+08 0.595E+07 0.180E+08 0.331E+00 0.249E+00 0.640E+02
   3   0.239E+08 0.595E+07 0.180E+08 0.331E+00 0.249E+00 0.640E+02
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   3   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   67.2% 27.0%  5.8%
   2   85.7% 12.9%  1.5%
   3   85.7% 12.9%  1.5%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.6418E+06     
 MaxValue projection: 267.9          
 CountRate spectrum.: 0.4056E+06     
 CountRate E-Window.: 0.3843E+06     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.365          
 Scatter/Total......: 0.57717        
 Scatter order 1....: 51.31 %        
 Scatter order 2....: 31.65 %        
 Scatter order 3....: 17.04 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.8939         
 Efficiency spectrum: 0.9437         
 Sensitivity Cps/MBq: 123.3005       
 Sensitivity Cpm/uCi: 273.7272       
                                                                              
 Simulation started.: 2026:09:20 21:29:11
 Simulation stopped.: 2026:09:20 22:03:14
 Elapsed time.......: 0 h, 34 m and 3 s
 DetectorHits.......: 778614         
 DetectorHits/CPUsec: 381            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: tc99m_simulation.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: tc99m_simulation tc99m_simulation /NN:0.01/FI:tc99m/CC:ge-megp/RR:12345/PX:0.4420000076293945
