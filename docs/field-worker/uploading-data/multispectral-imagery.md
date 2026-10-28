---
title: Multispectral Imagery
sidebar_position: 2
---

Multispectral imagery can be uploaded to the raw directory of collections for storage as well as for further processing into derived products.

## Supported Cameras

1. [MicaSense RedEdge-MX and Altum](https://www.micasense.com/)
2. [Sentera 6X](https://sentera.com/products/fieldcapture/sensors/6x/)
3. [DJI Phantom 4 Multispectral](https://www.dji.com/p4-multispectral)
4. [DJI Mavic 3 Multispectral](https://ag.dji.com/mavic-3-m)

## Requirements

1. All files uploaded must be compressed into a .zip or .tar.gz file. See the [file requirements](index.md#file-requirements).
2. The uploaded zip is recommended to be of a single flight.
3. Image naming convention must be `IMG_[four numbers]_[band number].tif`.
4. There must be five bands if the data is from a RedEdge sensor or six bands if the data is from Altum.
5. The images with name IMG_0000_*.tif (set of 5 or 6 bands) must be of the panel. This image is optional but highly recommended for proper calibration. There must be no other panel images anywhere else in the uploaded zip.
6. The images with name IMG_0001_*.tif (set of 5 or 6 bands) must exist, and is used to calibrate the alignment for the rest of the image collection. It is for this reason it is assumed that the uploaded zip is of a single flight. It is up to you to pick a good image to use for alignment, ideally one with lots of reference point objects such as cars, buildings or large chasms. If the camera experiences a shock event (ex. banging into a tree) the calibration may become invalid and images after the shock event may be misaligned as a result.

   1. Some flights may not have the optimal images for calibration for reasons like the recording starts while the UAV is on the ground (no birds eye view yet). In these cases the raw images must be manually adjusted to meet this requirement.
7. Take the time to look through your image collection and weed out any bad images, i.e. pictures of the camera inside the case, or pictures which are entirely black, etc. This will ensure the best chance of processing success for your flight.

:::info

It is best to zip all images you want to upload into a single .zip file rather than doing multiple uploads. The application was designed to handle very large .zip files (containing a lot of images) even in a low bandwidth environment.

:::

## Prerequisites

1. [Create a collection](../organizing-data/collections.md) if one doesn’t exist.

## Upload Multispectral Imagery Data

1. Select the upload button from the collection modal you want to upload imagery to. A new upload modal will load on the screen.

   ![](img/image-20231102-002131.png)
2. Drag & drop your compressed (.zip) file onto the “Drag & drop” area at the bottom of the form – or – click “Select file” to select your compressed (.zip) from the file system.
3. Select Upload to start the process.

:::info

OPTIONAL: Once your data is uploaded you can navigate to the collection and [process your raw data into derivative products](../products/generating-products.md). You can monitor the upload on the [Workflow Tasks](../workflow-tasks.md) page.

:::
