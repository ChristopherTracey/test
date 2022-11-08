# -*- coding: utf-8 -*-
"""
FESTF Aquatic Model Prep
"""
import arcpy, os
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("spatial") # Check out any necessary licenses.
arcpy.env.overwriteOutput = True
#arcpy.env.extent = "474806.480052848 1772520.30381433 496097.346963202 1786697.97491482"

cutecode = "notrtope"
model_run = "notrtope_20190513_112842"
def Rasterizer():
    # Set environment settings
    SnapRast = arcpy.Raster(r"S:/Data/NatureServe/Species_Distributions/MoBI_HabitatModels/spp_models/bombaffi/outputs/model_predictions/bombaffi_20190830_215612.tif")
    env.workspace = "S:/Projects/_Workspaces/Christopher_Tracey/FESTF"
    arcpy.env.cellSize = SnapRast # Set the cell size environment using a raster dataset.
    # var
    InputLines = "S:/Data/NatureServe/Species_Distributions/MoBI_HabitatModels/spp_models/" + cutecode + "/outputs/model_predictions/" + model_run + "_results.shp"
    InputPolys = "S:/Data/NatureServe/Species_Distributions/MoBI_HabitatModels/spp_models/" + cutecode + "/outputs/model_predictions/" + model_run + "_results_aquaPolys.shp"
    tmpRastLines = "results_PolylineToRaster.tif"
    tmpRastPolys = "results_PolygonToRaster.tif"
    tmpOutput = model_run + ".tif"
    print("working on " + cutecode)
    # conver vector to raster
    print("- converting vector to raster")
    arcpy.conversion.PolylineToRaster(InputLines, "prbblty", tmpRastLines, "MAXIMUM_LENGTH", "NONE", 30, "BUILD")
    arcpy.PolygonToRaster_conversion(InputPolys, "prbblty", tmpRastPolys, "MAXIMUM_AREA", "NONE", 30, "BUILD")
    # combine to a new raster
    print("- merging to final to raster")
    arcpy.management.MosaicToNewRaster("results_PolygonToRaster.tif;results_PolylineToRaster.tif", env.workspace, tmpOutput, None, "32_BIT_FLOAT", None, 1, "FIRST", "MATCH")

    # Delete intermediate files
    print("- Delete intermediate files")
    arcpy.Delete_management("results_PolylineToRaster.tif;results_PolygonToRaster.tif")

if __name__ == '__main__':
        Rasterizer()

