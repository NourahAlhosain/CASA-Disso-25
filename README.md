# Mitigating Urban Heat Island in Arid Cities: Satellite-Based Analysis of Urban Greening, Evidence from Riyadh


This repository contains analysis done for my MSs in [Urban Spatial Science](https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/urban-spatial-science-msc) offered by The UCL Bartlett Centre for Advanced Spatial Analysis (CASA).


## Research Overview

### Research Question and Objectives
This study explores urban greening’s potential to mitigate urban heat islands in arid cities, with Riyadh as a case study.  
**Research Question**: *How can urban greening achieve optimal microscale temperature reductions in arid cities?*  
**Objectives**:
- Measure temperature reductions linked to urban greening in Riyadh’s microscale zones.
- Quantify the relationship between green space characteristics and temperature reduction.
- Synthesize outputs into evidence-based design standards for optimizing green space configuration.

### Abstract

<div align="justify">
Rapid urbanization intensifies urban heat islands worldwide, exacerbating public health risks, elevating energy demands, and hindering sustainable urban development, creating significant barriers to global sustainability. Although urban green infrastructure mitigates urban heat islands through cooling, studies suggest lower cooling efficiency in arid climates where moisture scarcity and high-albedo surfaces amplify thermal challenges. Yet, microscale park design research remains limited, necessitating targeted studies. This research investigates how urban greening can optimize microscale temperature reductions in arid environments, using Riyadh’s Green Riyadh Project as a case study. Employing satellite-derived average summer land surface temperature (LST) and Multi-Scale Geographically Weighted Regression, the research analyzes 194 parks to assess cooling effects, quantify relationships with green space characteristics (e.g., vegetation density, park size), and derive evidence-based design standards. Findings reveal that 30% of parks exhibit inverse heating due to low vegetation density (NDVI < 0.16), while cooling parks achieve internal LST reductions averaging 0.46°C and external cooling intensities up to 0.91°C, with mid-sized parks (3,000–6,000 m²) and a park to buildings distance of approximately 20 meters showing optimal efficiency. These insights inform park design strategies for the Green Riyadh Project, confirming the influence of urban green infrastructure characteristics on cooling and highlighting the need for optimized designs to enhance urban cooling and resilience in arid climates, contributing to sustainable urban development.
</div>

### Paper
The paper link will be added once published

## Repository Contents


### Code Files


**Data Preparation**  
- **01_ParksDataValidation.py**: Validates park boundaries using OpenStreetMap and Riyadh Municipality data, outputting `Riyadh_parks_validated.geojson` used for subsequent analysis. 

- **02_LSTRetrieval.ipynb**: Retrieves average summer land surface temperature (LST) from Landsat 8/9 imagery for study area.

- **03_NDVI-PISIRetrieval.ipynb**: Calculates Normalized Difference Vegetation Index (NDVI) and Perpendicular Impervious Surface Index (PISI) to assess vegetation and impervious surfaces for study area. 

- **04_1_building_footprints_Extraction.ipynb**: Extracts building footprints for urban context analysis. The code is adopted from [link](https://github.com/microsoft/GlobalMLBuildingFootprints/tree/main/examples) to extract buildings within the study area.

**Analysis**  
- **04_FactorsCalculations.ipynb**: Computes park morphology (area and Landscape Shape Index), land composition (Avg NDVI and PISI), and urban context factors (building density and proximity).


- **05_CoolingImpactCalculations.ipynb**: Quantifies internal and external cooling effects (e.g., LST reduction, Park Cooling Intensity).
  
- **06_ImpactFactorsAnalysis.ipynb**: Applies Multi-Scale Geographically Weighted Regression (MGWR), a spatial regression model, to analyze relationships between park characteristics (output of: `04_FactorsCalculations.ipynb`)
and cooling effects (output of: `05_CoolingImpactCalculations.ipynb`).  

**Visualization**  
- **07_ResultsVisualization.ipynb**: Includes results exploration figures.


### Data Files

The `Data/` folder contains GeoJSON files with park boundaries, buffer zones, statistics, and calculated variables (e.g., land surface temperature, vegetation density, cooling metrics) that are inputs and outputs of the study’s analysis based on the scripts described above.


## Notes on Ignored Files
**Due to their large size, raw and processed satellite raster files (e.g., Landsat 8/9 imagery and derived land surface temperature, NDVI, and PISI rasters) are excluded via `.gitignore`.** Raw Landsat 8/9 Level 2 products (June–August 2024) can be downloaded from the [USGS EarthExplorer](https://earthexplorer.usgs.gov/). Processed rasters access instructions detailed in relevant scripts.

These rasters should be stored in the `Data/Raster/` folder for use with the provided scripts.


## License
Code and processed data (e.g., GeoJSONs, visualizations) are licensed under the MIT License for open access. **Source data (e.g., Landsat, OpenStreetMap, Riyadh Municipality) follow their respective licenses.**