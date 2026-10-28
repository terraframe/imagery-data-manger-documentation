---
title: Generating Products
sidebar_position: 1
---

The [collection modal](../organizing-data/collections.md#the-collection-modal) is where all raw images that have been uploaded to a collection (in one or multiple uploads) and the most recently processed output products are stored. All products derived using IDM functionality are configured in the collection modal or the processing workflow and built from the data in the raw tab.

## Process Raw Data Into Products

1. Navigate to the collection you want to create derived products for and select the raw tab if it's not selected already.

   ![](img/image-20251217-013529.png)
2. OPTIONAL and **not available for video**: Exclude any raw images you want to exclude from the derived products. Right-click an image and select *Exclude image from processing*. Excluded images are shown dimmed; to include one again, right-click it and select *Include image in processing*. By default all images in raw will be included in image processing unless you choose to exclude them.
3. Click the *Process* button to open the processing options modal. The *Process* button is only shown on the raw tab, and it's disabled while a process is running. It's also disabled until the raw tab has at least two images, or at least one file for LiDAR and video collections.

   1. Options for collections with the raw tab containing still images, thermal images, and multispectral images.

      ![](img/image-20260108-164330.png)

      1. Select one or more types of products to create (*Ptcloud*, *DEM*, *Ortho*).
      2. OPTIONAL: Review and configure the options under *Advanced Settings* for this processing job (see [Advanced Settings](#advanced-settings) for more details).
   2. Options for collections with the raw tab containing LiDAR data.

      ![](img/image-20260108-183635.png)

      1. Select one or more LiDAR products to create (see [LiDAR Options](#lidar-options)).
4. Enter a *Product name*. It's required, and can only contain letters, numbers, periods and underscores (no spaces or special characters).
5. Click the *Submit* button. It's disabled until you enter a product name and select at least one product type.
6. When the processing options modal closes you’ll see a message indicating the job is running with a link to the processing job. The status of the processing job will be tracked on the [Workflow Tasks](../workflow-tasks.md) page and successful results from the task will be available on the products tab of the collection modal and the Site Viewer. See [Viewing Products](viewing-products.md).

   ![](img/image-20260108-165035.png)

## Estimated Processing Time

For still image, thermal, multispectral and video collections, the processing options modal shows an *Estimated processing time* at the top once you change a product type or setting. The estimate is based on earlier processing jobs with a similar amount of raw data and similar settings, and the modal shows how many of those jobs it used ("Based on N other similar jobs"). If there are no similar jobs, the estimate is *Unknown*.

![The Estimated processing time box, showing about 4 hours based on 204 other similar jobs](img/estimated-processing-time.png)

## Processing Outputs

Each processing job creates a product with the *Product name* you entered, and that product becomes the collection's primary product. If the collection already has a product with that name, the new outputs are added to it.

ODM processing of still image, thermal, multispectral and video collections creates these files for the product types you select:

| Product type | Files created |
|---|---|
| Ptcloud | A georeferenced point cloud (`odm_georeferenced_model.laz`). |
| DEM | A DSM (`dsm.cog.tif`) and a DTM (`dtm.cog.tif`), as Cloud Optimized GeoTIFFs, plus a hillshade of the DSM. |
| Ortho | An ortho mosaic as a Cloud Optimized GeoTIFF (`odm_orthophoto.cog.tif`) and as a PNG (`odm_orthophoto.png`). |

The ODM processing report (`report.pdf`) is added to each product type you select. The full set of ODM outputs is kept as well, and can be downloaded with the *Download All Generated Data* button in the [collection modal](../organizing-data/collections.md#the-collection-modal).

## LiDAR Options

For LiDAR collections, the processing options modal lists these products instead of the product types and Advanced Settings. None are selected by default.

| Option | Description |
|---|---|
| Generate COPC | Converts the uploaded LAS/LAZ point cloud to a Cloud Optimized Point Cloud (`pointcloud.copc.laz`) in the product. The raw tab must contain a single LAS/LAZ file. |
| Generate Tree canopy cover | Creates a tree canopy cover raster. |
| Generate ground surface model | Creates a ground surface model raster. |
| Generate terrain model | Creates a terrain model raster. |

Each raster option creates its own product, named after your *Product name* with the raster type added (for example, `myproduct_terrain_model`). The rasters are made from the COPC point cloud. If you don't select *Generate COPC* in the same job, a product with the same *Product name* that already has a COPC point cloud must exist, otherwise the job fails.

## Advanced Settings

When configuring a processing job to create products for a collection there are Advanced Settings options that can be used to further refine the processing job.

The *Advanced Settings* section is always shown in the processing options modal, below the product types. Only the settings that apply to the product types you select are shown, so select the product types first. The *Shown when* column below lists when each setting appears.

   ![](img/image-20260108-172053.png)

### Default Values

If the collection has been processed before, the processing options modal starts with the settings of the most recent processing job, including the product types that were selected. Only the *Product name* starts empty.

Otherwise, the modal starts with no product types selected and the defaults in the *Default* column below. If the collection's sensor is marked as *High Resolution* (see [Platforms and Sensors](../../administration/platforms-and-sensors.md)), the resolution defaults to 2 cm and the point cloud quality to HIGH instead.

### Advanced Settings Fields

| Field | Description | Shown when | Default | Open Drone Map Docs |
|---|---|---|---|---|
| Orthophoto and DEM Resolution (cm) | Set the resolution for both orthophoto and elevation outputs. Orthophoto and DSM/DTM resolution in cm / pixel.<br /><br />Note that this value is capped by a ground sampling distance (GSD) estimate. | *Ortho* or *DEM* is selected. | 5 (2 for high resolution sensors) | [orthophoto-resolution](https://docs.opendronemap.org/arguments/orthophoto-resolution/) and [dem-resolution](https://docs.opendronemap.org/arguments/dem-resolution/). |
| Matcher Neighbors | Perform image matching with the nearest images based on GPS exif data. Set to 0 to match by triangulation. | *Ortho* or *DEM* is selected. | 0 | [matcher-neighbors](https://docs.opendronemap.org/arguments/matcher-neighbors/). |
| Minimum number of features to extract per image | Minimum number of features to extract per image. More features can be useful for finding more matches between images, potentially allowing the reconstruction of areas with little overlap or insufficient features. More features also slow down processing. | *Ortho* or *DEM* is selected. | 10000 | [min-num-features](https://docs.opendronemap.org/arguments/min-num-features/). |
| Generated point cloud quality | Set point cloud quality. Higher quality generates better, denser point clouds, but requires more memory and takes longer. Each step up in quality increases processing time roughly by a factor of 4x. Options: ULTRA, HIGH, MEDIUM, LOW, LOWEST. | *Ptcloud* is selected. | MEDIUM (HIGH for high resolution sensors) | [pc-quality](https://docs.opendronemap.org/arguments/pc-quality/). |
| Generated feature quality | Set feature extraction quality. Higher quality generates better features, but requires more memory and takes longer. Options: ULTRA, HIGH, MEDIUM, LOW, LOWEST. | *Ortho* is selected. | HIGH | [feature-quality](https://docs.opendronemap.org/arguments/feature-quality/). |
| Radiometric calibration | Set the radiometric calibration to perform on images. When processing multispectral and thermal images you should set this option to obtain reflectance/temperature values (otherwise you will get digital number values). Options:<br /><br />- *NONE*: no calibration.<br />- *CAMERA*: applies black level, vignetting, row gradient gain/exposure compensation (if appropriate EXIF tags are found) and computes absolute temperature values.<br />- *CAMERA+SUN (experimental)*: applies all the corrections of *CAMERA*, plus compensates for spectral radiance registered via a downwelling light sensor (DLS) taking in consideration the angle of the sun. | The collection has a radiometric or multispectral *Collection Format* (or no *Collection Format*). | CAMERA for radiometric and multispectral collections, otherwise NONE | [radiometric-calibration](https://docs.opendronemap.org/arguments/radiometric-calibration/). |
| Video Resolution | The maximum output resolution of extracted video frames in pixels. | The collection has a video *Collection Format* (or no *Collection Format*) and *Ortho* is selected. | Blank, which uses 4000 | [video-resolution](https://docs.opendronemap.org/arguments/video-resolution/). |
| Video Limit | Maximum number of frames to extract from video files for processing. Set to 0 for no limit. | The collection has a video *Collection Format* (or no *Collection Format*) and *Ortho* is selected. | Blank, which uses 500 | [video-limit](https://docs.opendronemap.org/arguments/video-limit/). |

:::info

The advanced settings are [Open Drone Map](https://docs.opendronemap.org/) settings, which is part of IDM's internal processing engine.

:::

## Georeferencing Options

Geo location and ground control point files are selected when you upload raw data, not when you process it. If a collection has a stored geo location file (`geo.txt`) or ground control point file (`gcp_list.txt`), IDM uses it automatically when processing. See [Geologger Files](geologger.md) and [Ground Control Points](ground-control-points.md).

If the collection's sensor needs a geo location file and none has been uploaded, the processing modal shows "Your sensor requires an uploaded geo location file" and you can't submit the job.
