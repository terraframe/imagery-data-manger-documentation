---
title: Troubleshooting Processing Errors
sidebar_position: 3.5
toc_max_heading_level: 2
---

This page lists the errors IDM reports while uploading and processing data, what causes them, and how to fix them. Errors are grouped by the stage of the job they happen in.

## Where Errors Are Shown

Errors are shown on the [Workflow Tasks](workflow-tasks.md) page, in the step of the processing job where they happened:

- **Status and Message.** When a step fails, its status changes to *Failed* (or *Error*) and its *Message* explains why.
- **Show Messages.** Some errors are listed with the *Show Messages* button instead, often along with warnings and other information. A message that ends with "View messages for more information" or "Check the messages for more information" means the details are in that list.
- **Complete With Messages.** A step that finished but recorded messages shows the status *Complete With Messages*. Check the messages: some of them, such as skipped files, may mean part of your data wasn't used.

Some messages include text that comes directly from the processing tools. If your message isn't on this page, or the fix doesn't work, [contact IDM support](../getting-started/getting-help.md) and include the full message.

## Trying Again

Some errors don't have a specific cause you can fix, and the suggested fix is to try the upload or processing again. In those cases:

:::warning

Try only **once** more. If it fails a second time, [contact IDM support](../getting-started/getting-help.md) instead of trying again. Repeated attempts are unlikely to work, use processing resources, and can make the problem harder to diagnose.

:::

## Upload Errors

These errors happen while IDM checks the files in an uploaded .zip or .tar.gz file. See the [file requirements](uploading-data/index.md#file-requirements).

| Message | Cause | Fix |
|---|---|---|
| The zip did not contain any files to process. Files must follow proper naming conventions and end in one of the following file extensions: … | None of the files in the archive have a file type the collection accepts. For multispectral and radiometric collections, the message starts with "You selected a multispectral sensor." or "You selected a radiometric sensor." | Check the file types against the [supported file formats](uploading-data/index.md#supported-file-formats) for the collection's format. |
| The uploaded file did not pass validation. Check the messages for more information. | One or more files failed a check. | Open *Show Messages* to see which files and why. |
| The file [name] is of an unsupported format and will be ignored. The following formats are supported: … | A file in the archive has a file type the collection doesn't accept. The file is skipped and the rest of the upload continues. | No action needed if the file wasn't meant to be uploaded. Otherwise, check the collection's format. |
| The filename [name] contains special characters which will be replaced with an underscore. | A file name contains characters other than letters, numbers, periods and underscores. The file is renamed and uploaded. | No action needed. Rename files before uploading to keep their original names. |
| The filename [name] conflicts with another name in the uploaded archive. … This will result in missing files. | Two files end up with the same name, because they were in different folders or because of replaced characters. Only the first one is kept. | Give every file a unique name and upload the missing files again. |
| The file [name] is not a valid image file | An image can't be read. It may be damaged or not really an image. | Remove or re-export the image and upload again. |
| The system encountered an error while reading your zip file. Your zip file may be corrupt, or it may have gotten corrupt during upload. | The archive can't be opened. | Create the zip file again and upload it again. |
| The zip file contains more than a single point cloud file. A Lidar collection can only have one raw point cloud. | A LiDAR upload contains more than one LAS/LAZ file. | Upload one point cloud per collection. See [LiDAR](uploading-data/lidar.md). |
| The zip file contains a new point cloud file with a different name than an existing point cloud file. A Lidar collection can only have one raw point cloud. | The collection already has a point cloud with a different name. | Use a new collection, or give the file the same name as the existing one to replace it. |
| Invalid Product Name [name]. No spaces or special characters … are allowed. | The product name contains spaces or special characters. | Use only letters, numbers, periods and underscores. |
| An error occurred while uploading the imagery to S3. … | The upload couldn't be completed. The rest of the message gives the reason. | Look up the rest of the message on this page. If it isn't listed, [contact support](../getting-started/getting-help.md). |

## Geo Location and Ground Control Point File Errors

These errors happen when IDM checks a [geo location file](products/geologger.md) or [ground control point file](products/ground-control-points.md) during upload, or before processing. The upload fails with one of these messages, and each problem in the file is listed under *Show Messages*.

| Message | Cause | Fix |
|---|---|---|
| Geo location file did not match the expected file format. View messages for more information. | The geo location file has errors. | Fix each line listed under *Show Messages* and upload the file again. See [Geologger Files](products/geologger.md#file-formats). |
| Ground control point file did not match the expected file format. View messages for more information. | The ground control point file has errors. | Fix each line listed under *Show Messages* and upload the file again. See [GCP File Format](products/ground-control-points.md#gcp-file-format). |
| Could not find a geo location file with name [name]. | *Upload includes geo location file* was checked, but no file with that name is in the archive. | Check the file name, or uncheck the option. |
| Could not find the specified ground control point file [name] inside the uploaded archive. | *Upload includes ground control point file* was checked, but no file with that name is in the archive. | Check the file name, or uncheck the option. |
| Geo-location file is invalid and cannot be sent to ODM. Upload a new geolocation file and try processing again. View messages for more information. | Processing found problems in the collection's stored geo location file. | Fix the problems listed under *Show Messages*, [upload the file again](products/geologger.md#adding-a-geo-location-file-to-a-collection-with-raw-data-already-uploaded), and process again. |

The problems listed under *Show Messages* include:

| Message | Fix |
|---|---|
| First line must be 'EPSG:4326' | Make the first line of the file exactly `EPSG:4326`, and use longitude and latitude in decimal degrees. |
| Line [n] must contain at least three values. / Expected at least 4 values on line [n]. / Line [n] must contain at least six values. | Add the missing values on that line. The number needed depends on the file format. |
| Line [n] contains a non-numeric longitude. / …latitude. / …value. | Fix the value on that line. Check for text, empty values or "NaN". |
| Line [n] contains a longitude which is out of bounds. Longitude must be between -180 and 180. / …latitude… between -90 and 90. | Check that the coordinates are in decimal degrees and that longitude and latitude aren't swapped. |
| The geo location file did not include a reference to [image] (an image in your collection). … / Image [name] exists in the collection but is not referenced in the geo-location file. | Add a line for that image to the geo location file. Every image in the collection needs a location. |
| Line [n] references an image which does not exist. Image names must match exactly and are case sensitive. | Fix the image name in the ground control point file so it matches an image in the collection exactly. |

## Imagery Processing Errors

These errors happen while Open Drone Map (ODM) processes still, thermal, multispectral or video imagery. See [Processing Imagery](products/generating-products.md#processing-imagery). When ODM reports more than one known problem, the message is "Errors were discovered in ODM output. See messages for more information." and each problem is listed under *Show Messages*.

| Message | Cause | Fix |
|---|---|---|
| ODM ran out of memory during processing. Please contact your technical support. You can also try turning down the quality settings and re-processing. | The processing server ran out of memory. This is more likely with many images, large images, or high quality settings. | Lower *Generated feature quality*, *Generated point cloud quality* or the resolution in the [Advanced Settings](products/generating-products.md#advanced-settings-fields), and process again. If that doesn't work, [contact support](../getting-started/getting-help.md). |
| ODM failed to produce a reconstruction from the image matches. Check that the images have enough overlap, that there are enough recognizable features and that the images are in focus. | ODM couldn't match the images to each other. | Check the image overlap and focus. [Exclude](products/generating-products.md#process-raw-data-into-products) blurry images, or images of the sky or ground, and process again. |
| Couldn't find enough usable images. … | Fewer than two usable images. | Check that the raw tab has at least two images and that they aren't all excluded. |
| Could not connect to the odm server. Please contact your server administrator. | IDM couldn't reach the processing server. | Wait a while, then [try once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| The job encountered an unspecified error. | The processing server returned an error without details. | [Try once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| ODM returned an unexpected response status [status]. … | The processing server returned a status IDM doesn't recognize. | [Contact support](../getting-started/getting-help.md). |
| ODM did not return any results. (There was a problem unzipping ODM's results zip file) | Processing finished, but its results couldn't be read. | [Process once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| The collection can not be processed because its product is locked. | The collection's product is [locked](products/viewing-products.md#locked-products). | Ask an administrator to unlock the product. |
| Job was canceled. | The job was canceled. The status is *Canceled* rather than *Failed*. | Process again if needed. |

### Multispectral Processing Errors

These errors are specific to multispectral imagery. See [Multispectral Imagery](uploading-data/multispectral-imagery.md) for the naming and panel requirements.

| Message | Fix |
|---|---|
| Unable to find image panel. This may effect image color quality. Did you include a panel with naming convention IMG_0000_*.tif? | Include the calibration panel images, named `IMG_0000_*.tif`. |
| Alignment image not found. Did you include an alignment image with naming convention IMG_0001_*.tif? | Include an alignment image set named `IMG_0001_*.tif`. |
| Image [name] does not match the naming convention. … | Rename the images to `IMG_[four numbers]_[band number].tif`. |
| Image alignment has failed. … | Remove bad images (for example, images of the inside of the case or entirely black images), check the panel images, or choose a different alignment image. Make sure the collection is from a single flight. |
| Your upload includes images with naming convention IMG_0000_*.tif, however those images do not appear to be of a panel. … | Make sure `IMG_0000_*.tif` is of the calibration panel, and that there are no other panel images in the upload. |

## LiDAR Processing Errors

These errors happen while processing LiDAR data. See [Processing LiDAR](products/generating-products.md#processing-lidar).

| Message | Cause | Fix |
|---|---|---|
| Lidar processing encountered errors. View messages for more information. | One or more steps failed. | Open *Show Messages* to see the details. |
| Expected a single laz file, but there were [n] | The raw tab has more than one point cloud file. | Keep only one LAS/LAZ file in the collection. |
| Error: Could not determine SRS (Spatial Reference System) for supplied pointcloud. / Error: Could not determine CRS (Coordinate Reference System) for supplied pointcloud. | The point cloud file doesn't say which coordinate system it uses. | Add the coordinate system to the LAS/LAZ file's header, and upload it again. |
| Error: Could not determine bounds for supplied pointcloud. | The point cloud's extent couldn't be read. The file may be empty or damaged. | Check the file in another tool, and upload it again. |
| No point cloud files to be processed. | You selected raster products without *Generate COPC*, and there's no product with the same *Product name* that has a COPC point cloud. The status is *Complete*, but no rasters were created. | Process again with *Generate COPC* selected, or use the *Product name* of an existing product that has a COPC. |

## Product Creation and Upload Errors

These errors happen while IDM creates the files for a product, after processing or when you [upload a product](products/uploading-products.md). Most are listed under *Show Messages*, and the step may still finish with some files missing.

| Message | Cause | Fix |
|---|---|---|
| ODM did not produce an expected file [file]. | Processing didn't create one of the expected outputs, for example because the product type wasn't selected or ODM couldn't create it. | Check whether the product you needed was created. If not, [process once more](#trying-again). If it's still missing, [contact support](../getting-started/getting-help.md). |
| Problem occurred generating cog file. Cog generation failed for [file]. (or a similar message about the overview file or copying the file) | IDM couldn't create the Cloud Optimized GeoTIFF for a file. | Check that the uploaded file is a valid GeoTIFF, then [upload or process once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| Problem occurred generating gdal transform. PNG file did not exist. / …Hillshade file did not exist. / …TIF file did not exist. | IDM couldn't create the preview image or hillshade. | Check that the file is a valid GeoTIFF, then [upload or process once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| Unable to determine the .tif(f) file and the .tif(f).aux.xml file in the archive. | A product uploaded as an archive doesn't contain one .tif file and its matching .tif.aux.xml file. | Put the .tif and its .aux.xml file in the archive, or upload the .tif by itself. |
| Problem occurred running Potree Converter. | IDM couldn't create the files for the 3D point cloud viewer. | Check that the point cloud file is valid, then [upload or process once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |
| Uploaded file ends with cog extension, but did not pass cog validation. | A file named `.cog.tif` isn't actually a Cloud Optimized GeoTIFF. IDM processes it as a regular GeoTIFF instead. | No action needed. |
| An error was encountered while processing the imagery. Something bad happened | A known issue in this release of IDM. It happens when you [upload an ortho](products/uploading-products.md#upload-a-product) as a .tif or .png file with *Process upload* checked. IDM usually creates the Cloud Optimized GeoTIFF and preview image before this error, so the ortho may still be usable. | Open the collection's products tab and check whether the ortho's `.cog.tif` and `.png` files are there. If they are, the ortho can be used. If they aren't, [contact IDM support](../getting-started/getting-help.md). |
| Error while uploading file … / An error was encountered while processing the imagery. … | A file couldn't be stored or processed. The rest of the message gives the reason. | [Upload once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md) with the full message. |
| Unexpected error invoking [tool] … | One of IDM's processing tools failed. The rest of the message comes from the tool. | [Contact support](../getting-started/getting-help.md) with the full message. |

Messages about cleaning up data from ODM or sending email can be ignored. They don't affect your data.

## Timeouts and Interrupted Jobs

| Message | Cause | Fix |
|---|---|---|
| The task timed out (was processing for too long with no updates). Contact your technical support. | A step stopped reporting progress. IDM fails a step after 1 day without updates for ODM processing and for uploads that are finishing, after 3 days for storing ODM results and processing uploaded orthos, and after 7 days for other steps. | [Contact support](../getting-started/getting-help.md) before processing again. |
| The server was shut down while the task was running. | The IDM server restarted during the step. | [Start the upload or processing once more](#trying-again). If it fails again, [contact support](../getting-started/getting-help.md). |

A step with status *Failed* and no message is usually an upload that was canceled.
