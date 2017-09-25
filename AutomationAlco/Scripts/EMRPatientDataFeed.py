from pywinauto.application import Application
#from ReadExcelData import readFromExcel

#app = Application().start(r"D:\MedicalDevices\Alcon\Testing\EMRSimulator\PatientDataEMR\EMR_Patient_Data.exe")
#app = Application().connect(path = r"D:\MedicalDevices\Alcon\Testing\EMRSimulator\PatientDataEMR\EMR_Patient_Data.exe")

def PatientRegistration(data, app):
    #DataFeederList = readFromExcel()
    #print DataFeederList
    print app.Registration.PrintControlIdentifiers()
    #for data in DataFeederList[1:]:

    #print app.EMP_Landing_Page.PrintControlIdentifiers()

    print data[0]
    app.Registration.Edit7.TypeKeys(str(data[0]))
    print data[1]
    app.Registration.Edit8.TypeKeys(str(data[1]))
    print data[2]
    app.Registration.Edit9.TypeKeys(str(data[2]))
    print data[3]
    app.Registration.ComboBox.Select(int(data[3]))
    print data[5]
    app.Registration.Edit5.TypeKeys(int(data[5]))
    print data[6]
    app.Registration.Edit4.TypeKeys(int(data[6]))
    print data[7]
    app.Registration.Edit6.TypeKeys(str(data[7]))
    print data[8]
    app.Registration.Edit2.TypeKeys(str(data[8]))
    print data[9]
    app.Registration.Edit1.TypeKeys(int(data[9]))
    app.Registration.Patient.Wait('ready').Click()

    #main_window = app.Registration.Patient.top_window_()
    #main_window.PopupWindow().OK.Click()

    #print app.Registration.Patient.OK.PrintControlIdentifiers()
    app.Registration.Patient.GetFocus().Click()
    app.Registration.GetFocus().Close()


if __name__ == '__main__':
    PatientRegistration()




