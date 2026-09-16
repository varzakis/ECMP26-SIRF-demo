


              SIMIND Monte Carlo Simulation Program    V8.0  
------------------------------------------------------------------------------
 Phantom S : h2o       Crystal...: nai       InputFile.: lu177_mc_scatter  
 Phantom B : bone      BackScatt.: pmt       OutputFile: lu177_mc_scatter  
 Collimator: pb_sb2    SourceRout: smap      SourceImg.: lu177_mc_scatter_s
 Cover.....: al        ScoreRout.: scattwin  DensityImg: lu177_mc_scatter_d
------------------------------------------------------------------------------
 PhotonEnergy.......: 208          lu177     PhotonsPerProj....: 40054          
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
 Emission type......: 2                      Initial Weight....: 62797.26819    
 NN ScalingFactor...: 0.05                   Energy Channels...: 512            
                                                                              
 SPECT DATA
 RotationMode.......: 360                    Nr of Projections.: 120            
 RotationAngle......: 3                      Projection.[start]: 1              
 Orbital fraction...: 0                      Projection...[end]: 120            
 Center of Rotation File: lu177_mc_scatter.cor
                                                                              
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
  Scattwin results: Window file: lu177_mc_scatter.win
  
  Win  WinAdded  Range(keV)   ScaleFactor
   1       0    187.2 - 228.8   1.000
   2       1    187.2 - 228.8   1.000
  
  Win    Total    Scatter   Primary  S/P-Ratio S/T Ratio  Cps/MBq
   1   0.432E+07 0.144E+07 0.288E+07 0.500E+00 0.333E+00 0.324E+01
   2   0.432E+07 0.144E+07 0.288E+07 0.500E+00 0.333E+00 0.324E+01
  
  Win  Geo(Air)  Pen(Air)  Sca(Air)  Geo(Tot)  Pen(Tot)  Sca(Tot)
   1   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
   2   100.00%     0.00%     0.00%   100.00%     0.00%     0.00%
  
  Win   SC 1  SC 2  SC 3
   1   84.8% 13.7%  1.5%
   2   84.8% 13.7%  1.5%
                                                                              
 INTERACTIONS IN THE CRYSTAL
 MaxValue spectrum..: 0.3151E+06     
 MaxValue projection: 539.3          
 CountRate spectrum.: 0.2258E+06     
 CountRate E-Window.: 0.1223E+06     
                                                                              
 SCATTER IN ENERGY WINDOW
 Scatter/Primary....: 1.8546         
 Scatter/Total......: 0.64969        
 Scatter order 1....: 51.25 %        
 Scatter order 2....: 33.08 %        
 Scatter order 3....: 15.68 %        
                                                                              
 CALCULATED DETECTOR PARAMETERS
 Efficiency E-window: 0.4686         
 Efficiency spectrum: 0.8654         
 Sensitivity Cps/MBq: 11.0049        
 Sensitivity Cpm/uCi: 24.4309        
                                                                              
 Simulation started.: 2026:09:16 20:19:38
 Simulation stopped.: 2026:09:16 20:23:21
 Elapsed time.......: 0 h, 3 m and 43 s
 DetectorHits.......: 102620         
 DetectorHits/CPUsec: 461            
                                                                              
 OTHER INFORMATION
 EMISSION
 Compiled 2025:01:28 with intel Linux 
 Current random number generator: ranmar
 Energy resolution as function of 1/sqrt(E)
 Header file: lu177_mc_scatter.h00
 Linear angle sampling within acceptance angle
 Inifile: simind.ini
 Command: lu177_mc_scatter lu177_mc_scatter /NN:0.05/FI:lu177/CC:ge-megp/RR:12345/PX:0.4420000076293945
