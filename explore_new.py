import os
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
from astropy.io import ascii
import glob
import pandas as pd


program_type = 'GO-1' # ERS, GTO, GO-1

programs = [1981, 1433, 1837, 1895, 1963, 2079, 2130,
            2282, 2514, 2561, 1727, 1936, 1984, 2061,
            2091, 2395, 2107]

#defining namespaces

rt = '{http://www.stsci.edu/JWST/APT}'
mi = '{http://www.stsci.edu/JWST/APT/Template/MiriImaging}' 
nci = '{http://www.stsci.edu/JWST/APT/Template/NircamImaging}'
ns = '{http://www.stsci.edu/JWST/APT/Instrument/Nirspec}' 
niwfss ='{http://www.stsci.edu/JWST/APT/Template/NirissWfss}' 
ncwfss = '{http://www.stsci.edu/JWST/APT/Template/NircamWfss}'
nsmos = '{http://www.stsci.edu/JWST/APT/Template/NirspecMOS}'
nsfss = '{http://www.stsci.edu/JWST/APT/Template/NirspecFixedSlitSpectroscopy}' 
nsbots = '{http://www.stsci.edu/JWST/APT/Template/NirspecBrightObjectTimeSeries}' 
ncgts = '{http://www.stsci.edu/JWST/APT/Template/NircamGrismTimeSeries}' 
ncwfss = '{http://www.stsci.edu/JWST/APT/Template/NircamWfss}' 
#loop over each program

for program in programs:

    print('-'*20)
    print(program)

    zipf = zipfile.ZipFile(f'apts/{program_type}/{program}.aptx', 'r')

    r = zipf.open(f'{program}.xml').read()

    root = ET.fromstring(r)
    
    ProposalID = []
    ObservationNumber= []
    TargetID = []
    TarNumber= []
    EqCoord = {}
    TargetNumber = []
    TargetScienceDuration = []
    EquatorialCoordinates = []
    CoordinatedParallel = []
    TargetInstrument = []
    ParallelInstrument= []
    MiriFilters = []
    NIRCamLongFilters = []
    NIRCamShortFilters = []
    NirspecFilters = []
    NirspecGratings = []
    NIRCAM_FilterConfiguration = []
    MIRI_FilterConfiguration = []
    NIRSPEC_FilterConfiguration = []
    
    #Loop over observations
    
    for observation in root.iter(f'{rt}Observation'):
    
        try:
            for ID in root.iter(f'{rt}ProposalInformation'):
                try:
                    ProposalID.append(ID.find(f'{rt}ProposalID').text)
                except:
                    pass
        except:
            pass
        try:
            ObservationNumber.append(int(observation.find(f'{rt}Number').text))
        except:
            pass
        try:
            Id = (observation.find(f'{rt}TargetID').text)
            TNumber = int(Id.split(' ')[0])
            TargetID.append(Id)
            TargetNumber.append(TNumber)
        except:
            pass
        try:
            TargetScienceDuration.append(int(observation.find(f'{rt}ScienceDuration').text))
        except:
            TargetScienceDuration.append('N/A')
        try:
            CoParallel = observation.find(f'{rt}CoordinatedParallel').text 
       
            if CoParallel == 'true':
                CoordinatedParallel.append(observation.find(f'{rt}CoordinatedParallel').text)
                PInstrument = observation.find(f'{rt}CoordinatedParallelSet').text
                ParallelInstrument.append(PInstrument.split('-')[1])
            if CoParallel == 'false':
                CoordinatedParallel.append(observation.find(f'{rt}CoordinatedParallel').text)
                ParallelInstrument.append('N/A')
        except:
            pass
        try:
            TargetInstrument.append(observation.find(f'{rt}Instrument').text)
        except:
            TargetInstrument.append('N/A')    
        try:
            Configuration = []
            for configuration in observation.iter(f'{nci}FilterConfig'):
                Config = []
                try:
                    Config.append(configuration.find(f'{nci}ShortFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nci}LongFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nci}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nci}Integrations').text)
                except:
                    pass
                Configuration.append(Config)
                
            for configuration in observation.iter(f'{ncgts}NircamGrismTimeSeries'):
                Config = []
                try:
                    Config.append(configuration.find(f'{ncgts}ShortPupilFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncgts}LongPupilFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncgts}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncgts}Integrations').text)
                except:
                    pass
                Configuration.append(Config)
            
            for configuration in observation.iter(f'{ncwfss}DiExposure'):
                Config = []
                try:
                    Config.append(configuration.find(f'{ncwfss}ShortFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncwfss}LongFilter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncwfss}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{ncwfss}Integrations').text)
                except:
                    pass  
                Configuration.append(Config)
                
            NIRCAM_FilterConfiguration.append(Configuration)
                
        except:
            pass    
        try:
            Configuration = []
            for configuration in observation.iter(f'{mi}FilterConfig'):
                Config = []
                try:
                    Config.append(configuration.find(f'{mi}Exposures').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{mi}Filter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{mi}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{mi}Integrations').text)
                except:
                    pass
                
                Configuration.append(Config)
            MIRI_FilterConfiguration.append(Configuration)
                
        except:
            pass    
        
        try:
            Configuration = []
            for configuration in observation.iter(f'{nsmos}Exposure'):
                Config = []
                try:
                    Config.append(configuration.find(f'{nsmos}Grating').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsmos}Filter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsmos}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsmos}Integrations').text)
                except:
                    pass
                
                Configuration.append(Config)   
                
            for configuration in observation.iter(f'{nsfss}Exposure'):
                Config = []
                try:
                    Config.append(configuration.find(f'{nsfss}Grating').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsfss}Filter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsfss}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsfss}Integrations').text)
                except:
                    pass
                    
                Configuration.append(Config)
            for configuration in observation.iter(f'{nsbots}NirspecBrightObjectTimeSeries'):
                Config = []
                try:
                    Config.append(configuration.find(f'{nsbots}Grating').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsbots}Filter').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsbots}Groups').text)
                except:
                    pass
                try:
                    Config.append(configuration.find(f'{nsbots}Integrations').text)
                except:
                    pass
                    
                Configuration.append(Config)
            NIRSPEC_FilterConfiguration.append(Configuration)
                
        except:
            pass    
  #      try:
   #         NspecFilters = []
    #        for Nspfilters in observation.iter(f'{ns}filter'):
     #           NspecFilters.append(Nspfilters.text)
      #      NirspecFilters.append(NspecFilters) 
       # except: 
        #    pass
      #  try:
       #     NspecGratings = []
        #    for Nspgratings in observation.iter(f'{ns}grating'):
         #       NspecGratings.append(Nspgratings.text)
          #  NirspecGratings.append(NspecGratings) 
     #   except: 
      #      pass  

        #       try:
     #       MiFilters = []
    #        for Mfilters in observation.iter(f'{mi}Filter'):
   #             MiFilters.append(Mfilters.text)
  #          MiriFilters.append(MiFilters) 
 #       except: 
#            pass
        
        
       # try:
       #     NlFilters = []
      #      for Nlfilters in observation.iter(f'{nci}LongFilter'):
     #           NlFilters.append(Nlfilters.text)   
    #        NIRCamLongFilters.append(NlFilters)
   #     except:
  #          pass
 #       try:
#            NsFilters = []
     #       for Nsfilters in observation.iter(f'{nci}ShortFilter'):
      #          NsFilters.append(Nsfilters.text) 
    #        NIRCamShortFilters.append(NsFilters)
   #     except:
  #          pass
        
    #Loop over Targets
    
    for Target in root.iter(f'{rt}Target'):
        try:
            TarNumber = (int(Target.find(f'{rt}Number').text))
        except:
            TarNumber = ('N/A')
        try:
            EqCoord[TarNumber] = (Target.find(f'{rt}EquatorialCoordinates').attrib['Value'])
        except:
            EqCoord[TarNumber] = ('N/A')
   
   #Reorder coordinates so they match with each target in each observation
    
    try:
        order_list = TargetNumber
        reordered_dict = {k: EqCoord[k] for k in order_list}
        EquatorialCoordinates = [reordered_dict[k] for k in order_list if k in reordered_dict]
    except: 
        while len(EquatorialCoordinates) != len(ObservationNumber):
            EquatorialCoordinates.append('N/A')
   
   
    
    #create data frame of extracted information
    
    program_df =pd.DataFrame(list(zip(ProposalID, ObservationNumber, TargetID, TargetNumber,TargetScienceDuration, 
                                      EquatorialCoordinates, CoordinatedParallel, 
                                      TargetInstrument, ParallelInstrument, 
                                      NIRCAM_FilterConfiguration, MIRI_FilterConfiguration, NIRSPEC_FilterConfiguration)), 
                             columns=['ProposalID', 'ObservationNumber', 'TargetID', 'TargetNumber',
                                      'TargetScienceDuration', 'EquatorialCoordinates', 
                                      'CoordinatedParallel', 'TargetInstrument','ParallelInstrument', 
                                      'NIRCAM_FilterConfiguration: (Short Filter, Long Filter, Groups, Integrations)',
                                      'MIRI_FilterConfiguration: (Exposures, Filter, Groups, Integrations)',
                                      'NIRSPEC_FilterConfiguration: (Grating, Filter, Groups, Integrations)'])
    
    #try and set title for each program number
    program_df.style.set_caption('program')
    
    print(program_df)
    
    #convert data frame to csv file
    
    program_df.to_csv(f"program{program}.csv")
    
    

extension = 'csv'
all_filenames = [i for i in glob.glob('program*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, sep= ',') for f in all_filenames])
#export to csv
combined_csv.to_csv( "AllProgramData.csv", index=False)    
    
    
    
###### need to look at 1981, 1895, 2514, 1936 ######
# 1936, 2061 needs different namespace (nsfss instead of ns) for filter/grism
# same for 1981 
# GW1 and Kilonova have no coordinates
# 2514 has no targets section.
