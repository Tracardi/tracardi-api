# Searching (after 0.8.2)

Filtering in version 0.8.2 was simplified and has the following operations.

1. **Comparison Conditions:**
    - Basic comparison between a field and a value:
        - `fieldName > "value"` or `product_price <= 100.50` or - `active = true`
    - Text search
        - `field.name = "value"` (text search + exact match, finds sentence with `value` or fields with `value`)
        - `field.name == "value"` or `field.name is "value"`(exact text search)
        - `field.name ~ "value"` or `field.name match "value"` (full text search only)
    - Text with wildcards
        - `field.name = "value*"` (wildcard search + text search: searches for any string starting with `value`)
        - `field.name == "value?"` (wildcard search in field: searches for any string starting with `value` + 1 character)
        - `field.name != "value"` (all but `value` search)
    - Boolean values search:
        - `is_active = TRUE`
        - `is_deleted = FALSE`
    - Checking for NULL values:
        - `product_name IS NULL`
    - Basic numeric value conditions:
        - `quantity > 10`
        - `quantity = 10.01`
        - `quantity < 10`
        - `quantity >= 10`
        - `quantity != 10`
        - `quantity <= 10`
    - Using arrays in conditions:
      - `categories IN ["Electronics", "Clothing", "Books"]`
      - `product_id NOT IN [101, 102, 103]` (TO BE IMPLEMENTED)
      
2. **Logical Operators:**
    - Combining conditions with `AND` and `OR`:
        - `sales > 1000 AND region = "North"`
        - `age >= 18 OR (gender = "Female" AND has_children = TRUE)`

3. **Grouping:**
    - Using parentheses to group conditions:
        - `(age < 30 AND income > 50000) OR (region = "West" AND product = "Widget")`

4. **Field Existence:**
    - Checking for the existence or non-existence of a field:
        - `customer_email EXISTS`
        - `employee_manager NOT EXISTS`

5. **Range Conditions:**
    - Comparing a field with a range:
        - `temperature BETWEEN 68 AND 72`
        - `price BETWEEN 10.99 AND 19.99`

6. **Field Equality:**
    - Comparing two fields:
        - `order_total_amount = payment_total_amount`
        - `start_date < end_date`

7. **Field Functions:**
    - Applying functions to fields:
    - `DATE(order_date) = "2023-01-15"` (TO BE IMPLEMENTED)
    - `UPPER(product_name) = "WIDGET"` (TO BE IMPLEMENTED)

8. **Compound Value and Field Conditions:**
    - Using compound values and fields:
    - `category("Electronics") = price + tax` (TO BE IMPLEMENTED)
    - `order_status("Shipped") = customer_name` (TO BE IMPLEMENTED)

9. **Time Conditions:**
    - Expressing time conditions:
    - `time_elapsed >= 2d` (greater than or equal to 2 days) (TO BE IMPLEMENTED)
    - `duration < 1h` (less than 1 hour) (TO BE IMPLEMENTED)


---
This documentation answer the following questions:

* How to search for profile, session, and events in Tracardi GUI
* How to search data in Tracardi?
* How does Tracardi's query parser work?
* What is a query condition?
* What is the syntax for searching, filtering in Tracardi?
