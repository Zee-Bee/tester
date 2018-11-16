import arcpy, datetime

rdsFC = r'C:\ZBECK\BlueStakes\testDB.gdb\RoadsHACK'

##flds = ['CARTOCODE', 'PREDIR', 'FULLNAME', 'STREETTYPE', 'SUFDIR', 'L_F_ADD', 'L_T_ADD', 'R_F_ADD', 'R_T_ADD', \
##        'ALIAS1', 'ALIAS2', 'ACSALIAS', 'ACSNAME', 'COFIPS', 'HWYNAME', 'MODIFYDATE', 'ADDR_SYS', 'SHAPE@']
##
##print 'Starting Roads  ' + str(datetime.datetime.now())
##
##with arcpy.da.UpdateCursor(rdsFC, flds) as rows:
##    for row in rows:
##        for fld in flds:
##            fldX = flds.index(fld)
##
##            if row[fldX] == ' ':
##                row[fldX] = None
##
##            rows.updateRow(row)
##
##print 'End Roads  ' + str(datetime.datetime.now())



rows = arcpy.UpdateCursor(rdsFC)
for row in rows:
    if row.ALIAS1 == ' ':
        row.ALIAS1 = None

    rows.updateRow(row)
