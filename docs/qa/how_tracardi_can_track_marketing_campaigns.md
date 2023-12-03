# How can I track marketing campaigns with tracardi?

You can use UTMs.

Tracardi can use UTM (Urchin Tracking Module) parameters to track marketing campaigns. UTM parameters are a
standard way of tagging URLs to track the source, medium, and campaign of traffic. When a user clicks on a URL with UTM
parameters, the parameters are appended to the URL and can be captured by Tracardi.

Here are some of the ways Tracardi can use UTM parameters:

* **Identify the source of traffic:** Tracardi can use the `utm_source` parameter to identify the source of traffic,
  such as a social media platform, email newsletter, or paid advertising campaign.
* **Identify the medium of traffic:** Tracardi can use the `utm_medium` parameter to identify the medium of traffic,
  such as a website, email, or social media post.
* **Identify the campaign:** Tracardi can use the `utm_campaign` parameter to identify the specific marketing campaign
  that generated the traffic.
* **Track campaign performance:** Tracardi can use UTM parameters to track the performance of marketing campaigns by
  measuring metrics such as click-through rates, conversion rates, and revenue generated.

To use UTM parameters with Tracardi, you can simply add them to the URLs that you are using to track your marketing
campaigns. For example, the following URL includes UTM parameters for a Facebook ad campaign:

```
https://www.example.com/product?utm_source=facebook&utm_medium=cpc&utm_campaign=summer-sale
```

When a user clicks on a URL with UTM parameters, Tracardi captures those parameters and associates them with the user's
session. This means that even if the user subsequently clicks on URLs without UTM parameters, their interactions will
still be attributed to the original UTM source. This is because Tracardi maintains the UTM parameters throughout the
user's session.

Overall, UTM parameters are a powerful tool that can be used to track marketing campaigns and gain valuable insights
into their performance. Tracardi can effectively use UTM parameters to track traffic, identify sources and mediums,
measure campaign performance, and optimize marketing efforts.