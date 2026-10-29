---
title: Uploading Data
sidebar_position: 2
---

import ZipRequirements from './_zip-requirements.md';

The Raw directory (RAW tab) of a Collection is where unprocessed or minimally processed data from a flight is stored. Uploading to the Raw directory ensures that your data is stored on the government cloud in a compliant manner and makes the data available for generating derived products.

Each type of data has its own requirements and steps:

- [Still Imagery](still-imagery.md) (RGB and thermal)
- [Multispectral Imagery](multispectral-imagery.md)
- [Video](video.md)
- [LiDAR](lidar.md)

Before uploading, [create a collection](../organizing-data/collections.md) to upload the data to if one doesn't exist already.

## Supported File Formats

| Data type | File extensions |
|---|---|
| Still images (RGB, thermal as RGB) | jpg, jpeg, png |
| Multispectral images | tif, tiff |
| Radiometric (thermal) images | tif, tiff |
| Video | mp4 |
| LiDAR | las, laz |

## File Requirements

<ZipRequirements />

## Best Practices

### Metadata

#### Automated metadata

Metadata for sensors, platforms, and UAVs are configured for the system by administrators which enables automation of parts of the metadata for each collection because the UAV, sensor, and platform must be assigned to the Collection. It’s strongly encouraged to fill out as much of the remaining metadata as possible to ensure data is compliant with storage and retention requirements.

#### Additional (optional) metadata

Sites, projects, missions, and collections all have optional metadata that should be filled out to ensure data is compliant with storage and retention requirements.

## After Initiating an Upload

Data uploads go through two basic steps.

1. The data is uploaded to the IDM server.
2. The data is processed to un-zip files, audit for issues, and automatically store data in compliant locations with the correct metadata assigned.

The post processing step (step 2 above) can take more time than the initial upload (step 1 above). You can monitor the progress of the upload in the Processing Jobs section of the [Workflow Tasks](../workflow-tasks.md) page.

:::info

If the upload fails, see [Upload Errors](../troubleshooting-processing-errors.md#upload-errors) in Troubleshooting Processing Errors.

:::

## After an Upload is Complete

Now that your data has been successfully uploaded you can manage that data from the [collection modal](../organizing-data/collections.md#the-collection-modal). You can access the collection modal from several locations in the application:

- By navigating through the hierarchy in the Site Viewer to the Site → Project → Mission → Collection.
- By selecting the “View Collection” button on the workflow task associated with the collection you uploaded data to.

From the collection you can [generate products](../products/generating-products.md) from the raw data.
