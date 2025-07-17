import os
import processing
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsVectorFileWriter,
    QgsCoordinateReferenceSystem,
    QgsFeatureSink
)
from PyQt5.QtCore import QVariant

# Define paths and parameters
output_dir = "/Users/Nourah/Desktop/Urban Spatial Science/courses/Dissertation/CASA-Disso-25/Data"  # Specify output directory
osm_layer_name = "OSM_parks"  # Name of OSM polygons layer in QGIS
muni_layer_name = "portal-parks"  # Name of municipality points layer in QGIS
osm_id_field = "osm_id"  # Specify cols to copy from inital layer. From OSM data, copy id in case needed for validation
point_attributes = [
    "OBJECTID", "FEATURE_ANAME", "MUNICIPALITY", "DISTRICT",
    "WALKING_TRACK", "GREEN_AREAS", "LAYERID", "LAYERANAME"
] # Specify cols to copy from inital layer. chose variables that might be useful for future analysis
output_crs = "EPSG:4326"  # Specify output CRS to ensure consistency

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load layers
try:
    osm_layer = QgsProject.instance().mapLayersByName(osm_layer_name)[0]
    muni_layer = QgsProject.instance().mapLayersByName(muni_layer_name)[0]
except IndexError:
    print(f"Error: One or both layers ('{osm_layer_name}', '{muni_layer_name}') not found in QGIS project.")
    raise
    
# Verify CRS consistency
if osm_layer.crs() != muni_layer.crs():
    print("CRS mismatch detected. Reprojecting municipality layer to match OSM layer.")
    muni_layer = processing.run(
        "qgis:reprojectlayer",
        {
            "INPUT": muni_layer,
            "TARGET_CRS": osm_layer.crs(),
            "OUTPUT": "memory:reprojected_muni"
        }
    )["OUTPUT"]

# Step 1: Clean geometries
valid_osm = processing.run(
    "qgis:fixgeometries",
    {
        "INPUT": osm_layer,
        "OUTPUT": "memory:valid_osm"
    }
)["OUTPUT"]
valid_muni = processing.run(
    "qgis:fixgeometries",
    {
        "INPUT": muni_layer,
        "OUTPUT": "memory:valid_muni"
    }
)["OUTPUT"]

# Step 2: Create validated layer with OSM polygons (id and shape only) and point attributes
# Initialize output layer with id field and point attributes
field_list = [QgsField(osm_id_field, QVariant.String)] + [QgsField(attr, QVariant.String) for attr in point_attributes]
validated_layer = QgsVectorLayer(
    f"Polygon?crs={valid_osm.crs().authid()}",
    "validated_parks",
    "memory"
)
validated_layer.dataProvider().addAttributes(field_list)
validated_layer.updateFields()

# Step 3: Spatial comparison and attribute transfer
added_polygons = set()  # Track added polygon IDs to avoid duplicates
sink = validated_layer.dataProvider()

for muni_feat in valid_muni.getFeatures():
    muni_geom = muni_feat.geometry()
    for osm_feat in valid_osm.getFeatures():
        osm_geom = osm_feat.geometry()
        osm_id = osm_feat[osm_id_field]  # Use specified OSM ID field
        
        if osm_id not in added_polygons and muni_geom.intersects(osm_geom):
            # Create new feature with OSM polygon geometry
            new_feat = QgsFeature(validated_layer.fields())
            new_feat.setGeometry(osm_geom)
            
            # Set OSM ID
            new_feat[osm_id_field] = osm_id
            
            # Transfer specified point attributes
            for attr in point_attributes:
                new_feat[attr] = muni_feat[attr]
            
            # Add feature to output layer
            sink.addFeature(new_feat, QgsFeatureSink.FastInsert)
            added_polygons.add(osm_id)

# Step 4: Save validated layer as GeoJSON
output_validated = os.path.join(output_dir, "Riyadh_parks_validated.geojson")
writer_options = QgsVectorFileWriter.SaveVectorOptions()
writer_options.driverName = "GeoJSON"
writer_options.destCRS = QgsCoordinateReferenceSystem(output_crs)
try:
    QgsVectorFileWriter.writeAsVectorFormatV2(
        validated_layer,
        output_validated,
        QgsProject.instance().transformContext(),
        writer_options
    )
except Exception as e:
    print(f"Error saving validated layer: {e}")
    raise
