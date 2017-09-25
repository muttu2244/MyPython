from xlrd import open_workbook

def readUIInput(fileName):
    
    wb = open_workbook(fileName)
    for s in wb.sheets():
        #print 'Sheet:',s.name
        values = []
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value  = (s.cell(row,col).value)
                #print value
                #print type(value)
                try : value = str(int(value))
                except : pass
                col_value.append(value)
            values.append(col_value)
    #print values
    return values[1:]
    #for val in values[1:]:
        #print val


if __name__ == '__main__':
    readUIInput()
    