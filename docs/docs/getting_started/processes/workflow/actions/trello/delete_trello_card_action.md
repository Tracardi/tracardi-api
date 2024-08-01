# Remove Trello card plugin

This plugin removes a card from given list in Trello.

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

#### Trello Plugin Form

- Trello resource - Select your resource, tagged **trello**, containing your API key
  and token.
- URL of Trello board - Paste in your Trello board's URL. That's the same URL you can see
  on top of your browser window while seeing the board.
- Name of Trello list - Type in the name of the list that you want to delete a card from.
  In fact, Trello requires its ID, but Tracardi will find it for you, using provided list name.
- Name of your card - That's the name of the card that you want to delete. It can be either a name or a dot path to the 
  data inside event, payload, etc.

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
}
```
**NOTE**: list_id parameter does not matter. Tracardi uses it to store ID of found list.
It should be left as **""** or **null**.

## Warning
If you have two lists with same names on one board, then Tracardi will pick one of them,
without a method of specifying which one will be picked. This rule also applies to the cards.


