All files uploaded to the raw tab of a collection must be compressed into a .zip or .tar.gz file.

IDM checks each file in the archive when the upload finishes. The results are shown on the upload's task on the [Workflow Tasks](../workflow-tasks.md) page.

- **Folders:** files inside folders in the archive are uploaded, but the folders are not kept. All files are placed directly in the raw tab.
- **File names:** only letters, numbers, periods (.) and underscores (_) are kept. Any other character, including spaces and hyphens (-), is replaced with an underscore. For example, `IMG 001-a.jpg` is stored as `IMG_001_a.jpg`.
- **Duplicate names:** if two files end up with the same name, because they were in different folders or because of replaced characters, only the first one is kept. The others are skipped with an error message.
- **Unsupported file types:** files that don't match the collection's format are skipped with an error message. See [Supported File Formats](index.md#supported-file-formats). If no files in the archive are supported, the whole upload fails.

:::info

To avoid skipped files, give every file a unique name that uses only letters, numbers, periods and underscores. For example, {props.example ?? 'IMG_001.jpg'} is a valid file name.

:::
