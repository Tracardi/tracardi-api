# Profile segmentation

## Introduction

A segment is a group of customer profiles that have been identified as having similar characteristics or behaviors. It
is the result of segmenting customer profiles. Segmentation is the process of dividing a customer base into smaller
groups with similar characteristics. These segments can be described by a simple logical rule or by more complex AI
models.

In the Tracardi system, a segment is a part of the customer profile, and it can be used in the segmentation workflow. A
segment is typically represented by a simple sentence that describes the group, for example "Customers with a high
volume of purchases". This group of customers, who have a high volume of purchases, can be targeted with specific
marketing campaigns or other customer-centric actions based on their behavior and characteristics.

## How to segment

The segmentation process is started automatically after each update of profile data, or it can be initiated manually
within a workflow by placing the action "Segment profile".

In the Tracardi, the criteria for segmentation are defined in the segmentation tab. This means that when a segmentation
is defined, it can be used in multiple workflows without the need to change anything in the workflows themselves. If
segmentation is enabled, it will be run automatically after each workflow is completed.

## Segmentation

A segment consists of a name and segmentation criteria. At the time of segmentation the name will be converted into the
segmentation id. Name will be lower-cased and spaces will be replaced with dashes.

## Segmentation criteria

A profile will be attached to a given segment if the data contained in it meet the defined segment criteria.

Criteria are nothing more than a logical rule. For example, a user must visit our website at least 10 times.

For example:

Segment named: `Frequent visitor`. He has a criterion that looks like this:

``
profile@stats.visits > 10
``

#### Result of segmentation

If the profile in its statistical data has been saved that the number is more than 10, then the segmentation id will be
added in the profile in the segments item, which will look like `frequent-visitor`.

A profile can belong to multiple segments. 




