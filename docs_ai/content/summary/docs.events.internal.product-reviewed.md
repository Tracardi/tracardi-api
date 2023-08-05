This documentation provides information about the event "Product Reviewed". This event should be used when a customer provides a review of a product. The review can contain feedback, comments, or suggestions regarding the product. The event can be used to analyze customer satisfaction and improve the product. 

The expected properties for this event are review, rate, and id. All properties are optional and if any property is missing it will not be processed and no error will be reported. The example usage provided is when a customer has written a review for a product they recently purchased. 

Auto indexing is also discussed in the documentation. This is a structure that organizes the data by copying information from the different parts of the data and putting it into a specific format that can be used to analyze and group the data. This table describes which event property will be copied to event traits. The event traits are ec.product.id, ec.product.review, and ec.product.rate. 

Finally, the documentation states that data will not be copied to profile. An example JSON is also provided.