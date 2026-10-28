---
title: Introduction
sidebar_position: 1
slug: /
---

The Imagery Data Management (IDM) platform was developed by Zivaro for the Office of Surface Mining Reclamation and Enforcement (OSMRE) to automate imagery management and processing workflows. OSMRE wanted to reduce effort performing routine IT tasks and free available resources to perform more remote sensing. Prior to IDM, the effort to ingest, archive, process and share numerous types of data, including terrestrial LIDAR, UAS imagery, photography and sensor data was labor intensive. Since OSMRE operates in many remote locations with unreliable access to the internet and limited bandwidth, uploading and managing remote sensing outputs to the cloud was not practical. Large amounts of data ended up siloed on multiple laptops, resulting in imagery not being used due to the inability to find them across the organization.

The IDM platform solves these problems by providing a cloud-based solution that streamlines the upload, metadata capture, management, and processing workflows of data obtained by remote sensors. Large amounts of data can be uploaded even when the internet is poor and unreliable. It also automates the ingest process, data delivery, and capture of the standard specifications for metadata and data formats required by the USGS EROS Center. The IDM was designed with extensibility in mind. Since it is built entirely out of open-source components, common functionality can be shared across organizations. This will result in cost savings and productivity gains as it is adopted by additional bureaus and agencies.

## Key Takeaways

The Imagery Data Management platform:

- is designed to work in low bandwidth environments
- is built on open source software
- uses Open Drone Map (ODM) for image processing
- supports multispectral imagery from MicaSense, Sentera, and DJI sensors
- enforces the USGS documentation/standard data model

## Application URL

- <Deployment value="appUrl" />

## Application Version Info

This documentation covers IDM <DocsVersion />. Use the version menu at the top of the page to read the documentation for a different release.

The exact IDM and Open Drone Map (ODM) versions running in the application are listed on its System Information page: <Deployment value="appUrl" path="#/admin/system-info" />. Administrators can also open it by choosing *System Info* from the navigation menu. The page also links to the release notes.

## Using This Documentation

- **[Getting Started](getting-started/accessing-idm.md)** covers logging in, a tour of the Site Viewer, how data is organized in IDM, and [where to get help](getting-started/getting-help.md).
- **[Field Worker Guides](field-worker/index.md)** are step-by-step instructions for organizing, uploading, processing, sharing, and downloading data.
- **[Administrator Guide](administration/index.md)** covers configuring IDM and managing its users.
- **[Know-STAC](know-stac.md)** describes the public catalog that published IDM products are registered in.
- **[Frequently Asked Questions](faq.md)** has answers to common issues.
