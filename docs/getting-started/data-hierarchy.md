---
title: Data Hierarchy
sidebar_position: 3
---

In IDM data is organized in a hierarchy. The standard hierarchy is:

- Site
  - Project
    - Mission
      - accessible_support
      - Collection
        - raw
        - video
        - products

This standard way of organizing data provides consistency to how data is stored, how data is classified, and how data is described (metadata) within the hierarchy.

| Level | Description |
|---|---|
| Site | A site is the top most level of the data hierarchy and includes the location of where the data is collected. |
| Project | There can be one or more projects within a site. A project defines the operational project that all work is conducted for. |
| Mission | There can be one or more missions within a project. A mission defines a tactical field operation to collect data in a specific area, for a specific purpose, and within a specific time range. |
| accessible_support | There is only one accessible_support folder per mission. Accessible_support is a storage folder for supporting data (e.g. documents) that are relevant to the mission. |
| Collection | There can be one or more collections within a mission. A collection is where the primary data is organized and operations on that data are made. |
| Collection: raw | The raw directory of a collection stores the data in its most raw form directly after collection. See the [supported file formats](../field-worker/uploading-data/index.md#supported-file-formats). |
| Collection: video | The video directory stores videos that are manually uploaded to a collection's video folder. |
| Collection: products | The products directory stores the products generated from raw data or manually uploaded to the products directory directly. |

Administrators can also configure [custom hierarchies](../administration/custom-hierarchies.md) that can be used to browse sites in the Site Viewer.

## Next Steps

- [Create a site](../field-worker/organizing-data/sites.md)
- [Create a collection](../field-worker/organizing-data/collections.md), including any new projects and missions
