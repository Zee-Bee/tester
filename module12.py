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

def parcels():

    print 'Starting Parcels  ' + str(datetime.datetime.now())

#-Check for parcels in staging DB, add it if missing, delete features if they exist
##    for fips in fipsNum:
##        parcelFC = stageDB + '\\' + 'par' + fips
##
##        if not arcpy.Exists(parcelFC):
##            arcpy.CopyFeatures_management(schemaDB + '\\parSSCCC_schema', stageDB + '\\par' + fips)
##            print 'Copied par' + fips + ' to staging GDB'
##        else:
##            arcpy.DeleteFeatures_management(parcelFC)
##            print 'Deleted existing features in ' + parcelFC

    fc = r'C:\ZBECK\BlueStakes\testDB.gdb\Parcels_Garfield'
    fcBS = r'C:\ZBECK\BlueStakes\stagingBS.gdb\par49001'

    srcFlds = ['PARCEL_ID', 'PARCEL_ADD', 'SHAPE@']
    tarFlds = ['ADDR_NUMB', 'ADDR_FULL', 'FEDIRP', 'FENAME', 'FETYPE', 'FEDIRS', 'OWNER', 'SHAPE@']


##    for fc in arcpy.ListFeatureClasses():
##        #if fc[:23][-7:] == 'Parcels':      #get SDE parcels
##        if fc.split('_')[0] == 'Parcels':
##
##            cnty = fc.split('_')[1]

##    tarRows = arcpy.da.InsertCursor(stageDB + '\\par' + fipsDict[cnty], tarFlds)
    tarRows = arcpy.da.InsertCursor(fcBS, tarFlds)
    srcRows = arcpy.da.SearchCursor(fc, srcFlds)

    for srcRow in srcRows:

        srcPar_ParID = srcRow[0]
        addFull = srcRow[1]
        shp = srcRow[2]

        if addFull != None and addFull.strip() != '':

        #--Address Number-----------------------------------------
            if addFull.split(' ')[0].isdigit():
                addNum = addFull.split(' ')[0]
            else:
                addNum = ''

        #--Prefix Direction---------------------------------------
            preDirs = addFull.split(' ')[1]

            if preDirs.upper() in dirList:
                preDir = preDirs.upper()

            if preDirs.upper() in dirList2:
                preDir = dirDict[preDirs.upper()]

            else:
                preDirs = ''

        #--Sufix Direction----------------------------------------
            sufDirs = addFull.split(' ')[-1]

            if sufDirs.upper() in dirList:
                sufDir = sufDirs.upper()

            if sufDirs.upper() in dirList2:
                sufDir = dirDict[sufDirs.upper()]

            else:
                sufDirs = ''


        #--Street Type--------------------------------------------
            sTypes = addFull.split(' ')[-1]

            if sTypes.upper() in typeList:
                sType = sTypes.upper()

            if sTypes.upper() in typeList2:
                sType = typeDict[sTypes.upper()]

            else:
                sType = ''

        #---Street Name-------------------------------------------

            houseNumber = 'houseNumber'
            preDirection = 'preDirection'
            sName = 'sName'
            streetNameBegun = 'streetNameBegun'
            streetNameEnded = 'streetNameEnded'

            streetName = ''

            if streetName != None:
                def checkWord(word, state):
                    global streetName
                    if state == houseNumber:
                        return preDirection
                    elif state == preDirection:
                        if word in dirList or word in dirList2:
                            return sName
                        else:
                            streetName = streetName + word
                            return streetNameBegun
                    elif state == sName:
                        streetName = word
                        return streetNameBegun
                    elif state == streetNameBegun:
                        if word in typeList or word in dirList or word in typeList2 or word in dirList2:
                            return streetNameEnded
                        else:
                            streetName = streetName + ' ' + word
                            return streetNameBegun
                    elif state == streetNameEnded:
                        return streetNameEnded


                def findStName(addFull):
                    global streetName
                    streetName = ''
                    state = houseNumber
                    for word in addFull.strip().split(' '):
                        state = checkWord(word, state)

                    return streetName

##            for add in addList:
##                print findStName(add)

        else:
            addNum = ''
            preDir = ''
            sType = ''
            sufDir = ''
            srcPar_ParID = ''

        tarRows.insertRow((addNum, addFull, preDir, findStName(srcRow[1]), sType, 'S', srcPar_ParID, shp))


    del tarRows
    del srcRows

#    print cnty + ' par' + fipsDict[cnty] + ' Done'



    print 'Done Parcels  ' + str(datetime.datetime.now())



#-------------------------------------------------------------------------------------------------------------------------------------------

def addressPoints():

    print 'Starting Address Points  ' + str(datetime.datetime.now())

    addPts = sgid10_GEO + '\\AddressPoints'
    addPtsBS = stageDB + '\\adr_StWide'
    clpCnty = 'SGID10.BOUNDARIES.Counties'

    #---Check for Address Points in SGID10_GEOGRAPHIC staging area
    if arcpy.Exists(addPts):
        arcpy.Delete_management(addPts)
        arcpy.CopyFeatures_management(r'Database Connections\DC_Location@SGID10@gdb10.agrc.utah.gov.sde\SGID10.LOCATION.AddressPoints', addPts)
    else:
        arcpy.CopyFeatures_management(r'Database Connections\DC_Location@SGID10@gdb10.agrc.utah.gov.sde\SGID10.LOCATION.AddressPoints', addPts)

    #---Check for statewide Address Points in BlueStakes schema
    if not arcpy.Exists(addPtsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\adrSSCCC_schema', addPtsBS)
    else:
        arcpy.DeleteFeatures_management(addPtsBS)

    srcFlds = ['ADDLABEL', 'ADDNBR', 'PRE_DIR', 'STREETNAME', 'STREETTYPE', 'SUF_DIR', 'SHAPE@']
    tarFlds = ['ADDR_NUMB', 'ADDR_FULL', 'FEDIRP', 'FENAME', 'FETYPE', 'FEDIRS', 'OWNER', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(addPts, srcFlds)
    tarRows = arcpy.da.InsertCursor(addPtsBS, tarFlds)

    for srcRow in srcRows:

        if srcRow[1] != None:
            ADDR_NUMB = srcRow[1]
        else:
            ADDR_NUMB = ''

        if srcRow[0] != None:
            ADDR_FULL = srcRow[0]
        else:
            ADDR_FULL = ''

        if srcRow[2] != None:
            FEDIRP = srcRow[2]
        else:
            FEDIRP = ''

        if srcRow[3] != None:
            FENAME = srcRow[3]
        else:
            FENAME = ''

        if srcRow[4] != None:
            FETYPE = srcRow[4]
        else:
            FETYPE = ''

        if srcRow[5] != None:
            FEDIRS = srcRow[5]
        else:
            FEDIRS = ''

        OWNER = ''

        shp = srcRow[6]

        tarRows.insertRow((ADDR_NUMB, ADDR_FULL, FEDIRP, FENAME, FETYPE, FEDIRS, OWNER, shp))

    del tarRows


    #---Copy State wide address points to Bluestakes root---------------
    arcpy.CopyFeatures_management(addPtsBS, outLoc + '\\adr_StWide.shp')


    #---Clip by county-------------------------------------------
    clpFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
    clpRows = arcpy.da.SearchCursor(clpCnty, clpFlds)

    for row in clpRows:
        clpFeat = row[2]

        #----Delete shapefiles with no features----
        clp = arcpy.Clip_analysis(addPtsBS, clpFeat, outLoc + '\\TGR' + row[1] + '\\adr' + row[1] + '.shp')
        clpCount = int(arcpy.GetCount_management(clp).getOutput(0))

        if clpCount < 1:
            arcpy.Delete_management(clp)


    print 'Done Translating Address Points  ' + str(datetime.datetime.now())


#-------------------------------------------------------------------------------------------------------------------------------------------

def roads():

    print 'Starting Roads  ' + str(datetime.datetime.now())

##    for fips in fipsNum:
##        streetFC = stageDB + '\\TGR' + fips + 'lkA'
##
##        if not arcpy.Exists(streetFC):
##            arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCLKA_schema', stageDB + '\\TGR' + fips + 'lkA')
##            print 'Copied TGR' + fips + 'lkA to staging GDB'
##        else:
##            arcpy.DeleteFeatures_management(streetFC)
##            print 'Deleted existing features in ' + streetFC


    srcFlds = ['CARTOCODE', 'PREDIR', 'FULLNAME', 'STREETTYPE', 'SUFDIR', 'L_F_ADD', 'L_T_ADD', 'R_F_ADD', 'R_T_ADD', 'ALIAS1', \
               'ALIAS2', 'ACSALIAS', 'ACSNAME', 'COFIPS', 'HWYNAME', 'MODIFYDATE', 'ADDR_SYS', 'STREETNAME', 'SHAPE@']

    tarFlds = ['FEDIRP', 'FENAME', 'FETYPE', 'FEDIRS', 'CFCC', 'FRADDL', 'TOADDL', 'FRADDR', 'TOADDR', 'CFCC1', 'CFCC2', 'FULLNAME', \
               'HASALT', 'ISALT', 'S_FIPS', 'AGRC_MDATE', 'ADDRESS_SY', 'SHAPE@']

    #rdFC = 'Roads'
    rdFC = 'SLCRoads'
    #tarRds = stageDB + '\\TGR_StWide_lkA'
    tarRds = stageDB + '\\TGR49035lkA'

##    #----Remove empty spaces from roads----------------------------------------------------------------------------
##    with arcpy.da.UpdateCursor(rdFC, srcFlds) as rows:
##        for row in rows:
##            for fld in srcFlds:
##                fldX = srcFlds.index(fld)
##
##                if row[fldX] == ' ':
##                    row[fldX] = None
##
##                rows.updateRow(row)
##
##    del rows

    srcRows = arcpy.da.SearchCursor(rdFC, srcFlds)
    tarRows = arcpy.da.InsertCursor(tarRds, tarFlds)

    for srcRow in srcRows:
        #----Prefix Direction----
        if srcRow[1] == None:
            FEDIRP = None
        else:
            FEDIRP = srcRow[1]

        #----Root and Full Street Name----
        if srcRow[2] != None:

            if FEDIRP != None:
                FULLNAME = (FEDIRP + ' ' + srcRow[2]).title()
            else:
                FULLNAME = srcRow[2].title()

        else:
            FULLNAME = ''

        if srcRow[17] != None:
            FENAME = srcRow[17].replace('HIGHWAY', 'HWY').title()
        else:
            FENAME = ''


        #----Street Type----
        if srcRow[3] != None:
            FETYPE = srcRow[3].title()
        else:
            FETYPE = ''

        #----Sufix Direction----
        if srcRow[4] != None:
            FEDIRS = srcRow[4]
        else:
            FEDIRS = ''

        #----CFCC----
        if srcRow[0] != None:
            if srcRow[0] == '1':
                CFCC = 'A15'
            if srcRow[0] == '2':
                CFCC = 'A25'
            if srcRow[0] == '3':
                CFCC = 'A21'
            if srcRow[0] == '4':
                CFCC = 'A35'
            if srcRow[0] == '5':
                CFCC = 'A31'
            if srcRow[0] == '6':
                CFCC = 'A41'
            if srcRow[0] == '7':
                CFCC = 'A20'
            if srcRow[0] == '8':
                CFCC = 'A31'
            if srcRow[0] == '9':
                CFCC = 'A41'
            if srcRow[0] == '10':
                CFCC = 'A41'
            if srcRow[0] == '11':
                CFCC = 'A41'
            if srcRow[0] == '12':
                CFCC = 'A41'

            CFCC1 = 'A'
            CFCC2 = CFCC[:2]

        #----From Address Left----
        if srcRow[5] != None:
            FRADDL = str(srcRow[5]).split('.')[0]
        else:
            FRADDL = 0

        #----To Address Left----
        if srcRow[6] != None:
            TOADDL = str(srcRow[6]).split('.')[0]
        else:
            TOADDL = 0

        #----From Address Right----
        if srcRow[7] != None:
            FRADDR = str(srcRow[7]).split('.')[0]
        else:
            FRADDR = 0

        #----To Address Right----
        if srcRow[8] != None:
            TOADDR = str(srcRow[8]).split('.')[0]
        else:
            TOADDR = 0

        #----FIPS----
        if srcRow[13] != None:
            S_FIPS = srcRow[13]
        else:
            S_FIPS = ''

        #----AGRC M Date----
        if srcRow[15] != None:
            AGRC_MDATE = srcRow[15]
        else:
            AGRC_MDATE = '1/1/1000'

        #----Address System----
        if srcRow[16] != None:
            ADDRESS_SY = srcRow[16]
        else:
            ADDRESS_SY = ''


        shp = srcRow[18]


        #----Has Alt Name----
        if srcRow[9] != None:
            HASALT = 1
            ISALT = 0
        elif srcRow[12] != None:
            HASALT = 1
            ISALT = 0
        else:
            HASALT = 0
            ISALT = 0

        tarRows.insertRow((FEDIRP, FENAME, FETYPE, FEDIRS, CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, HASALT, \
                           ISALT, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))


        #----Add Duplicate Interstates----
        if srcRow[0] == '1':

            usFENAME = srcRow[14]

            if FEDIRP != None:
                FULLNAME = FEDIRP + ' ' + usFENAME
            else:
                FULLNAME = usFENAME

            tarRows.insertRow((FEDIRP, usFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                               0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))


        #----Add Duplicate US Highways----
        if srcRow[0] == '2' or srcRow[0] == '3':

            usFENAME = srcRow[14]

            if FEDIRP != None:
                FULLNAME = FEDIRP + ' ' + usFENAME
            else:
                FULLNAME = usFENAME

            tarRows.insertRow((FEDIRP, usFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                               0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))

            if srcRow[14].split()[0] == 'US':

                hwyFENAME = 'Hwy ' + srcRow[14].split()[1]

                if FEDIRP != None:
                    FULLNAME = FEDIRP + ' ' + hwyFENAME
                else:
                    FULLNAME = hwyFENAME

                tarRows.insertRow((FEDIRP, hwyFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                                   0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))


        #----Add Duplicate State Highways----
        if srcRow[0] == '4' or srcRow[0] == '5' or srcRow[0] == '6':

            if srcRow[14] != None:
                srFENAME = srcRow[14]

                if FEDIRP != None:
                    FULLNAME = FEDIRP + ' ' + srFENAME
                else:
                    FULLNAME = srFENAME

                tarRows.insertRow((FEDIRP, srFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                                   0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))

                if srcRow[14].split()[0] == 'SR':
                    if srcRow[14].split()[1] != '201':

                        hwyFENAME = 'Hwy ' + srcRow[14].split()[1]

                        if FEDIRP != None:
                            FULLNAME = FEDIRP + ' ' + hwyFENAME
                        else:
                            FULLNAME = hwyFENAME

                        tarRows.insertRow((FEDIRP, hwyFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                                           0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))


        #----Add Duplicate Alias and ACSAlias----
        if srcRow[9] != None:
            if srcRow[9] != '':
                if srcRow[9][:7] != 'HIGHWAY':
                    alsFENAME = srcRow[9]
                    if FEDIRP != None:
                        FULLNAME = FEDIRP + ' ' + alsFENAME + ' ' + FEDIRS
                    else:
                        alsFENAME + ' ' + FEDIRS
                    tarRows.insertRow((FEDIRP, alsFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, \
                                       FULLNAME, 0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))

        if srcRow[12] != None:
            acsFENAME = srcRow[12]
            if FEDIRP != None:
                FULLNAME = FEDIRP + ' ' + acsFENAME + ' ' + FEDIRS
            else:
                FULLNAME = acsFENAME + ' ' + FEDIRS
            tarRows.insertRow((FEDIRP, acsFENAME, '', '', CFCC, FRADDL, TOADDL, FRADDR, TOADDR, CFCC1, CFCC2, FULLNAME, \
                               0, 1, S_FIPS, AGRC_MDATE, ADDRESS_SY, shp))


    del tarRows
    del srcRows

    #---Copy Roads to Blues Stakes root level-----------------
#    arcpy.CopyFeatures_management(tarRds, outLoc + '\\TGR_StWide_lka.shp')


    #---Clip Blue Stakes Roads-----------------------------------------------------------
    clip(tarRds, 'lkA.shp');

    print 'Done Translating Roads  ' + str(datetime.datetime.now())


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


    #---Copy Municipalities to Blues Stakes root level
    arcpy.CopyFeatures_management(muniBS, outLoc + '\\TGR_StWide_plc00.shp')


    #---Clip Blue Stakes Municipalities-----------------------------------------------------------
    clip(muniBS, 'plc00.shp');


    print 'Done Translating Municipalities  ' + str(datetime.datetime.now())

#-------------------------------------------------------------------------------------------------------------------------------------------

def mileposts():

    print 'Starting Mileposts  ' + str(datetime.datetime.now())

    arcpy.env.overwriteOutput = True

    milePosts = sgid10_GEO + '\\UDOTMilePosts'
    exits = sgid10_GEO + '\\Roads_FreewayExits'
    milePostsBS = stageDB + '\\Hwy_MPM'

    #---Copy new Exits and Mileposts to Staging DB
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.Roads_FreewayExits', exits)
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.UDOTMileposts', milePosts)
    print 'Copied SGID10.TRANSPORTATION.Roads_FreewayExits to staging DB'
    print 'Copied SGID10.TRANSPORTATION.UDOTMileposts to staging DB'


    #---Check for Mileposts BlueStakes schema
    if not arcpy.Exists(milePostsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\Hwy_MPM', milePostsBS)
    else:
        arcpy.DeleteFeatures_management(milePostsBS)


    srcMP_Flds = ['RT_NAME', 'MILEPOST', 'CARTO', 'SHAPE@']
    srcEX_Flds = ['EXITNAME', 'SHAPE@']
    tarFlds = ['Type', 'Label_Name', 'SHAPE@']


    srcMP_Rows = arcpy.da.SearchCursor(milePosts, srcMP_Flds)
    srcEX_Rows = arcpy.da.SearchCursor(exits, srcEX_Flds)
    tarRows = arcpy.da.InsertCursor(milePostsBS, tarFlds)

    #----Add Milepost Records--------------------------------------------------------
    for srcMP_Row in srcMP_Rows:

        Type = 'mpm'

        hwyDig1 = srcMP_Row[0][3:4]
        hwyDig2 = srcMP_Row[0][2:4]
        hwyDig3 = srcMP_Row[0][1:4]

        if srcMP_Row[2] == '1':
            Label_Name = 'I-{0} milepost {1}'.format(hwyDig2, srcMP_Row[1])
        else:
            if srcMP_Row[0][2] == '0':
                Label_Name = 'Hwy {0} milepost {1}'.format(hwyDig1, srcMP_Row[1])
            elif srcMP_Row[0][1] == '0':
                Label_Name = 'Hwy {0} milepost {1}'.format(hwyDig2, srcMP_Row[1])
            else:
                Label_Name = 'Hwy {0} milepost {1}'.format(hwyDig3, srcMP_Row[1])

        shp = srcMP_Row[3]

        tarRows.insertRow((Type, Label_Name, shp))

    #----Add Exit Records-------------------------------------------------------------
    for srcEX_Row in srcEX_Rows:

        Type = 'epm'

        if srcEX_Row[0].split()[0] == 'SR':
            Label_Name = 'Hwy ' + ' '.join(srcEX_Row[0].split()[1:])
        elif srcEX_Row[0].split()[0] == 'US':
            Label_Name = 'Hwy ' + ' '.join(srcEX_Row[0].split()[1:])
        else:
            Label_Name = srcEX_Row[0]

        shp = srcEX_Row[1]

        tarRows.insertRow((Type, Label_Name, shp))


    del tarRows


    #----Copy Mileposts to shapefile--------------------------------------------------
    if arcpy.Exists(outLoc + '\\Hwy_MPM.shp'):
        arcpy.Delete_management(outLoc + '\\Hwy_MPM.shp')
        arcpy.FeatureClassToShapefile_conversion(milePostsBS, outLoc)
    else:
        arcpy.FeatureClassToShapefile_conversion(milePostsBS, outLoc)


    print 'Done Translating Mileposts  ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------

def landownershipLarge():

    print 'Starting Large Landownership  ' + str(datetime.datetime.now())

    landown = sgid10_GEO + '\\LandOwnership'
    parks = sgid10_GEO + '\\Parks'
    cemeteries = sgid10_GEO + '\\Cemeteries'
    golf = sgid10_GEO + '\\GolfCourses'

    landownBS = stageDB + '\\TGR_StWide_lpy'

    clpCnty = 'SGID10.BOUNDARIES.Counties'

    #---Add new Landownership, Parks, and Cemeteries to SGID10_GEOGRAPHIC staging area
    arcpy.CopyFeatures_management('SGID10.CADASTRE.LandOwnership', landown)
    arcpy.CopyFeatures_management('SGID10.RECREATION.ParksLocal', parks)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.Cemeteries_Poly', cemeteries)
    arcpy.CopyFeatures_management('SGID10.RECREATION.GolfCourses', golf)

    #---Check for statewide Large Landownership BlueStakes schema
    if not arcpy.Exists(landownBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCClpy_schema', landownBS)
    else:
        arcpy.DeleteFeatures_management(landownBS)


    srcLnd_Flds = ['OWNER', 'DESIG', 'LABEL_STATE', 'LABEL_FEDERAL', 'STATE_LGD', 'SHAPE@']
    srcPrk_Flds = ['NAME', 'SHAPE@']
    srcCem_Flds = ['Name', 'SHAPE@']
    srcGlf_Flds = ['NAME', 'SHAPE@']

    tarFlds = ['CFCC', 'LANDNAME', 'SHAPE@']

    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']


    srcLnd_Rows = arcpy.da.SearchCursor(landown, srcLnd_Flds)
    srcPrk_Rows = arcpy.da.SearchCursor(parks, srcPrk_Flds)
    srcCem_Rows = arcpy.da.SearchCursor(cemeteries, srcCem_Flds)
    srcGlf_Rows = arcpy.da.SearchCursor(golf, srcGlf_Flds)

    tarRows = arcpy.da.InsertCursor(landownBS, tarFlds)

    #----Add LandOwn features-------------------------------------
    for srcLnd_Row in srcLnd_Rows:

        if srcLnd_Row[0] == 'Tribal':

            CFCC = 'D40'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

        if srcLnd_Row[1] == 'Military':

            CFCC = 'D10'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

        if srcLnd_Row[1] == 'National Historic Site' or srcLnd_Row[1] == 'National Monument' \
                            or srcLnd_Row[1] == 'National Park' or srcLnd_Row == 'National Recreation Area':

            CFCC = 'D83'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

        if srcLnd_Row[1] == 'National Forest':

            CFCC = 'D84'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

        if srcLnd_Row[1] == 'Primitive Area' or srcLnd_Row[1] == 'Wilderness' or srcLnd_Row[1] == 'Wildlife Reserve/Management Area' \
                             or srcLnd_Row[1] == 'National Wildlife Refuge':

            CFCC = 'D89'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

        if srcLnd_Row[1] == 'Parks and Recreation':

            CFCC = 'D85'

            if srcLnd_Row[3] != None:
                LANDNAME = srcLnd_Row[3]
            else:
                LANDNAME = srcLnd_Row[4]

            shp = srcLnd_Row[5]

            tarRows.insertRow((CFCC, LANDNAME, shp))

    #----Add Parks--------------------------------------------
    for srcPrk_Row in srcPrk_Rows:

        CFCC = 'D85'

        if srcPrk_Row[0] != None:
            LANDNAME = srcPrk_Row[0]

        else:
            LANDNAME = ''

        shp = srcPrk_Row[1]

        tarRows.insertRow((CFCC, LANDNAME, shp))


    #----Add Cemeteries--------------------------------------------
    for srcCem_Row in srcCem_Rows:

        CFCC = 'D82'

        if srcCem_Row[0] != None:
            LANDNAME = srcCem_Row[0]

        else:
            LANDNAME = ''

        shp = srcCem_Row[1]

        tarRows.insertRow((CFCC, LANDNAME, shp))

    del tarRows


    arcpy.CopyFeatures_management(landownBS, outLoc + '\\TGR_StWide_lpy.shp')


    #---Clip Blue Stakes Misc Transportation-----------------------------------------------------------
    clip(landownBS, 'lpy.shp');



    print 'Done Translating Large Landownership  ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------

def lakes():

    print 'Starting Lakes  ' + str(datetime.datetime.now())

    lakes = sgid10_GEO + '\\LakesNHDHighRes'
    lakesBS = stageDB + '\\TGR_StWide_wat'
    clpCnty = 'SGID10.BOUNDARIES.Counties'

    #---Check for lakesNHD in SGID10_GEOGRAPHIC staging area
    if arcpy.Exists(lakes):
        arcpy.Delete_management(lakes)
        arcpy.CopyFeatures_management('SGID10.WATER.LakesNHDHighRes', lakes)
    else:
        arcpy.CopyFeatures_management('SGID10.WATER.LakesNHDHighRes', lakes)

    #---Check for statewide lakes BlueStakes schema
    if not arcpy.Exists(lakesBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCWAT_schema', lakesBS)
    else:
        arcpy.DeleteFeatures_management(lakesBS)

    srcFlds = ['FType', 'FCode', 'GNIS_Name', 'InUtah', 'SHAPE@']
    tarFlds = ['CFCC', 'LANDNAME', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(lakes, srcFlds)
    tarRows = arcpy.da.InsertCursor(lakesBS, tarFlds)






    print 'Done Translating Lakes  ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------

def rail():

    print 'Starting Railroads  ' + str(datetime.datetime.now())

    rail = sgid10_GEO + '\\Railroads'
    railLt = sgid10_GEO + '\\LightRail_UTA'
    railLt_new = sgid10_GEO + '\\LightRailNewRoutes_UTA'
    railCommut = sgid10_GEO + '\\CommuterRailRoute_UTA'
    railCommut_new = sgid10_GEO + '\\CommuterRailNewRoutes_UTA'

    railBS = stageDB + '\\TGR_StWide_lkB'


    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.Railroads', rail)
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.LightRail_UTA', railLt)
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.LightRailNewRoutes_UTA', railLt_new)
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.CommuterRailRoute_UTA', railCommut)
    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.CommuterRailNewRoutes_UTA', railCommut_new)


    #---Check for statewide railroad BlueStakes schema
    if not arcpy.Exists(railBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCClkB_schema', railBS)
    else:
        arcpy.DeleteFeatures_management(railBS)


    srcRail_Flds = ['RAILROAD', 'SHAPE@']
    srcRailLt_Flds = ['SHAPE@']
    srcRailLtNew_Flds = ['SHAPE@']
    srcRailCommut_Flds = ['SHAPE@']
    srcRailCommutNew_Flds = ['SHAPE@']

    tarFlds = ['FENAME', 'CFCC2', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRail_Rows = arcpy.da.SearchCursor(rail, srcRail_Flds)
    srcRailLt_Rows = arcpy.da.SearchCursor(railLt, srcRailLt_Flds)
    srcRailLtNew_Rows = arcpy.da.SearchCursor(railLt_new, srcRailLtNew_Flds)
    srcRailCommut_Rows = arcpy.da.SearchCursor(railCommut, srcRailCommut_Flds)
    srcRailCommutNew_Rows = arcpy.da.SearchCursor(railCommut_new, srcRailCommutNew_Flds)

    tarRows = arcpy.da.InsertCursor(railBS, tarFlds)

    #---Add Railroads---------------------------------
    for srcRail_Row in srcRail_Rows:

        if srcRail_Row[0] != 'UTA' and srcRail_Row[0] != 'UT Transit Auth':

            FENAME = srcRail_Row[0]
            CFCC2 = 'B1'
            shp = srcRail_Row[1]

            tarRows.insertRow((FENAME, CFCC2, shp))

    #----Add Light Rail------------------------------------
    for srcRailLt_Row in srcRailLt_Rows:

        FENAME = 'UTA Trax light rail'
        CFCC2 = 'B1'
        shp = srcRailLt_Row[0]

        tarRows.insertRow((FENAME, CFCC2, shp))

    #----Add Light New Rail------------------------------------
    for srcRailLtNew_Row in srcRailLtNew_Rows:

        FENAME = 'UTA Trax light rail'
        CFCC2 = 'B1'
        shp = srcRailLtNew_Row[0]

        tarRows.insertRow((FENAME, CFCC2, shp))

    #----Add Commuter Rail------------------------------------
    for srcRailCommut_Row in srcRailCommut_Rows:

        FENAME = 'UTA Frontrunner railroad'
        CFCC2 = 'B1'
        shp = srcRailCommut_Row[0]

        tarRows.insertRow((FENAME, CFCC2, shp))

    #----Add Commuter New Rail------------------------------------
    for srcRailCommutNew_Row in srcRailCommutNew_Rows:

        FENAME = 'UTA Frontrunner railroad'
        CFCC2 = 'B1'
        shp = srcRailCommutNew_Row[0]

        tarRows.insertRow((FENAME, CFCC2, shp))

    del tarRows


    #---Copy Railroads to Blue Stakes root level----------------------
    arcpy.CopyFeatures_management(railBS, outLoc + '\\TGR_StWide_lkB.shp')


    #---Clip Blue Stakes Airstrips-----------------------------------------------------------
    clip(railBS, 'lkB.shp');


    print 'Done Translating Railroads  ' + str(datetime.datetime.now())



#-------------------------------------------------------------------------------------------------------------------------------------------

def airstrips():

    print 'Starting Airstrips  ' + str(datetime.datetime.now())

    airstrips = sgid10_GEO + '\\Airports'
    airstripsBS = stageDB + '\\TGR_StWide_lkD'
    clpCnty = 'SGID10.BOUNDARIES.Counties'

    arcpy.CopyFeatures_management('SGID10.TRANSPORTATION.Airports', airstrips)

    #---Check for statewide airports BlueStakes schema
    if not arcpy.Exists(airstripsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCClkD_schema', airstripsBS)
    else:
        arcpy.DeleteFeatures_management(airstripsBS)

    srcFlds = ['FAC_TYPE', 'FULLNAME', 'SHAPE@']
    tarFlds = ['FENAME', 'CFCC2', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(airstrips, srcFlds)
    tarRows = arcpy.da.InsertCursor(airstripsBS, tarFlds)

    for srcRow in srcRows:

        if srcRow[0] == 'AIRPORT':
            if srcRow[0].find('AIRFIELD') != -1:
                FENAME = srcRow[1].replace('MUNI', 'MUNICIPAL')
            elif srcRow[0].find('BASE') != -1:
                FENAME = srcRow[1]
            else:
                FENAME = srcRow[1].replace('MUNI', 'MUNICIPAL') + ' ' + srcRow[0]
        else:
            FENAME = srcRow[1]

        CFCC2 = 'D5'

        shp = srcRow[2]

        tarRows.insertRow((FENAME, CFCC2, shp))

    del tarRows


    #---Copy Airstrips to Blue Stakes root level-------------------------
    arcpy.CopyFeatures_management(airstripsBS, outLoc + '\\TRG_StWide_lkD.shp')


    #---Clip Blue Stakes Airstrips-----------------------------------------------------------
    clip(airstripsBS, 'lkD.shp');


    print 'Done Translating Airstrips  ' + str(datetime.datetime.now())


#-------------------------------------------------------------------------------------------------------------------------------------------

def miscTransportation():

    print 'Starting Misc Transportation  ' + str(datetime.datetime.now())

    miscTrans = sgid10_GEO + '\\SkiLifts'
    miscTransBS = stageDB + '\\TGR_StWide_lkC'
    clpCnty = 'SGID10.BOUNDARIES.Counties'

    arcpy.CopyFeatures_management('SGID10.RECREATION.SkiLifts', miscTrans)

    #---Check for statewide municipalities BlueStakes schema
    if not arcpy.Exists(miscTransBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCClkC_schema', miscTransBS)
    else:
        arcpy.DeleteFeatures_management(miscTransBS)

    srcFlds = ['LIFT_NAME', 'SHAPE@']
    tarFlds = ['FENAME', 'CFCC2', 'SHAPE@']
    cntyFlds = ['NAME', 'FIPS_STR', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(miscTrans, srcFlds)
    tarRows = arcpy.da.InsertCursor(miscTransBS, tarFlds)

    for srcRow in srcRows:

        FENAME = srcRow[0] + ' Ski Lift'
        CFCC2 = 'C3'
        shp = srcRow[1]

        tarRows.insertRow((FENAME, CFCC2, shp))

    del tarRows


    #---Copy Misc Trans to Blue Stakes root level---------------
    arcpy.CopyFeatures_management(miscTransBS, outLoc + '\\TGR_StWide_lkC.shp')


    #---Clip Blue Stakes Misc Transportation-----------------------------------------------------------
    clip(miscTransBS, 'lkC.shp');


    print 'Done Translating Misc Transportation  ' + str(datetime.datetime.now())

#----------------------------------------------------------------------------------------------------------------------------------------------

def townships():

    print 'Starting Townships  ' + str(datetime.datetime.now())

    twnShips = sgid10_GEO + '\\PLSSTownships'
    twnShipsBS = stageDB + '\\UT_TR'

    #---Move Townships in SGID10_GEOGRAPHIC staging area
##    if arcpy.Exists(muni):
##        arcpy.Delete_management(muni)
    arcpy.CopyFeatures_management('SGID10.CADASTRE.PLSSTownships_GCDB', twnShips)
##    else:
##        arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Municipalities', muni)

    #---Check for statewide township BlueStakes schema
    if not arcpy.Exists(twnShipsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\UT_TR_schema', twnShipsBS)
    else:
        arcpy.DeleteFeatures_management(twnShipsBS)

    srcFlds = ['BASEMERIDIAN', 'TWNSHPLAB', 'SHAPE@']
    tarFlds = ['NAME', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(twnShips, srcFlds)
    tarRows = arcpy.da.InsertCursor(twnShipsBS, tarFlds)

    for srcRow in srcRows:

        NAME = ("SL" if srcRow[0] == "26" else "UI") + " " + srcRow[1]
        shp = srcRow[2]

        tarRows.insertRow((NAME, shp))

    del tarRows

    #---Export to shapefile-------------------------------------------
    arcpy.CopyFeatures_management(twnShipsBS, outLoc + '\\UT_TR.shp')

    outTwnshps = outLoc + '\\UT_TR.shp'
    flds = arcpy.ListFields(outTwnshps)
    for fld in flds:
        if fld.name == 'Shape_Area':
            arcpy.DeleteField_management(outTwnshps, 'Shape_Area')
        if fld.name == 'Shape_Leng':
            arcpy.DeleteField_management(outTwnshps, 'Shape_Leng')


    print 'Done Translating Townships  ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------------

def sections():

    print 'Starting Sections  ' + str(datetime.datetime.now())

    sections = sgid10_GEO + '\\PLSSSections'
    sectionsBS = stageDB + '\\UT_TRS'

    #---Move Sections to SGID10_GEOGRAPHIC staging area
##    if arcpy.Exists(muni):
##        arcpy.Delete_management(muni)
    arcpy.CopyFeatures_management('SGID10.CADASTRE.PLSSSections_GCDB', sections)
##    else:
##        arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Municipalities', muni)

    #---Check for statewide BlueStakes sections
    if not arcpy.Exists(sectionsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\UT_TRS_schema', sectionsBS)
    else:
        arcpy.DeleteFeatures_management(sectionsBS)

    srcFlds = ['SNUM', 'SHAPE@']
    tarFlds = ['NAME', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(sections, srcFlds)
    tarRows = arcpy.da.InsertCursor(sectionsBS, tarFlds)

    for srcRow in srcRows:

        NAME = srcRow[0]
        shp = srcRow[1]

        tarRows.insertRow((NAME, shp))

    del tarRows


    #---Export to shapefile-------------------------------------------
    arcpy.CopyFeatures_management(sectionsBS, outLoc + '\\UT_TRS.shp')

    outSections = outLoc + '\\UT_TR.shp'
    flds = arcpy.ListFields(outTwnshps)
    for fld in flds:
        if fld.name == 'Shape_Area':
            arcpy.DeleteField_management(outTwnshps, 'Shape_Area')
        if fld.name == 'Shape_Leng':
            arcpy.DeleteField_management(outTwnshps, 'Shape_Leng')


    print 'Done Translating Sections  ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------------

def deciPoints():

    print 'Starting Deci Points (GNIS) ' + str(datetime.datetime.now())

    deciPts = sgid10_GEO + '\\GNIS2010'
    deciPtsBS = stageDB + '\\TGR_StWide_deci'

    #---Move GNIS to SGID10_GEOGRAPHIC staging area
    arcpy.CopyFeatures_management('SGID10.LOCATION.PlaceNamesGNIS2010', deciPts)

    #---Check for statewide Deci Points BlueStakes schema
    if not arcpy.Exists(deciPtsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCdeci_schema', deciPtsBS)
    else:
        arcpy.DeleteFeatures_management(deciPtsBS)

    srcFlds = ['NAME', 'SHAPE@']
    tarFlds = ['NAME', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(deciPts, srcFlds)
    tarRows = arcpy.da.InsertCursor(deciPtsBS, tarFlds)

    for srcRow in srcRows:

        if srcRow[0] != None:
            NAME = srcRow[0]
        else:
            NAME = ''

        shp = srcRow[1]

        tarRows.insertRow((NAME, shp))

    del tarRows


    #---Clip Blue Stakes Deci Points-----------------------------------------------------------
    clip(deciPtsBS, 'deci.shp');


    print 'Done Translating Deci Points (GNIS) ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------------

def addedPoints():

    print 'Starting Added Points ' + str(datetime.datetime.now())

    correctionsPts = sgid10_GEO + '\\CorrectionalFacilities'
    fireStnPts = sgid10_GEO + '\\FireStations'
    libraryPts = sgid10_GEO + '\\Libraries'
    liquorPts = sgid10_GEO + '\\LiquorStores'
    churchPts = sgid10_GEO + '\\PlacesOfWorship'
    policePts = sgid10_GEO + '\\PoliceStations'
    postOfficePts = sgid10_GEO + '\\PostOffices'
    schoolPts = sgid10_GEO + '\\Schools'
    mallPts = sgid10_GEO + '\\ShoppingMalls'
    healthCarePts = sgid10_GEO + '\\HealthCareFacilities'

    addedPtsBS = stageDB + '\\TGR_StWide_added'

    #---Move Points to SGID10_GEOGRAPHIC staging area
    arcpy.CopyFeatures_management('SGID10.SOCIETY.CorrectionalFacilities', correctionsPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.FireStations', fireStnPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.Libraries', libraryPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.LiquorStores', liquorPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.PlacesOfWorship', churchPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.PoliceStations', policePts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.PostOffices', postOfficePts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.Schools', schoolPts)
    arcpy.CopyFeatures_management('SGID10.SOCIETY.ShoppingMalls', mallPts)
    arcpy.CopyFeatures_management('SGID10.HEALTH.HealthCareFacilities', healthCarePts)
    print 'Done copying features from SGID10 to staging area'

    #---Check for statewide Deci Points BlueStakes schema
    if not arcpy.Exists(addedPtsBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCdeci_schema', addedPtsBS)
    else:
        arcpy.DeleteFeatures_management(addedPtsBS)


    tarFlds = ['NAME', 'SHAPE@']
    tarRows = arcpy.da.InsertCursor(addedPtsBS, tarFlds)

    pointFC_List = [correctionsPts, fireStnPts, libraryPts, churchPts, mallPts, healthCarePts]

    #---Loop through feature classes that have common fields-------
    for pointFC in pointFC_List:

        srcFlds = ['NAME', 'SHAPE@']
        srcRows = arcpy.da.SearchCursor(pointFC, srcFlds)

        for srcRow in srcRows:

            if srcRow[0] != None:
                if len(srcRow[0]) > 79:
                    NAME = ' '.join(srcRow[0].split()[:-1]).title()
                else:
                    NAME = srcRow[0].title()
            else:
                NAME = ''

            shp = srcRow[1]

            tarRows.insertRow((NAME, shp))

        print 'Added ' + pointFC


    liquorFlds = ['TYPE', 'SHAPE@']
    policeFlds = ['NAME', 'SHAPE@']
    postOfficeFlds = ['TOWN', 'STREET', 'SHAPE@']
    schoolFlds = ['INSTITUTION_NAME', 'SHAPE@']

    liquorRows = arcpy.da.SearchCursor(liquorPts, liquorFlds)
    policeRows = arcpy.da.SearchCursor(policePts, policeFlds)
    postOfficeRows = arcpy.da.SearchCursor(postOfficePts, postOfficeFlds)
    schoolRows = arcpy.da.SearchCursor(schoolPts, schoolFlds)


    for liquorRow in liquorRows:

        if liquorRow[0] != None:
            NAME = 'Liquor ' + liquorRow[0]
        else:
            NAME = 'Liquor Store'

        shp = liquorRow[1]

        tarRows.insertRow((NAME, shp))

    print 'Added ' + liquorPts


    for policeRow in policeRows:

        if policeRow[0] != None:
            if policeRow[0] == 'UNITED STATES FISH AND WILDLIFE SERVICE - OFFICE OF LAW ENFORCEMENT - BEAR RIVER MIGRATORY BIRD REFUGE':
                NAME = 'U.S. Fish And Wildlife Service - Law Enforcement - Bear River Bird Refuge'
            else:
                NAME = (policeRow[0].title().replace('United States', 'U.S.'))
        else:
            NAME = ''

        shp = policeRow[1]

        tarRows.insertRow((NAME, shp))

    print 'Added ' + policePts


    for postOfficeRow in postOfficeRows:

        if postOfficeRow[0] != None:
            NAME = postOfficeRow[0] + ' Post Office'
        else:
            NAME = 'Post Office'

        shp = policeRow[1]

        tarRows.insertRow((NAME, shp))

    print 'Added ' + postOfficePts


    for schoolRow in schoolRows:

        if schoolRow[0] != None:
            NAME = schoolRow[0].title()
        else:
            NAME = ''

        shp = schoolRow[1]

        tarRows.insertRow((NAME, shp))

    print 'Added ' + schoolPts




    del tarRows


    #---Clip Blue Stakes Deci Points-----------------------------------------------------------
    clip(deciPtsBS, 'deci.shp');


    print 'Done Translating Added Points ' + str(datetime.datetime.now())


#----------------------------------------------------------------------------------------------------------------------------------------------

def counties():

    print 'Starting Counties ' + str(datetime.datetime.now())

    cnty = sgid10_GEO + '\\Counties'
    utah = sgid10_GEO + '\\Utah'
    cntyBS = stageDB + '\\TGRSSCCCcty00'
    cntyBS_All = stageDB + '\\CO49_D90'
    stateBS = stageDB + '\\ST49_D00'

    #---Move Counties to SGID10_GEOGRAPHIC staging area
    arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Counties', cnty)
    arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Utah', utah)

    #---Check for County BlueStakes schema
    if not arcpy.Exists(cntyBS):
        arcpy.CopyFeatures_management(schemaDB + '\\TGRSSCCCcty00_schema', cntyBS)
    if not arcpy.Exists(cntyBS_All):
        arcpy.CopyFeatures_management(schemaDB + '\\CO49_D90_schema', cntyBS_All)
    if not arcpy.Exists(stateBS):
        arcpy.CopyFeatures_management(schemaDB + '\\ST49_D00_schema', stateBS)
    else:
        arcpy.DeleteFeatures_management(cntyBS)
        arcpy.DeleteFeatures_management(cntyBS_All)
        arcpy.DeleteFeatures_management(stateBS)

    srcFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
    srcFldsUT = ['STATE', 'SHAPE@']
    cntyFlds = ['COUNTY', 'SHAPE@']
    cntyAllFlds = ['NAME', 'ST', 'CO', 'SHAPE@']
    stFlds = ['NAME', 'STATE', 'SHAPE@']

    srcRows = arcpy.da.SearchCursor(cnty, srcFlds)
    srcRowsUT = arcpy.da.SearchCursor(utah, srcFldsUT)
    cntyRows = arcpy.da.InsertCursor(cntyBS, cntyFlds)
    cntyAllRows = arcpy.da.InsertCursor(cntyBS_All, cntyAllFlds)
    stRows = arcpy.da.InsertCursor(stateBS, stFlds)

    #---Create individual county shapefiles--------------------------------------------------------
    for srcRow in srcRows:

        if srcRow[0] != None:
            COUNTY = srcRow[0]
        else:
            COUNTY = ''

        shp = srcRow[2]

        cntyRows.insertRow((COUNTY, shp))

    del cntyRows

    arcpy.CopyFeatures_management(cntyBS, outLoc + outCntyShp)

    #---Copy each county to Bluestakes folder----------
    cntyBSRows = arcpy.da.SearchCursor(cntyBS, cntyFlds)

    for cntyBSRow in cntyBSRows:

        cntyName = ''.join(cntyBSRow[0].title().split())
        fldrPrefix = '\\TGR'
        outFldr = outLoc + '\\TGR' + fipsDict[cntyName]
        outCntyShp = fldrPrefix + fipsDict[cntyName] + 'cty00.shp'

        cntyFL = arcpy.MakeFeatureLayer_management(cntyBS, cntyName + '_FL', " \"COUNTY\" = '{0}' ".format(cntyBSRow[0]))
        arcpy.CopyFeatures_management(cntyFL, outFldr + outCntyShp)

        flds = arcpy.ListFields(outFldr + outCntyShp)
        for fld in flds:
            if fld.name == 'Shape_Area':
                arcpy.DeleteField_management(outFldr + outCntyShp, 'Shape_Area')
                print 'should have deleted area fld'
            if fld.name == 'Shape_Leng':
                arcpy.DeleteField_management(outFldr + outCntyShp, 'Shape_Leng')
                print 'should have deleted leng fld'


    #---Create Statewide County Shapefile----------------------------------------------------------
    for srcRow in srcRows:

        NAME = srcRow[0]
        ST = '49'
        CO = srcRow[1][-3:]
        shp = srcRow[2]

        cntyAllRows.insertRow((NAME, ST, CO, shp))

    del cntyAllRows

    cntyBS_All_shp = outLoc + '\\CO49_D90.shp'
    arcpy.CopyFeatures_management(cntyBS_All, cntyBS_All_shp)

    flds = arcpy.ListFields(cntyBS_All_shp)
    for fld in flds:
        if fld.name == 'Shape_Area':
            arcpy.DeleteField_management(cntyBS_All_shp, 'Shape_Area')
        if fld.name == 'Shape_Leng':
            arcpy.DeleteField_management(cntyBS_All_shp, 'Shape_Leng')


    #---Create State shapfile--------------------------------------------------------------------
    for srcRowUT in srcRowsUT:
        if srcRowUT[0] == 'Utah':

            NAME = 'Utah'
            STATE = '49'
            shp = srcRowUT[1]

            stRows.insertRow((NAME, STATE, shp))

    del stRows

    stateBS_shp = outLoc + '\\ST49_D00.shp'
    arcpy.CopyFeatures_management(stateBS, stateBS_shp)

    flds = arcpy.ListFields(stateBS_shp)
    for fld in flds:
        if fld.name == 'Shape_Area':
            arcpy.DeleteField_management(stateBS_shp, 'Shape_Area')
        if fld.name == 'Shape_Leng':
            arcpy.DeleteField_management(stateBS_shp, 'Shape_Leng')



    print 'Done Translating Counties ' + str(datetime.datetime.now())




#---Clip Blue Stakes output, delete empty shapefiles, delete Shape_Leng field-----------------------------------------
def clip(clipMe, outNameSuffix):

    clpCnty = sgid10_GEO + '\\Counties'

    arcpy.CopyFeatures_management('SGID10.BOUNDARIES.Counties', clpCnty)

    clpFlds = ['NAME', 'FIPS_STR', 'SHAPE@']
    clpRows = arcpy.da.SearchCursor(clpCnty, clpFlds)
    fldrPrefix = '\\TGR'


    for row in clpRows:
        clpFeat = row[2]

        #----Delete shapefiles with no features----
        clp = arcpy.Clip_analysis(clipMe, clpFeat, outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix)
        clpCount = int(arcpy.GetCount_management(clp).getOutput(0))

        if clpCount < 1:
            arcpy.Delete_management(clp)

        flds = arcpy.ListFields(clp)
        for fld in flds:
            if fld.name == 'Shape_Area':
                arcpy.DeleteField_management(clp, 'Shape_Area')
            if fld.name == 'Shape_Leng':
                arcpy.DeleteField_management(clp, 'Shape_Leng')

##        else:
##            #----Delete shapefiles with no features----
##            clp = arcpy.Clip_analysis(clipMe, clpFeat, outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix)
##            clpCount = int(arcpy.GetCount_management(clp).getOutput(0))
##            if clpCount < 1:
##                arcpy.Delete_management(clp)
##
##            flds = [fld.name for fld in arcpy.ListFields(clp)]
##            if fld.name == 'SHAPE_Leng' or fld.name == 'Shape_Leng':
##                arcpy.DeleteField_management(clp, 'SHAPE_Leng')
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
##            clp = arcpy.Clip_analysis(clipMe, clpFeat, outLoc + fldrPrefix + row[1] + fldrPrefix + row[1] + outNameSuffix)
##            clpCount = int(arcpy.GetCount_management(clp).getOutput(0))
##            if clpCount < 1:
##                arcpy.Delete_management(clp)
##
##            flds = [fld.name for fld in arcpy.ListFields(clp)]
##            if fld.name == 'SHAPE_Leng' or fld.name == 'Shape_Leng':
##                arcpy.DeleteField_management(clp, 'SHAPE_Leng')



#parcels();
#roads();
#municipalities();
#mileposts();
#landownershipLarge();
#lakes();
#rail();
#airstrips();
#miscTransportation();
#addressPoints();
townships();
#sections();
#deciPoints();
#addedPoints();
#counties();

