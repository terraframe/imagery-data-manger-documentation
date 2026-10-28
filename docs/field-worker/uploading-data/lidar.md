---
title: LiDAR
sidebar_position: 4
---

import ZipRequirements from './_zip-requirements.md';

LiDAR can be uploaded to the raw directory of collections for storage as well as for further processing into derived products.

## Requirements

- Only one LiDAR file (.las or .laz) can be uploaded per upload.

<ZipRequirements example="point_cloud.las" />

## Prerequisites

1. [Create a collection](../organizing-data/collections.md) if one doesn’t exist.
2. Set the sensor format to a LiDAR format for the collection.

## Upload LiDAR

1. Select the upload button from the collection modal you want to upload LiDAR to. A new upload modal will load on the screen.

   ![](img/image-20231102-002131.png)
2. Drag & drop your compressed (.zip) file onto the “Drag & drop” area at the bottom of the form – or – click “Select file” to select your compressed (.zip) from the file system.
3. Select Upload to start the process.

:::info

OPTIONAL: Once your data is uploaded you can navigate to the collection and [process your raw data into derivative products](../products/generating-products.md). You can monitor the upload on the [Workflow Tasks](../workflow-tasks.md) page.

:::
