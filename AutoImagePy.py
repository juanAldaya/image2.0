
from infoSvs import infoSvs
import configFiles
import pwScripts
import csvFiles
import timeMgmt
import xmlFiles
import fileMgmt

import time
import datetime

# from bs4 import BeautifulSoup, NavigableString
# from bs4 import Comment
# import pandas as pd



svName = input('SV Name: (ex. BMP): \n')


#########  VARIABLES THAT NEED THE PREVIOUS FUNCTIONS AND NEEDED FROM PREP REP####


actualMonthYear = str(timeMgmt.threeFirstChars(timeMgmt.previousMonthName())+timeMgmt.lastTwoDigitsOfTheYear()) # EX. MAY 24 ACTUAL

lastMonthYear = str(timeMgmt.get_month_name_two_months_ago()+str(timeMgmt.lastTwoDigitsOfTheYear()))# EX. APRIL 24 LAST

actualYear = str(datetime.datetime.now().year)

imagesPath = infoSvs[svName]['local']

WkPath = infoSvs[svName]['global']  ## WK DISK GLOB TEAM. SOURCE

  
###########################HERE RUN THE SCRIPT OF REPLICATE PREP FROM WK DISK###  



if fileMgmt.checkReleases(WkPath): #: #checkReleases(WkPath)

    if pwScripts.replicationPrep():#replicationPrep():#replicationPrep():


        actualPrepRelease = imagesPath + '\\Win11_' + timeMgmt.threeFirstChars(timeMgmt.previousMonthName())+ "_" + actualYear + '\\Deploy'

        lastPrepRelease = imagesPath + '\\Win11_' + str(timeMgmt.threeFirstChars(timeMgmt.get_month_name_two_months_ago())) + "_" + actualYear + "\\Deploy" #possible error when the year is still last one and not the actual (like december)

        
        time.sleep(1)
        
        if pwScripts.replicationProv(): ###    REPLICATION OF THE PREP    ####
            print("Provisioning replication went OK")
            
        else:
            print("Something went wrong with the prov replication")




        ### SCRIPTS FOLDERS
        scriptFolderActualRelease = actualPrepRelease + "\\Scripts"
        scriptFolderLastRelease = lastPrepRelease + "\\Scripts"


        ## TASK SEQUENCE

        actualPrepTaskSequence = actualPrepRelease+"\\Control\\WIN11PREP_" + str(timeMgmt.last_month_number()) + str(timeMgmt.lastTwoDigitsOfTheYear()) + "\\ts.xml"
        lastPrepTaskSequence = lastPrepRelease+ "\\Control\\WIN11PREP_" + str(timeMgmt.get_month_two_months_ago()) + str(timeMgmt.lastTwoDigitsOfTheYear()) + "\\ts.xml"
    


        actualCSPrep = actualPrepRelease + "\\Control\\CustomSettings.ini"
        lastCSPrep = lastPrepRelease + "\\Control\\CustomSettings.ini"

        ##DEPLOY WIZRD FILES
        actualDw = scriptFolderActualRelease + "\\DeployWiz_Definition_ENU.xml"
        lastDw = scriptFolderLastRelease + "\\DeployWiz_Definition_ENU.xml"



        ###### CUSTOM PREP ############
        # 
        # 
        # 
        #      
        pwScripts.copyThingsPrep(scriptFolderLastRelease, scriptFolderActualRelease) ## Copy scripts, $1 folder, etc


        configFiles.generateNewCSPrep(lastCSPrep, actualCSPrep, actualPrepRelease) #CONFIG SETTINGS .INI PREP

        xmlFiles.deployWizardPrep(actualDw, lastDw) #Script deploy wizard prep

        csvFiles.modelAliasPrep(scriptFolderLastRelease, scriptFolderActualRelease) #script model alias prep




        ######      WORKBENCH STAGE     ######

        xmlFiles.modifyTaskSequencePrep(lastPrepTaskSequence, actualPrepTaskSequence) #modify task sequence prep



        ############   -------------------      CUSTOM PROV   ----------------------------   ##########


        lastReleaseProv = lastPrepRelease + "\\$OEM$\\ProvisioningPackage\\Deploy"
        actualReleaseProv = actualPrepRelease + "\\$OEM$\\ProvisioningPackage\\Deploy"
        
        scriptsLastReleaseProv = lastReleaseProv+'\\Scripts' # The source directory
        scriptsActualReleaseProv = actualReleaseProv+'\\Scripts' # The destination directory
        
        actualProvTaskSequence = actualReleaseProv + "\\Control\\APP-WINX-CIO\\ts.xml"
        lastProvTaskSequence = lastReleaseProv  + "\\Control\\APP-WINX-CIO\\ts.xml"
        
        lastCustomSettingsGDN = lastReleaseProv + "\\Control\\CustomSettingsGDN.ini"
        actualCustomSettingsGDN = actualReleaseProv + "\\Control\\CustomSettingsGDN.ini"

        lastProvCustomSettings = lastReleaseProv + "\\Control\\CustomSettingsGDN.ini"
        actualProvCustomSettings = actualReleaseProv + "\\Control\\CustomSettingsGDN.ini"        

        actualDwProv = scriptsActualReleaseProv + "\\DeplowWiz_Definition_ENU.xml"




        configFiles.boostrapProv()  # OK  #

        configFiles.configCSProv() # OK  #
  


        pwScripts.scriptsProv(scriptsLastReleaseProv, scriptsActualReleaseProv) # OK #

        xmlFiles.removeItemDWProv(actualDwProv)  # OK #



        #gdnOUMapping(scriptsLastReleaseProv, scriptsActualReleaseProv)  # OK # 
        #gndSiteProv(scriptsLastReleaseProv, scriptsActualReleaseProv) # OK #

        #WORKBENCH STAGE
        xmlFiles.modifyTaskSequenceProv(lastProvTaskSequence, actualProvTaskSequence)
        
        ###MANUALY COPY LATAN APPLICATIONS IN WORKBENCH

  
else:
    print("Release is Not Ready")



