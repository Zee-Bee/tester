import arcpy
from arcpy import da

PoD = r'C:\ZBECK\BlueStakes\testDB.gdb\Municipalities'
PoD2load = r'C:\ZBECK\BlueStakes\testDB.gdb\MunicipalitiesIn'


#----Delete features from target Points of Diversion----------------
if arcpy.Exists(PoD):
    arcpy.DeleteFeatures_management(PoD)
    print 'Deleted features from ' + PoD
else:
    print 'Couldnt find ' + PoD


fields = ['NAME', 'COUNTYSEAT', 'SHAPE@']


#----Load new Points of Diversion------------------------------------
PoD_Rows = arcpy.da.InsertCursor(PoD, fields)


with arcpy.da.SearchCursor(PoD2load, fields) as PoD2load_Rows:
    for PoD2load_Row in PoD2load_Rows:
        PoD_Rows.insertRow(PoD2load_Row)

    del PoD_Rows
    del PoD2load_Rows

