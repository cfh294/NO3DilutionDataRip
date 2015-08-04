#!/usr/bin/env python
# Code: Connor Hornibrook, 04 August 2015
#
# Rips all NO3 dilution data by watershed from the DEP Excel model, and outputs an excel sheet
# with the new data. Created because the current model only allows for the selection of individual
# municipalities. This script does it for the whole state. The file for the DEP model is located
# within this git repository as "DEP_Nitrate_Model". The result of this module can be easily joined
# watershed GIS data on the HUC11 field. The DEP model, and therefore this tool, does not calculate
# values for either Hudson or Essex County. This tool is used on the command
# line. 

import sys, os
from xlrd import *
from xlwt import *
                                        # Standard values were used for all
                                        # of our project's calculations. 3.14
                                        # was our standard population density
                                        # but the DEP's model default was 3.0
        #DEP model                              #std.: 2.0    #std.: 10.0
def main(modelFile, outputDirectory, inPopDens, inTargetNO3, inLoadingRate):

    popDensity = float(inPopDens)
    targetNO3 = float(inTargetNO3)
    loadingRate = float(inLoadingRate)

    # creating the output file path with pop. density
    outputFile = outputDirectory + "\\NJ_NO3_values_%s.xls"%(str(popDensity))

    hucDict = {}

    # constant - taken from the model calculations
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

    # writing headers
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
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    
    
