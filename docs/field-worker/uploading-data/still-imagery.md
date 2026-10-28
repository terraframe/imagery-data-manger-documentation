---
title: Still Imagery
sidebar_position: 1
---

import ZipRequirements from './_zip-requirements.md';

Still imagery (RGB) can be uploaded to the raw directory of collections for storage as well as for further processing into derived products.

## Requirements

<ZipRequirements example="IMG_001.jpg" />

:::info

It is best to zip all images you want to upload into a single .zip file rather than doing multiple uploads. The application was designed to handle very large .zip files (containing a lot of images) even in a low bandwidth environment.

:::

## Prerequisites

1. [Create a collection](../organizing-data/collections.md) if one doesn’t exist.

## Upload Still Imagery Data (radiometric or non-radiometric)

1. Select the upload button from the collection modal you want to upload imagery to. A new upload modal will load on the screen.

   ![](img/image-20231102-002131.png)
2. Drag & drop your compressed (.zip) file onto the “Drag & drop” area at the bottom of the form – or – click “Select file” to select your compressed (.zip) from the file system.
3. Select Upload to start the process.

:::info

OPTIONAL: Once your data is uploaded you can navigate to the collection and [process your raw data into derivative products](../products/generating-products.md). You can monitor the upload on the [Workflow Tasks](../workflow-tasks.md) page.

:::

### Including a Geologger Configuration File

1. Add the geo location (e.g. geologger) file to the zip file that contains the other raw images. See [Geologger Files](../products/geologger.md) for more information.

### Including a Ground Control Point (GCP) Configuration File

1. Add the ground control point file to the zip file that contains the other raw images. See [Ground Control Points](../products/ground-control-points.md) for more information.
