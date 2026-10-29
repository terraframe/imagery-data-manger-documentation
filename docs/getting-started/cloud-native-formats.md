---
title: Cloud Native Formats
sidebar_position: 3.5
---

IDM stores the products it creates in *cloud native* formats. This page explains what that means, why IDM uses them, and where you'll find them in IDM.

## What Cloud Native Means

Imagery, elevation and LiDAR files are often several gigabytes each. With traditional file formats, you have to download the whole file before you can look at any part of it.

Cloud native formats organize a file so that software can read just the part it needs, directly from cloud storage over the internet. To show a small area of an ortho mosaic at a given zoom level, a map only reads the few pieces of the file that cover that area. The rest of the file is never downloaded.

The files are still ordinary, standard files. Desktop tools such as QGIS and ArcGIS can open them like any other GeoTIFF or LAZ file.

## Why IDM Uses Them

IDM was built for teams that work in remote locations with limited, unreliable internet, and that need to share large datasets across an organization. Cloud native formats support that directly:

- **Work in low bandwidth.** You can view products on the map, zoom in and pan around without downloading the full files. Only the data on your screen is transferred.
- **One copy serves every use.** The same file is used for map display, download, analysis and public sharing. IDM doesn't have to build and store separate map tiles or preview copies, so there's less to keep in sync and less storage to pay for.
- **Easy sharing.** Once a product is [published](../field-worker/publishing-products.md), anyone can stream it straight from its public URL into their own GIS software, without asking for a copy or downloading the whole file. See [Public Image Services](../administration/public-image-services.md).
- **Open standards.** The formats are open, widely supported standards, so data stored in IDM isn't tied to IDM and stays usable by other tools and agencies.
- **Findable data.** Published products are described with STAC, a standard catalog format, so they can be searched and found alongside data from other systems. See [Know-STAC](../know-stac.md).

## The Formats IDM Uses

| Format | Used for | Created when |
|---|---|---|
| **Cloud Optimized GeoTIFF (COG)**, files ending in `.cog.tif` | Ortho mosaics and elevation models (DSM, DTM) | IDM [processes imagery](../field-worker/products/generating-products.md#processing-outputs), or you [upload an ortho or DEM](../field-worker/products/uploading-products.md#upload-fields) |
| **Cloud Optimized Point Cloud (COPC)**, files ending in `.copc.laz` | LiDAR point clouds | You [process a LiDAR collection](../field-worker/products/generating-products.md#lidar-options) with *Generate COPC* |
| **Potree point cloud tiles** | The 3D point cloud viewer | IDM processes imagery into a point cloud, or you upload a point cloud with *Enable Potree viewer for point cloud* |
| **SpatioTemporal Asset Catalog (STAC)** | Descriptions of published products, with links to their COG files | You [publish a product](../field-worker/publishing-products.md) |

When you upload an ortho or DEM, IDM keeps your original file and creates a COG alongside it. If you uncheck *Process upload*, the original is stored as-is, without a COG, and won't display on IDM's map.

## Where You'll See Them in IDM

| Where | How cloud native formats are used |
|---|---|
| [Site Viewer map](../field-worker/products/viewing-products.md#viewing-products-in-the-site-viewer) | *Aerial* and *Hillshade* draw ortho and elevation layers by streaming tiles from the product's COG as you pan and zoom. *3D* streams the point cloud into the Potree viewer. |
| [Products tab](../field-worker/products/viewing-products.md#viewing-products-in-a-collection) of a collection | Lists the `.cog.tif` and `.copc.laz` files with the rest of each product's files, ready to download. |
| [Publishing](../field-worker/publishing-products.md) | Copies the product's files, including its COGs, to public cloud storage, and creates a STAC item that links to them. |
| [Public Image Services](../administration/public-image-services.md) | Explains how to stream published COGs into QGIS and other GIS software. |
| [Know-STAC](../know-stac.md) | The public catalog where published products' STAC items can be searched. |
| [LiDAR processing](../field-worker/products/generating-products.md#processing-lidar) | Tree canopy cover, ground surface model and terrain model rasters are created from the COPC point cloud. |
