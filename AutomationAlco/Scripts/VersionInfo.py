import ConfigParser, os


Config = ConfigParser.ConfigParser()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def getConfig():

    script_path = os.path.dirname(__file__)
    #print script_path
    #script_dir = os.path.split(script_path)[0]
    #print script_dir

    Config.read(script_path + "\\config.ini")
    BuildVer = ConfigSectionMap("SectionOne")['version']

    #print ConfigSectionMap("MSHHL7Data")
    
    EncodingChars = ConfigSectionMap("MSHHL7Data")['encodingchars']
    SendingApplication = ConfigSectionMap("MSHHL7Data")['sendingapplication']
    SendingFacility = ConfigSectionMap("MSHHL7Data")['sendingfacility']
    ReceivingAppln = ConfigSectionMap("MSHHL7Data")['receivingappln']
    ReceivingFacility = ConfigSectionMap("MSHHL7Data")['receivingfacility']
    AdtMessageType1 = ConfigSectionMap("MSHHL7Data")['adtmessagetype1']
    ProcessingID = ConfigSectionMap("MSHHL7Data")['processingid']
    VersionID = ConfigSectionMap("MSHHL7Data")['versionid']
    AdtMessageType2 = ConfigSectionMap("MSHHL7Data")['adtmessagetype2']

    HospitalService = ConfigSectionMap("PVHL7Data")['hospitalservice']
    AdmitSource = ConfigSectionMap("PVHL7Data")['admitsource']
    AmbulatoryStatus = ConfigSectionMap("PVHL7Data")['ambulatorystatus']
    eventTypeCode = ConfigSectionMap("EVNHL7Data")['eventtypecode']
    PatientClass = ConfigSectionMap("PVHL7Data")['patientclass']
    OmgMessageType1 = ConfigSectionMap("MSHHL7Data")['omgmessagetype1']
    OmgMessageType2 = ConfigSectionMap("MSHHL7Data")['omgmessagetype2']
    SiuMessageType1 = ConfigSectionMap("MSHHL7Data")['siumessagetype1']
    SiuMessageType2 = ConfigSectionMap("MSHHL7Data")['siumessagetype2']
    OruProcessingID = ConfigSectionMap("MSHHL7Data")['oruprocessingid']
    OruSendingApplication = ConfigSectionMap("MSHHL7Data")['orusendingapplication']
    OruSendingFacility = ConfigSectionMap("MSHHL7Data")['orusendingfacility']
    OruReceivingAppln = ConfigSectionMap("MSHHL7Data")['orureceivingappln']
    OruReceivingFacility = ConfigSectionMap("MSHHL7Data")['orureceivingfacility']
    OruMessageType1 = ConfigSectionMap("MSHHL7Data")['orumessagetype1']
    OruMessageType2 = ConfigSectionMap("MSHHL7Data")['orumessagetype2']
    
    print [BuildVer, EncodingChars, SendingApplication, SendingFacility, ReceivingAppln, ReceivingFacility, AdtMessageType1, ProcessingID, VersionID,
           HospitalService, AdmitSource, AmbulatoryStatus, eventTypeCode, PatientClass,OmgMessageType1,SiuMessageType1,OruProcessingID,OruSendingApplication,
           OruSendingFacility,OruReceivingAppln,OruReceivingFacility,OruMessageType1,AdtMessageType2,OmgMessageType2,SiuMessageType2,OruMessageType2]
    return [BuildVer, EncodingChars, SendingApplication, SendingFacility, ReceivingAppln, ReceivingFacility,AdtMessageType1, ProcessingID, VersionID,
            HospitalService, AdmitSource, AmbulatoryStatus, eventTypeCode, PatientClass,OmgMessageType1,SiuMessageType1,OruProcessingID,OruSendingApplication,
           OruSendingFacility,OruReceivingAppln,OruReceivingFacility,OruMessageType1,AdtMessageType2,OmgMessageType2,SiuMessageType2,OruMessageType2]
    


if __name__ == '__main__':
	#unittest.main()
	getConfig()

    
