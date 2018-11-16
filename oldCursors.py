import arcpy
from arcpy import env

sgid10 = r'C:\ZBECK\BlueStakes\testDB.gdb'
stageDB = r'C:\ZBECK\BlueStakes\stagingBS.gdb'

env.workspace = sgid10

fipsDict = {'Beaver': 'par49001', 'BoxElder': 'par49003', 'Cache': 'par49005', 'Carbon': 'par49007', 'Daggett': 'par49009', \
'Davis': 'par49011', 'Duchesne': 'par49013', 'Emery': 'par49015', 'Garfield': 'par49017', 'Grand': 'par49019', 'Iron': 'par49021', \
'Juab': 'par49023', 'Kane': 'par49025', 'Millard': 'par49027', 'Morgan': 'par49029', 'Piute': 'par49031', 'Rich': 'par49033', \
'SaltLake': 'par49035', 'SanJuan': 'par49037', 'Sanpete': 'par49039', 'Sevier': 'par49041', 'Summit': 'par49043', 'Tooele': 'par49045', \
'Uintah': 'par49047', 'Utah': 'par49049', 'Wasatch': 'par49051', 'Washington': 'par49053', 'Wayne': 'par49055', 'Weber': 'par49057'}

for fc in arcpy.ListFeatureClasses():
    if fc.split('_')[0] == 'Parcels':

        cnty = fc.split('_')[1]

        tarRows = arcpy.InsertCursor(stageDB + '\\' + fipsDict[cnty])
        srcRows = arcpy.SearchCursor(fc)
        srcRow = srcRows.next()

        cnty = fc.split('_')[1]

        while srcRow:
            tarRow = tarRows.newRow()
            addFull = srcRow.PARCEL_ADD

            if addFull != None and addFull.strip() != '':

                tarRow.ADDR_FULL = addFull

                if addFull.split(' ')[0].isdigit():
                    addNum = addFull.split(' ')[0]
                    tarRow.ADDR_NUMB = addNum
                else:
                    addNum = ''
                    tarRow.ADDR_NUMB = addNum

                if addFull.split(' ')[1] == 'N' or addFull.split(' ')[1] == 'S' or addFull.split(' ')[1] == 'E' or addFull.split(' ')[1] == 'W':
                    preDir = addFull.split(' ')[1]
                    tarRow.FEDIRP = preDir
                else:
                    preDir = ''
                    tarRow.FEDIRP = preDir

            tarRows.insertRow(tarRow)

            srcRow = srcRows.next()

