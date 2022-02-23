# Fetch funnel from MixPanel plugin

This plugin fetches funnel created in MixPanel, for current profile. 


## Requirements

This plugin requires MixPanel account with created project, and a service account
created for this project. Credentials for the service account must be included in 
resource, as well as server prefix (either EU or US).

## Input

This plugin takes any payload as input.

## Outputs

This plugin outputs fetched funnel on port **success**, or an error message (if it's known one) on port
**error** if one occurs.

## Configuration

#### Form fields

- MixPanel resource - Select your MixPanel resource, containing service account username, password
  and server prefix.
- Project ID - Here paste your MixPanel project ID. You can find it under Settings > Project settings > 
  <your-project-name>. 
- Funnel ID - Paste in your MixPanel funnel ID. You can find it in URL when 
  inspecting your funnel (**...app/funnels#view/<funnel-id>/...**).
- Lower time bound - Here type in the path to the date (or the date itself). That will
  the lower time bound for your funnel. It can be a timestamp, a datetime, or a string in form of **YYYY-MM-DD**.
  Other formats are not supported.
- Upper time bound - That's the upper bound for your funnel. It's optional. It works according to same rules
  as Lower time bound.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-mixpanel-resource>",
    "name": "<name-of-your-mixpanel-resource>"
  },
  "project_id": "<id-of-your-mixpanel-project>",
  "funnel_id": "<id-of-your-mixpanel-funnel>",
  "from_date": "<path-to-lower-time-bound>",
  "to_date": "<optional-path-to-upper-time-bound>"
}
```