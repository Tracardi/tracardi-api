# Passing Profile ID in the URL Between Owned Domains

This feature is beneficial if you want to ensure that the same profile ID is created within owned domains. For example,
if you own two domains that are linked and you click and redirect user from one domain to another domain, the same
profile ID should be used. The JavaScript code can be used to rewrite links on the page to contain the current profile
and pass it to destination domain. However, the profile must first exist in the system.

System then will recognize that the profile already exists and is redirected from other domain and will 
connect the same profile to the customer even if customer never visited this page before.

Please note that default behaviour (without `passing of profile ID` enabled) would be to create a random profile ID
if customer never visited the page before. And later merge the profile if customer provides data that can be used 
for this. 

To activate `passing of profile ID` feature, add `trackExternalLinks` to `settings`:

```javascript title="Example" linenums="1" hl_lines="10-12"
    const options = {
      tracker: {
        url: {
            script: 'http://localhost:8686/tracker',
            api: 'http://localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        settings: {
          trackExternalLinks: ['example.com', 'tracardi.com']
        }
    }
}
```

This will automatically update all `A.href` links on the page with the `__tr_pid`, `__tr_src` parameter, which will
contain the current profile ID, source ID respectively, if the A.href URL end with any of the defined domains
in `trackExternalLinks`. In our example it is 'example.com' and ,
'tracardi.com'.

Here is the explanation how Tracardi treats referenced profiles IDs.

Tracardi checks if there is referer data containing a profile ID and source ID. If it exists and is valid, it merges the
referred profile with the existing profile in the local storage on the visited page (domain). If there is no existing
profile on visited page, it replaces current generated profile ID with the referred one.

It also invalidates the session if it has the wrong profile ID and creates a new session if none exists. If the referred
profile ID is invalid, it logs a warning. Similarly, if the referred source ID is invalid, it logs a warning and shows
the error message.