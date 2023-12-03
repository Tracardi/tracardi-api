# What is the difference between the segment and audience?

In the context of Tracardi, "segment" and "audience" are two terms that are often used, but they refer to
different concepts:

1. Segment: A segment refers to a specific group of people within your broader customer base or database who share
   certain characteristics or behaviors. Segmentation involves dividing your market into subsets based on criteria like
   demographics (age, gender, income), psychographics (interests, values, lifestyle), behavior (purchase history,
   product usage), or geography. The purpose of segmentation in marketing automation is to target these groups with
   tailored messages or offers that are more likely to resonate with them. For example, you might have a segment of
   customers who have previously purchased a specific product and you want to target them with a promotional offer for a
   related product.

2. Audience: An audience, on the other hand, can be thought of as the larger group of people you are trying to reach
   with your marketing efforts. This could include your current customers, potential customers, and other stakeholders.
   In marketing automation, the term "audience" is often used more broadly and can encompass multiple segments. It's
   about the total group of people who will be exposed to your marketing campaign. For instance, your audience for a
   digital ad campaign could include several different segments, such as new customers, returning customers, and
   prospects who have engaged with your content but haven't made a purchase.

Segmentation has a dynamic nature. That means that individuals can move from one segment to another over time. This
dynamism is a critical aspect of segmentation and is based on changes in customer behavior, preferences, or other
defining characteristics. Here's how it works:

1. **Behavioral Changes**: Customers' behaviors can change due to various factors such as life events, changing
   interests, or evolving needs. For instance, a customer who was in a segment characterized by infrequent purchases
   might start buying more regularly, thus moving to a segment of frequent buyers.

2. **Data Updates**: As new data is collected, the profiles of customers get updated. This continuous influx of data can
   lead to customers being reclassified into different segments. For example, updating demographic information like age
   or income can shift a customer into a new segment more aligned with their current status.

3. **Engagement Levels**: A change in how customers interact with your brand can also trigger a shift in segments. For
   example, a customer who increases their engagement with your digital content or marketing emails might move into a
   segment characterized by higher engagement levels.

4. **Purchase History**: Changes in purchasing behavior, such as the types of products bought or the frequency of
   purchases, can result in movement between segments. For instance, a customer might move from a "one-time purchaser"
   segment to a "repeat customer" segment.

5. **Automated Re-segmentation**: Many marketing automation systems are designed to automatically re-segment customers
   based on predefined rules or machine learning algorithms. This automation ensures that segments are always up-to-date
   and reflective of the latest customer data and behaviors.

From the technical point of view that means the segments are constantly re-evaluated, and a segment is just a tag that
tells that some customer belongs to defined segment.

In contrast to segments, audiences in the context of marketing automation and data management are generally more static
and purpose-specific. Unlike segments, which are continuously updated based on ongoing data collection, time passing,
and behavioral
changes, audiences are typically created for a specific purpose as a data query at a specific point in time. Here's a
detailed look
at the audience properties:

1. **Purpose-Specific Creation**: An audience is often created for a particular marketing campaign or business
   initiative. This means that the data used to define an audience is queried and compiled to meet the specific
   requirements of that campaign or initiative. Once the audience is defined, it does not automatically update customer
   tags or change
   unless manually revised for a new purpose, or when data is queried again.

2. **Lack of Automatic Re-evaluation**: In contrast to segments that are often re-evaluated and updated automatically as
   new data comes in, audiences do not undergo this automatic re-evaluation. The data set for an audience reflects the
   criteria and information available at the time of its creation. Basically the audience is the information on how to
   query data to compose the required set of customers.

4. **Targeted for Specific Campaigns**: Audiences are often used for specific, time-bound marketing campaigns, events,
   or promotions. For example, an audience might be created for a holiday season marketing campaign, using data relevant
   to that particular time period and campaign objective. Audiences are used for customer activation using external
   systems. Once sent to external system then stay the ave and do not evolve.

5. **Manual Intervention for Updates**: If there is a need to update an audience in the external system, such as
   including more recent customer data or adjusting the criteria, this usually requires manual intervention. The
   marketer would need to re-query the database to create an updated audience. This approach contrasts with the fluid
   nature of segments, which are continuously updated and in any give time we can tell if customer belongs to given
   segment or not. This is not possible with audiences.

In summary, audiences in a technical marketing context are less dynamic than segments. They are created for specific
purposes and remain largely unchanged unless manually updated or redefined. 