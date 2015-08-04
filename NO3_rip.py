import sys, os
from xlrd import *
from xlwt import *

# Rips all NO3 dilution data by watershed from the DEP Excel model, and outputs an excel sheet
# with the new data. Created because the current model only allows for the selection of individual
# municipalities. This script does it for the whole state. 

def main(modelFile, outputDirectory, inPopDens):

    popDensity = float(inPopDens)

    # creating the output file path with pop. density
    outputFile = outputDirectory + "\\NJ_NO3_values_%s.xls"%(str(popDensity))

    hucDict = {}

    # constants / standards
    targetNO3 = 2.0
    loadingRate = 10.0
    calcConstant = 4.42

    # column indexes
    rechargeCol = 48
    huc11Col = 47

    sheet = open_workbook(modelFile).sheet_by_index(1)

    # populating the dictionary
    for row in range(2, 151):
        avgRecharge = sheet.cell(row, rechargeCol).value
        huc11 = str(sheet.cell(row, huc11Col).value)
        sepDens = (calcConstant * popDensity * loadingRate) / (avgRecharge * targetNO3)
        hucDict[huc11] = (sepDens, avgRecharge)

    wb = Workbook()
    writerSheet = wb.add_sheet("NO3_vals_%s_popdens"%(str(popDensity)))
    writerSheet.write(0, 0, "HUC11")
    writerSheet.write(0, 1, "SEPDENS")
    writerSheet.write(0, 2, "AVGRECHRG")

    # writing the values to the new table
    row_index = 1
    for key, value in hucDict.iteritems():
        sepdens = value[0]
        avgRecharge = value[1]
        writerSheet.write(row_index, 0, key)
        writerSheet.write(row_index, 1, sepdens)
        writerSheet.write(row_index, 2, avgRecharge)
        row_index += 1

    wb.save(outputFile)
    os.startfile(outputFile)

# main method
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    
    
