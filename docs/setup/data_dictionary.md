# Data Dictionary

This document describes the main fields used by SafeCity Vision.

| Field | Type | Description |
|---|---|---|
| `Timestamp` | datetime | Date and time when the incident occurred. |
| `Latitude` | float | Geographic latitude of the incident. |
| `Longitude` | float | Geographic longitude of the incident. |
| `Crime_Category` | string | Normalized category or type of crime. |
| `Description` | string | Additional incident description when available. |
| `Hour` | integer | Extracted hour from `Timestamp`, from 0 to 23. |
| `DayOfWeek` | integer | Extracted weekday, where 0 is Monday and 6 is Sunday. |
| `Month` | integer | Extracted month, from 1 to 12. |
| `Temperature` | float | Weather feature or simulated weather proxy. |
| `Is_Raining` | integer | Binary weather indicator, where 1 means raining. |
| `Dist_to_Transit` | float | Distance-to-transit or urban-context proxy feature. |

## Notes

- Raw data from different cities should be converted to the normalized schema before modeling.
- Derived fields should be regenerated during enrichment rather than manually edited.
- Sensitive personally identifiable information should not be stored in this project.
