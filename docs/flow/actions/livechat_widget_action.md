# Livechat integration

This plugin injects the LiveChat widget into your web page.

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

Please copy the sting that is at the <LICENSE> position to the plugin form.

If you already have an account log-in to the system and go to __Settings__. Select __Channel/WebSite__. You should see
the same code.

## Form

* License - Copy from LiveChat system
