# Notes for IDM developers

Found while checking these docs against osmre-uav 1.8.6. Code paths are relative to the osmre-uav repo root.

## Bug: processed ortho uploads always fail

`uasdm-server/src/main/java-gen/stub/gov/geoplatform/uasdm/bus/OrthoProcessingTask.java:114` throws `new RuntimeException("Something bad happened")` unconditionally after creating the COG and PNG for any ortho upload with *Process upload* checked that isn't a .tif + .aux.xml archive. This looks like leftover debugging code. The task ends *Failed* with "An error was encountered while processing the imagery. Something bad happened" (`CollectionUploadEvent.java:305`), although the COG and PNG were already created. The troubleshooting docs list this message as a known issue (users check whether the COG and PNG exist, or contact support). Remove that entry once this is fixed.

## Security: SQL injection in the accounts table filter

`uasdm-server/src/main/java/gov/geoplatform/uasdm/UserInfoPageQuery.java:108,114,124` concatenates the user's filter text straight into SQL (`... LIKE '%" + value.toUpperCase() + "%'`). The parameters map is filled in but not used for these clauses. The account controllers also have no explicit admin check (Runway permissions may cover this; not verified). Please use bound parameters.

## GCP help text shows a format the validator rejects

The upload screen's GCP help text shows a UTM example (`uasdm-ui/src/app/site/component/modal/tus-upload-modal.component.html:250-264`). The validator rejects anything whose first line isn't exactly `EPSG:4326` (`uasdm-server/src/main/java/gov/geoplatform/uasdm/processing/gcp/ODMGroundControlPointFileValidator.java:51`). The docs now say EPSG:4326 only.

## Code that contradicts the changelog, or looks like a bug

1. 1.8.5 (#475) says sites can be created without an organization. The server still throws "Organization is a required field." (`uasdm-server/src/main/java-gen/stub/gov/geoplatform/uasdm/graph/Site.java:105-110`), and the form marks it required (`uasdm-ui/src/app/site/component/modal/entity-modal.component.html:45`).
2. Multispectral/MicaSense: is this path still supported? The multispectral ODM flag is commented out (`uasdm-server/src/main/java/gov/geoplatform/uasdm/odm/ODMService.java:398-400`), and the `uasdm-odm` README calls it legacy.
3. The "Process upload" checkbox never shows for DEM product uploads. The template checks for `'dem'`, but the target is `'dem/dsm'` or `'dem/dtm'` (`tus-upload-modal.component.html:52`).
4. The Project Type isn't saved when a project is created. Every option has `value="projectType"` instead of `[value]` (`uasdm-ui/src/app/site/component/modal/create-collection-modal.component.html:114`). The same bug is in the standalone product group form (`create-standalone-product-group-modal.component.html`). In that form, *Product group name* and *Short Name* have `required` attributes, but the Create button only checks UAV, sensor, collection date and format (`isValid()`).
5. Admins skip the private filter when browsing (`graph/UasComponent.java:1406`), but `UserAccessEntity.hasAccess` has no admin bypass. As a result, an admin who isn't the owner or a collaborator can see a private collection but is blocked by `validateAccess` from product details, map tiles, downloading all files, publishing, locking and deleting its products (`ProductService.java`, `ImageSetService.java`, `CloudOptimizedGeoTiffService.java`). Admins can't manage collaborators either, because grant/remove is owner-only (`UserAccessEntityService.java:79,113`). Which behavior is intended? The docs currently describe this mixed behavior.
6. The in-app Help page's "IDM Documentation" link still points to Confluence (`uasdm-ui/src/app/site/component/help/help.component.html:16`). It should point to the new docs site.

7. Bulk user import (`uasdm-server/src/main/java/gov/geoplatform/uasdm/account/CSVUserImporter.java`):
   - If the CSV has a Role column, a row whose value isn't exactly `admin` gets no role at all (lines 139-149). Should it default to Field Worker? The docs warn about this for now.
   - Rows skipped because the email already exists don't increment `lineNum` (line 128), so the line number in later error messages is too low.

8. Help pages (`uasdm-server/src/main/java/gov/geoplatform/uasdm/service/business/HelpPageBusinessService.java`):
   - The query that picks a user's help page goes through the org and its ancestors with `LIMIT 1` and no ordering (lines ~30-40). If both a bureau and its parent have pages, a user may get the parent's page instead of their own. The docs say users see their own organization's page first.
   - The universal fallback page (organization = null) can't be edited in the UI, because the pencil button is disabled when no organization is selected (`help.component.html`).
   - The TerraFrame help desk (support@terraframe.com) isn't shown anywhere in the app. The old Help Desk section is commented out and still uses `reportEmail = "example@address.com"` (`help.component.ts`). Consider adding a short "IDM Help Desk" line under the bureau content.

9. The old "Create custom layers" feature can't be reached. `LayerPanelComponent` (`uasdm-ui/src/app/site/component/layer-panel/`) isn't used by any template. Is it retired? The docs no longer mention it.

10. The share dialog for a published product lists its "Services" as relative IDM URLs (`api/cog/tilejson.json?path=...`, from `ProductService.getMappableItems`). They're served through `CloudOptimizedGeoTiffService`, which runs an access check. Do they work for the public without signing in to IDM? If not, the share dialog should show the public bucket's COG URLs instead. The docs currently describe them as map tile links "for use in web maps and GIS tools".

11. Processing (`uasdm-ui/src/app/site/component/modal/`):
    - The *Process* button's minimum-image check counts `page.results.length` (the current page of 25, including excluded images), so it can be enabled with fewer than 2 active images (`collection-modal.component.ts:313-318`).
    - The video resolution and video limit inputs both have `name="`"` (`run-process-modal.component.html:167,185`). Their server defaults are null (`ODMProcessConfiguration.java` ~210-223), so the runtime estimate query gets null video values (`ODMRunService.java:97-100`).
    - Client-side defaults (`generateCopc: true`, radiometric calibration) are always overwritten by the server config (`run-process-modal.component.ts:49,74`).
    - The LiDAR checkboxes don't call `configChange()`, so no runtime estimate is ever requested for LiDAR (`run-process-modal.component.html:206-232`).

12. Downloads:
    - *Download All* on the raw tab of a video-format collection sends key "image", which only matches jpg/png/tif, so videos are probably left out (`collection-modal.component.ts:456`, `ComponentHasDocumentQuery.java:104-122`).
    - *Download All* also shows on the image-sets tab and sends `key=image-sets`, which probably gives an empty zip (`collection-modal.component.html:398`).
    - `hasAllZip` is a collection-wide flag (`Product.java:721-731`, set in `ODMZipPostProcessor.java:121`), but *Download All Generated Data* fetches the primary product's all.zip (`ProjectManagementService.java:1365-1375`). After another group is made primary, the button may still show and the download fail.

13. Image sets:
    - `ImageSet.getAll` (~398-413) and `UserAccessEntity.hasAccess` give admins no exception, so admins can't open private-collection image sets or their share links (see #5).
    - The share URL is built from `window.location.origin + "/#"` (`image-set-panel.component.ts:281`), so it breaks when IDM is served under a sub-path.
    - Images without EXIF GPS are silently dropped (`ImageSet.java` ~291-294, 467). That probably includes every LiDAR .las/.laz file, so *Add to image set...* on a LiDAR collection adds nothing, with no error.

14. Accounts and reports:
    - The accounts table columns show sort arrows, but `UserInfoPageQuery.java` has no ORDER BY (~175-193).
    - The "admin can't be deleted" rule is only checked in the browser (`accounts.component.ts:88`); `UserInfo.removeByUser` has no server-side guard.
    - The invite-complete password field has `minlength="5"`, but the server requires 14 (`account-invite-complete.component.html:60`).
    - *Number of Downloads* in the collection report only goes up when a map tile description is requested (`cog/TiTillerProxy.java:327`). Real file downloads aren't counted.
    - `processedImageSizeMb` rounds each file down to whole MB before adding them up, so small images count as 0 (`ProcessingReportService.java:239`).
    - Probable: both CSV exports close the zip stream before the file inside it (`AccountCSVExportService.java:43`, `SessionEventCSVExportService.java:40`).
    - The collection report column is "Date of Create" in the UI (`reports.component.ts:60`) but "Date of Creation" in the CSV (`CollectionReport.java:861`).

15. STAC items (`uasdm-server/src/main/java-gen/stub/gov/geoplatform/uasdm/graph/Product.java`):
    - The hierarchy data on a STAC item comes from the first GeoPrism Registry sync profile, read with no ordering (1006-1010).
    - For a product attached to a mission, Collection is set to the mission's name and Mission is never set (993, with `UasComponent.getAncestors()`).
    - If a product has no metadata, the STAC date falls back to roughly the time it was published (1036).
    - `platform` and `mission` are written without the `geoplatform:` prefix the other custom properties have (`model/StacItem.java:306,318`). This may be intentional.

16. Custom hierarchies (`uasdm-ui/src/app/admin/component/labeled-property-graph-sync/labeled-property-graph-sync.component.ts`): *Create tiles* silently does nothing when the profile has no version. The Edit button is commented out, so `handleOnEdit` can't be reached here or on the organization profile page.

17. The *Upload includes ground control point file* checkbox shows on product (ortho and DEM) uploads, not just raw uploads. Its condition is `(metadata.processOrtho || metadata.processDem) && !isVideo()` (`tus-upload-modal.component.html:237`), and both flags default to true for every upload (`tus-upload-modal.component.ts` `init()`). GCP files are only used when processing raw imagery, so the checkbox probably needs `uploadTarget === 'raw'`.

18. Error reporting:
    - LiDAR raster generation without a COPC (none in the job and none in a product with that name) ends *Complete* with "No point cloud files to be processed." (`lidar/LidarProcessingTask.java:108-116,148-152`). Nothing was created, so this should probably be *Failed* with a message telling the user to select *Generate COPC*. The docs currently explain the *Complete* behavior.
    - The *Show Messages* list shows INFO, WARNING and ERROR actions in one table with no type column (`tasks-panel.component.html:84-103`), so users can't tell errors from warnings.
    - "The filename [name] contains special characters which will be replaced with an underscore." is logged as an ERROR action (`UploadValidationProcessor.java:443`), although nothing fails. It should probably be a WARNING.
    - "The file [name is not a valid image file]": the closing bracket is in the wrong place (`UploadValidationProcessor.java:434`).
    - "…try processsing again" typo in `ODMGeoLocationProcessConverter.java:161`.

## UI text bugs

- "Matcher Nieghbors" (`run-process-modal.component.html:89`). CHANGELOG 1.7.0 says this was fixed.
- Garbled sentence in the upload screen: "...or apostrophes are allowed or apostrophes will be replaced with underscores" (`tus-upload-modal.component.html:167-169`).
- The image set name error says "Product name is required." (`create-image-set-modal.component.html`).
- The Export Users zip contains a CSV named `session-event-export.csv` (`uasdm-server/src/main/java/gov/geoplatform/uasdm/service/request/AccountService.java:143`).
- "The server responsed" (`labeled-property-graph-sync.component.ts`).
