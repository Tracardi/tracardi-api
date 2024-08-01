# Passing Profile ID in the URL Between Owned Domains (Cross Domain Event / Cross Domain Identification)

This feature is beneficial if you want to ensure that the same profile ID is created within owned domains. For example,
if you own two domains that are linked and you click and redirect user from one domain to another domain, the same
profile ID should be used. The JavaScript code can be used to rewrite links on the page to contain the current profile
and pass it to destination domain. However, the profile must first exist in the system.

System then will recognize that the profile already exists and is redirected from other domain and will
connect profiles.

## Default Behavior (without Cross-Domain Events):

1. First Visit: A random profile ID is created for a new visitor.
2. Subsequent Visits: The existing profile ID is reused.
3. Merging Profiles:
    - Only occurs when the user provides identifiable data (e.g., email during sign-in).
    - Without such data, profiles remain separate.

## Cross-Domain Events Advantage:

1. Prevents Multiple Profiles: Avoids creating separate profiles for the same user across different domains.
2. Automatic Merging: The system connects profiles based on the sequence of events, even without explicit merging keys
   like email.
3. Improved Tracking: Maintains a single user profile across all your owned domains.

This feature is particularly useful when you can't rely on traditional merging methods (like email sign-ins) to connect
user profiles across your different websites.

!!! Note

        This is commercial feature

## Javascript Configuration

To enable the "passing of profile ID" feature:

1. Add `trackExternalLinks` to the `settings` object in your Tracardi configuration:

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

2. This configuration automatically modifies `<a>` tags on your page, adding `__tr_pid` (profile ID) and `__tr_src` (
   source ID) parameters to links ending with the specified domains.

3. When a user navigates between your domains, Tracardi processes the profile data as follows:

   a. Checks for valid referrer data (profile ID and source ID).
   b. If valid, marks for merging the referred profile with the existing local profile.
   c. Logs warnings for invalid profile or source IDs.
