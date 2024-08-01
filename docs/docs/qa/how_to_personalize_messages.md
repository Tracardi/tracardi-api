# How to personalize messages?

Tracardi offers a Template Plugin that simplifies the process of creating templates and referencing data within them.
The plugin allows you to generate dynamic text content that can be utilized in various plugins, such as SMS77, SMTP
email, Mailchimp messages, and more.

To leverage the Template Plugin in Tracardi, follow these steps:

* __Create a Template__: Start by creating a template using the Template Plugin. This plugin provides an interface where
  you can design your template and use placeholders for the dynamic data.
* __Use Data Placeholders__: Within the template, you can define data placeholders using {{ }}. Place a referenced data
  inside, for example {{ event@properties.name }}. These placeholders will represent the dynamic information that will be
  replaced when the template is processed.
* __Use Template__: After creating the template, you can use it as a data source in various plugins within
  Tracardi. For example, you can reference the template in the SMS77 plugin to generate personalized SMS messages, or in
  the SMTP email plugin to create customized email content.

---
This document also answers the questions:
- How to personalize SMS77 messages?
- How to send personalized emails?
- How to use templates?
- How to use data placeholders in text?
- How to customize the messages?
- Can messages be dynamic?