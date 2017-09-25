import os
from xlrd import open_workbook
from VersionInfo import getVersionInfo
ver = getVersionInfo()

def readHL7Input():
    script_path = os.path.dirname(__file__)
    print script_path
    script_dir = os.path.split(script_path)[0]
    print script_dir
    #projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.20' + '\\' + 'V1.20' + '\\' + 'Alcon' + '\\' + 'output'  + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
    projDir = os.path.join(script_dir, 'SRC' + '\\' + ver + '\\' + ver + '\\' + 'Alcon' + '\\' + 'output'  + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
    
    print projDir

    #wb = open_workbook('D:\\MedicalDevices\\Alcon\\Testing\\FinalTestScripts\\HL7InputData.xlsx')
    wb = open_workbook(script_path + '\\HL7InputData.xlsx')
    for s in wb.sheets():
        #print 'Sheet:',s.name
        values = []
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value  = (s.cell(row,col).value)
                try : value = str(int(value))
                except : pass
                col_value.append(value)
            values.append(col_value)
    #print values
    return values
    #for val in values[1:]:
        #print val


if __name__ == '__main__':
    readHL7Input()
    