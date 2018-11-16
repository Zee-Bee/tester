import arcpy, datetime, time
from arcpy import env
from arcpy import da



sgid10 = r'Database Connections\dc_agrc@SGID10@gdb10.agrc.utah.gov.sde'
sgid10_GEO = r'C:\ZBECK\BlueStakes\stagingBS.gdb\SGID10_GEOGRAPHIC'
stageDB = r'C:\ZBECK\BlueStakes\stagingBS.gdb'
schemaDB = r'C:\ZBECK\BlueStakes\schemaBS.gdb'
outLoc = r'C:\ZBECK\BlueStakes\outBlueStakes'


env.workspace = sgid10

fipsNum = ['49001', '49003', '49005', '49007', '49009', '49011', '49013', '49015', '49017', '49019', '49021', \
           '49023', '49025', '49027', '49029', '49031', '49033', '49035', '49037', '49039', '49041', '49043', '49045', \
           '49047', '49049', '49051', '49053', '49055', '49057']

fipsDict = {'Beaver': '49001', 'BoxElder': '49003', 'Cache': '49005', 'Carbon': '49007', 'Daggett': '49009', \
            'Davis': '49011', 'Duchesne': '49013', 'Emery': '49015', 'Garfield': '49017', 'Grand': '49019', \
            'Iron': '49021', 'Juab': '49023', 'Kane': '49025', 'Millard': '49027', 'Morgan': '49029', \
            'Piute': '49031', 'Rich': '49033', 'SaltLake': '49035', 'SanJuan': '49037', 'Sanpete': '49039', \
            'Sevier': '49041', 'Summit': '49043', 'Tooele': '49045', 'Uintah': '49047', 'Utah': '49049', \
            'Wasatch': '49051', 'Washington': '49053', 'Wayne': '49055', 'Weber': '49057'}

typeList = ('ALY', 'AVE', 'BLVD', 'CIR', 'CT', 'CV', 'DR', 'EST', 'ESTS', 'EXPY', 'FWY', 'HWY', 'HOLW', \
            'JCT', 'LN', 'LOOP', 'PKWY', 'PL', 'PLZ', 'PT', 'RAMP', 'RNCH', 'RD', 'RTE', 'RUN', 'RW', 'SQ', \
            'ST', 'TER', 'TRL', 'WAY', 'HTS', 'COR')

typeList2 = ('ALLEY', 'AVENUE', 'BOULEVARD', 'CIRCLE', 'COURT', 'COVE', 'DRIVE', 'ESTATE', 'ESTATES', 'EXPRESSWAY', \
             'FREEWAY', 'HEIGHTS', 'HIGHWAY', 'HOLLOW', 'JUNCTION', 'LANE', 'LOOP', 'PARKWAY', 'PLACE', 'PLAZA', \
             'POINT', 'RAMP', 'RANCH', 'ROAD', 'ROUTE', 'RUN', 'ROW', 'SQUARE', 'STREET', 'TERRACE', 'TRAIL', 'WAY', 'CORNER')

typeDict = {'ALLEY': 'ALY', 'AVENUE': 'AVE', 'BOULEVARD': 'BLVD', 'CIRCLE': 'CIR', 'COURT': 'CT', 'COVE': 'CV', \
            'DRIVE': 'DR', 'ESTATE': 'EST', 'ESTATES': 'ESTS', 'EXPRESSWAY': 'EXPY', 'FREEWAY': 'FWY', 'HIGHWAY': 'HWY', \
            'HOLLOW': 'HOLW', 'JUNCTION': 'JCT', 'LANE': 'LN', 'LOOP': 'LOOP', 'PARKWAY': 'PKWY', 'PLACE': 'PL', \
            'PLAZA': 'PLZ', 'POINT': 'PT', 'RAMP': 'RAMP', 'RANCH': 'RNCH', 'ROAD': 'RD', 'ROUTE': 'RTE', 'RUN': 'RUN', \
            'ROW': 'RW', 'SQUARE': 'SQ', 'STREET': 'ST', 'TERRACE': 'TER', 'TRAIL': 'TRL', 'WAY': 'WAY', 'HEIGHTS': 'HTS', \
            'CORNER': 'COR'}

dirList = ('N', 'S', 'E', 'W')

dirList2 = ('NORTH', 'SOUTH', 'EAST', 'WEST')

dirDict = {'NORTH': 'N', 'SOUTH': 'S', 'EAST': 'E', 'WEST': 'W'}

if not arcpy.Exists(stageDB):
    arcpy.CreateFileGDB_management('C:\ZBECK\BlueStakes', 'stagingBS.gdb')



#-------------------------------------------------------------------------------------------------------------------------------------------

def municipalities():

    print 'Starting Municipalities  ' + str(datetime.datetime.now())

    muni = sgid10_GEO + '\\Municipalities'
    muniBS = stageDB + '\\TGR_StWide_plc00'
    clpCnty = 'SGID10.BOUNDARIES.Counties'

    #---Check for Municipalites in SGID10_GEOGRAPHIC staging area
    if arcpy.Exists(muni):
        arcpy.Delete_management(muni)
        arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Municipalities', muni)
    else:
        arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Municipalities', muni)

    #---Check for statewide municipalities BlueStakes schema
    if not arcpy.Exists(muniBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCplc00_schema', muniBS)
    else:
        arcpy.DeleteFeatures_management(muniBS)

    srcFlds = ['NAME', 'SHAPE@']
    tarFlds = ['NAME', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(muni, srcFlds)
    tarRows = arcpy.da.InsertCursor(muniBS, tarFlds)

    for srcRow in srcRows:

        NAME = srcRow[0]
        shp = srcRow[1]

        tarRows.insertRow((NAME, shp))

    del tarRows


    #---Clip by county-------------------------------------------
    clpFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
    clpRows = arcpy.da.SearchCursor(clpCnty, clpFlds)

    for row in clpRows:
        clpFeat = row[2]
        if arcpy.Exists(outLoc + '\\TGR' + row[1] + '\\TGR' + row[1] + 'plc00.shp'):
            arcpy.Delete_management(outLoc + '\\TGR' + row[1] + '\\TGR' + row[1] + 'plc00.shp')
            arcpy.Clip_analysis(muniBS, clpFeat, outLoc + '\\TGR' + row[1] + '\\TGR' + row[1] + 'plc00.shp')
        else:
            arcpy.Clip_analysis(muniBS, clpFeat, outLoc + '\\TGR' + row[1] + '\\TGR' + row[1] + 'plc00.shp')


    print 'Done Translating Municipalities  ' + str(datetime.datetime.now())


municipalities();


