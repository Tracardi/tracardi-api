# LiveChat widget

The LiveChat widget plugin integrates the LiveChat messaging feature into webpages. This widget facilitates real-time
chat between the website visitors and the support or sales teams.

# Version

0.7.3

## Description

This plugin is used to inject the LiveChat widget, a popular customer support chat tool, into a webpage. The widget
allows website visitors to communicate directly with customer support or sales teams. It requires a LiveChat license
number for activation. Once configured, the plugin appends a JavaScript snippet to the webpage, activating the LiveChat
widget. This enhancement can significantly improve user engagement and customer support efficiency.

# Inputs and Outputs

- __Inputs__: The plugin accepts a payload, typically containing the data necessary for the widget's operation.
- __Outputs__:
    - __response__: Outputs the payload back after processing. The main function of this plugin is to append the LiveChat
      widget to the page, not to alter the payload.
    - __error__: Outputs in case of any execution error.

# Configuration

- __License__: Your LiveChat license number, a crucial element for enabling the widget on your webpage.

# How to obtain license number

In order to integrate this application with your webpage you will need to open an account at www.livechat.com. During
sign-up, you will be presented with the following code:

```html
<!-- Start of LiveChat (www.livechat.com) code -->
<script>
    window.__lc = window.__lc || {};
    window.__lc.license = <LICENSE>;
    ;(function(n,t,c){function i(n){return e._h?e._h.apply(null,n):e._q.push(n)}var e={_q:[],_h:null,_v:"2.0",on:function(){i(["on",c.call(arguments)])},once:function(){i(["once",c.call(arguments)])},off:function(){i(["off",c.call(arguments)])},get:function(){if(!e._h)throw new Error("[LiveChatWidget] You can't use getters before load.");return i(["get",c.call(arguments)])},call:function(){i(["call",c.call(arguments)])},init:function(){var n=t.createElement("script");n.async=!0,n.type="text/javascript",n.src="https://cdn.livechatinc.com/tracking.js",t.head.appendChild(n)}};!n.__lc.asyncInit&&e.init(),n.LiveChatWidget=n.LiveChatWidget||e}(window,document,[].slice))

</script>
<noscript><a href="https://www.livechat.com/chat-with/<LICENSE>/" rel="nofollow">Chat with us</a>, powered by <a
        href="https://www.livechat.com/?welcome" rel="noopener nofollow" target="_blank">LiveChat</a></noscript>
<!-- End of LiveChat code -->
```

Please copy the sting that is at the __LICENSE__ position to the plugin form.

If you already have an account log-in to the system and go to __Settings__. Select __Channel/WebSite__. You should see
the same code.

# JSON Configuration

Example configuration:

```json
{
  "license": "your-livechat-license-number"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

Plugins like the Livechat widget, which fall under the "UIX Widgets" category, require a synchronous event. It will not
work if sent event is asynchronous.

# Errors

- "License can not be empty.": This error occurs when the LiveChat license number is not provided in the plugin
  configuration. The license number is essential for the widget's operation.
- General script-related errors might occur, usually related to the execution of the appended JavaScript in the webpage
  environment. These errors could arise from conflicts with other scripts or issues in the webpage's structure.
