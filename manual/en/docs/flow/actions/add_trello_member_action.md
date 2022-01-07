# Add Trello member plugin

This plugin adds a member to a given card in Trello.

## Input
This plugin takes any payload.

## Output
This plugin returns response from Trello API on port **response**, or empty payload
on **error** port, if an error occurs.

## Configuration

#### With form
- Trello resource - Here select your resource, tagged **trello**, containing your API key
  and token.
- URL of Trello board - Here paste in your Trello board's URL. That's the same URL you can see
  on top of your browser window while seeing the board.
- Name of Trello list - Here type in the name of the list containing the card, that you want
  to add a member to.
- Name of your card - Here provide the path to the field containing name of the card that you
  want to add a member to.
- ID of the member - Here provide the path to the field containing the ID of Trello member, that
  you want to add to your card.

#### Advanced configuration
```json
{
  "source": {
    "id": "<id-of-your-trello-resource>",
    "name": "<name-of-your-trello-resource>"
  },
  "board_url": "<full-url-to-your-board-in-trello>",
  "list_name": "<exact-name-of-your-trello-list>",
  "list_id": "<check-note-below>",
  "card_name": "<exact-name-of-your-trello-card>",
  "member_id": "<path-to-the-field-containing-id-of-the-member>"
}
```
**NOTE**: list_id parameter does not matter. Tracardi uses it to store ID of found list.
It should be left as **""** or **null**.

## Warning
If you have two lists with same names on one board, then Tracardi will pick one of them,
without a method of specifying which one will be picked. This rule also applies to the cards.



