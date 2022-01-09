# Add Trello card plugin

This plugin adds a card to a list in Trello.

## Input

This plugin takes any payload object.

## Output

This plugin returns response from Trello API on port **response**, or empty payload
on **error** port, if an error occurs.

## Trello Resource Configuration

To begin working with Trello inside Tracardi, you need an API key and token. These can be typed inside Tracardi resources.
Resources can be found under Traffic -> Outbound resources. More information on how to create a resource can be found below.

### Trello API KEY

Every Trello user is given an API key. You can retrieve your 
API key by logging into Trello and visiting https://trello.com/app-key/.

When the page loads you should see the header __Developer API Keys__ and a __Key__ which looks like this:

```
164a9547a52d0951f3ed781b723d03c1b60d9abd
```

You will need this key to copy to Trello Resource in Tracardi.

### Trello TOKEN

The below the key you will see the following message:

```
  Most developers will need to ask each user to authorize your application. If you are looking to build an application 
  for yourself, or are doing local testing, you can manually generate a Token. 
```

Click on Token link. It will move you to the page with the information on the scope of the token. Click allow at the
bottom of the page. 

You should see the message *You have granted access to your Trello account via the token below* and the token that looks 
like this:

```
b723d03c1b60d9abd164a9547a52d0951f3ed781b164a9547a52d0951f3ed781723d0
```

### Trello Resource

Now it is time to create a Tracardi Trello Resource.

* Go to Traffic -> Outbound resources. 
* Click new resource
* Fill the form and replace __<token>__ with the generated token and __<api-key__> with api key in the credentials section.
* Replace it int the test and production tab. 

*Example of the credentials JSON*

```json
{
  "token": "<token>",
  "api_key": "<api-key>"
}

```

#### Trello Configuration Form

- Trello resource - Select any resource, tagged **trello**, containing your API key
  and token.
- URL of Trello board - Trello board's URL. That's the same URL you can see
  on top of your browser window while visiting the board.
- Name of Trello list - The name of the list that you want to add card to.
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
