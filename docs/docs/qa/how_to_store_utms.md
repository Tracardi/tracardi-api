# How to Tracardi stores UTMs?

Tracardi utilizes UTM to help track website traffic and better understand where it is coming from. UTM, which stands for
Urchin Tracking Module, is parameter that is added to the end of a URL, allowing website owners to track various pieces
of information about the source of the traffic, such as the campaign name, the medium used, and the source of the
traffic.

To store UTM information, Tracardi stores the first URL that contains the UTM code in a session. Subsequent clicks by
the customer will retrieve this information from the session, allowing Tracardi to continue tracking the customer's
activity and providing connection with campaign that brought the customer to the page.

In order to ensure that all UTMs are passed through to Tracardi, it is necessary to include them in the URL. This means
that any campaign-specific parameters should be included at the end of the URL, following a question mark (?), with each
parameter separated by an ampersand (&). By doing so, Tracardi will be able to track the source and success of each
campaign, providing valuable data that can be used to optimize future marketing efforts.

## Example

Example URL that could redirect customer from marketing banner to the page.

```
https://www.example.com/?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale&utm_content=text_ad
```

In this example, the UTM parameters are:

* utm_source=google: This indicates that the source of the traffic is Google.
* utm_medium=cpc: This indicates that the medium of the traffic is cost-per-click advertising.
* utm_campaign=spring_sale: This indicates that the traffic is part of a campaign called "Spring Sale."
* utm_content=text_ad: This indicates that the traffic is coming from a text ad.