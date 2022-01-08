# Add Trello card plugin

This plugin adds a card to a list in Trello.

## Input

This plugin takes any payload object.

## Output

This plugin returns response from Trello API on port **response**, or empty payload
on **error** port, if an error occurs.

## Configuration

#### Form fields

- Trello resource - Select any resource, tagged **trello**, containing your API key
  and token.
- URL of Trello board - Trello board's URL. That's the same URL you can see
  on top of your browser window while seeing the board.
- Name of Trello list - The name of the list that you want to add card to.
  In fact, Trello requires its ID, but Tracardi will find it for you, using provided list name.
- Name of your card - Dot path to field that contains text. This text will become your
  card's name.
- Card description - Card description. Here you can type in regular text, or 
  dot template, so for example **Customer {{profile@pii.name}} has ordered something**.
  This configuration parameter is optional.
- Card link - You can add link to your card as an attachment. This configuration parameter is optional.
- Card coordinates - You can add coordinates to your Trello card to use in Trello app. The path should
  point at an object in payload, containing fields called **latitude** and **longitude**. This
  feature works well with **GeoIp service** plugin. This configuration parameter is optional.
- Card due date - You can add due date to your card. This parameter is a path to a field
  containing date. Best format to use is UTC, but for example **YYYY-MM-DD** should also work.
  This configuration parameter is optional.

#### Advanced JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-trello-resource>",
    "name": "<name-of-your-trello-resource>"
  },
  "board_url": "<full-url-to-your-board-in-trello>",
  "list_name": "<exact-name-of-your-trello-list>",
  "list_id": "<check-note-below>",
  "card": {
    "name": "<dot-path-to-card-name-or-name-itself>",
    "desc": "<card-description>",
    "urlSource": "<url-that-you-want-to-attach-to-your-card>",
    "coordinates": "<dot-path-to-object-containing-coordinates>",
    "due": "<dot-path-to-field-containing-due-date>"
  }
}
```
**NOTE**: list_id parameter does not matter. Tracardi uses it to store ID of found list.
It should be left as **""** or **null**.

## Warning

If you have two lists with same names on one board, then Tracardi will pick one of them,
There is no method of specifying which one will be picked.
