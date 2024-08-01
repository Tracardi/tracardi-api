# What is cross domain click?

A cross-domain click refers to a user interaction where a click on one website leads to navigation to a different
domain. This typically occurs when a user clicks a link on Site A that directs them to Site B.

Cross-domain clicks are important in web analytics, advertising, and user experience design. They can present challenges
for tracking user behavior, as browsers implement various restrictions on cross-domain interactions to protect user
privacy.

# What is cross domain event?

A cross-domain event in Tracardi is a mechanism that allows the transfer of a customer's profile ID from one domain to
another, maintaining continuity of customer identification across different owned websites. Here's how it works:

1. Configuration: Enable the feature by adding `trackExternalLinks` to the tracker settings, specifying the domains you
   own.

2. Link Rewriting: The JavaScript code automatically rewrites links on the page, adding `__tr_pid` (profile ID)
   and `__tr_src` (source ID) parameters to URLs that match the specified domains.

3. Profile Transfer: When a user clicks a modified link, these parameters are passed to the destination domain.

4. Profile Recognition: On the new domain, Tracardi checks for these parameters. If found and valid profile is available
   then it merges the referred profile with an existing local profile

5. Session Management: Tracardi invalidates the session if the profile ID is incorrect and creates a new one if
   necessary.

This approach ensures consistent customer identification across your owned domains, improving user tracking and
analytics capabilities.