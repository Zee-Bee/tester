import arcpy, datetime, time
from arcpy import env
from arcpy import da

#sgid10 = r'C:\ZBECK\BlueStakes\stagingBS.gdb\SGID10_GEOGRAPHIC'
sgid10 = r'Database Connections\dc_agrc@SGID10@gdb10.agrc.utah.gov.sde'
#sgid10 = r'C:\ZBECK\BlueStakes\testDB.gdb'
sgid10_GEO = r'C:\ZBECK\BlueStakes\stagingBS.gdb\SGID10_GEOGRAPHIC'
stageDB = r'C:\ZBECK\BlueStakes\stagingBS.gdb'
schemaDB = r'C:\ZBECK\BlueStakes\schemaBS.gdb'
outLoc = r'C:\ZBECK\BlueStakes\outBlueStakes'
#clpCnty = r'Database Connections\ac_agrc@SGID10@gdb10.agrc.utah.gov.sde\SGID10.BOUNDARIES.Counties'

env.workspace = sgid10
arcpy.env.overwriteOutput = True

fc = 'SGID10.SOCIETY.CorrectionalFacilities'

flds = ['NAME']

rows = arcpy.da.SearchCursor(fc, flds)

for row in rows:
    if len(row[0]) > 79:
        print row[0]

##def airstrips():
##
##    print 'Starting Airstrips  ' + str(datetime.datetime.now())
##
##    airstrips = sgid10_GEO + '\\Airports'
##    airstripsBS = stageDB + '\\TGR_StWide_lkD'
##    clpCnty = 'SGID10.BOUNDARIES.Counties'
##
##    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.Airports', airstrips)
##
##    #---Check for statewide airports BlueStakes schema
##    if not arcpy.Exists(airstripsBS):
##        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCClkD_schema', airstripsBS)
##    else:
##        arcpy.DeleteFeatures_management(airstripsBS)
##
##    srcFlds = ['FAC_TYPE', 'FULLNAME', 'SHAPE@']
##    tarFlds = ['FENAME', 'CFCC2', 'SHAPE@']
##    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
##
##    srcRows = arcpy.da.SearchCursor(airstrips, srcFlds)
##    tarRows = arcpy.da.InsertCursor(airstripsBS, tarFlds)
##
##    for srcRow in srcRows:
##
##        if srcRow[0] == 'AIRPORT':
##            if srcRow[0].find('AIRFIELD') != -1:
##                FENAME = srcRow[1].replace('MUNI', 'MUNICIPAL')
##            elif srcRow[0].find('BASE') != -1:
##                FENAME = srcRow[1]
##            else:
##                FENAME = srcRow[1].replace('MUNI', 'MUNICIPAL') + ' ' + srcRow[0]
##        else:
##            FENAME = srcRow[1]
##
##        CFCC2 = 'D5'
##
##        shp = srcRow[2]
##
##        tarRows.insertRow((FENAME, CFCC2, shp))
##
##    del tarRows
##
##    clip(airstripsBS, 'lkD.shp');
##
##
##def clip(clipMe, outNameSuffix):
##
##    clpCnty = sgid10_GEO + '\\Counties'
##
##    arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Counties', clpCnty)
##
##    clpFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
##    clpRows = arcpy.da.SearchCursor(clpCnty, clpFlds)
##    fldrPrefix = '\\TGR'
##
##    for row in clpRows:
##        clpFeat = row[2]
##        if arcpy.Exists(outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix):
##            arcpy.Delete_management(outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix)
##
##            #----Delete shapefiles with no features----
##            clp = arcpy.Clip_analysis(clipMe, clpFeat, outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix)
##            clpCount = int(arcpy.GetCount_management(clp).getOutput(0))
##            if clpCount < 1:
##                arcpy.Delete_management(clp)
##
##            flds = [fld.name for fld in arcpy.ListFields(clp)]
##            if fld.name == 'SHAPE_Leng' or fld.name == 'Shape_Leng':
##                arcpy.DeleteField_management(clp, 'SHAPE_Leng')
##
##        else:
##            #----Delete shapefiles with no features----
##            clp = arcpy.Clip_analysis(clipMe, clpFeat, outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + 'lkD.shp')
##            clpCount = int(arcpy.GetCount_management(clp).getOutput(0))
##            if clpCount < 1:
##                arcpy.Delete_management(clp)
##
##            flds = [fld.name for fld in arcpy.ListFields(clp)]
##            if fld.name == 'SHAPE_Leng' or fld.name == 'Shape_Leng':
##                arcpy.DeleteField_management(clp, 'SHAPE_Leng')
##
##
##
##airstrips();


