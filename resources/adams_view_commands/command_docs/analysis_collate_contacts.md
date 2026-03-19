# analysis collate_contacts

Sets the tolerance value for track data and reference marker with respect to which contact data is computed.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `analysis_name` | Existing analysis | Specifies an existing analysis. |
| `contact_name` | Existing contact | Specifies an existing contact. |
| `tolerance` | Real | Specifies the distance used to decide if two successive impacts of two geometries used by the same contact belong to the same track. If you do not provide it, Adams Solver computes the tolerance, which can take a long time. |
| `reference_marker` | Existing marker | Specifies the marker with respect to which the track data is computed. Otherwise, the track data is in the global reference frame. |
