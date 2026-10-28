---
title: Session Event Log
sidebar_position: 10
---

The *Session Event Log* section of the System Configuration page allows administrators to monitor sign-ins to IDM. To open it, choose *System Configuration* from the navigation menu.

The table lists the most recent events first, 20 per page. Use the page numbers under the table to see older events.

| Column | Description |
|---|---|
| Username | The username or email address entered when signing in. For sign-ins through single sign-on, this is the user's email address. |
| Bureau | The organization the user belonged to when they signed in. It is blank for failed sign-ins. |
| Event Date | The date and time of the sign-in, in your browser's time zone. |
| Event Type | `LOGIN_SUCCESS` for a successful sign-in, or `LOGIN_FAILURE` for a failed one. |

Only sign-ins are recorded. Sign-outs and other actions are not logged.

## Exporting the Log

Click the *Export Session Log* button to download the whole log. The download is a zip file, `idm-session-log.zip`, containing a CSV file named `session-event-export.csv` with one row per event and these columns:

| Column | Description |
|---|---|
| username | Same as *Username* in the table. |
| eventType | `LOGIN_SUCCESS` or `LOGIN_FAILURE`. |
| eventDate | The date and time of the event in UTC, in ISO 8601 format (for example `2025-03-14T17:05:22.000Z`). |
| organization | Same as *Bureau* in the table. |

The rows in the export are not guaranteed to be in date order. Sort the file by *eventDate* after opening it.
