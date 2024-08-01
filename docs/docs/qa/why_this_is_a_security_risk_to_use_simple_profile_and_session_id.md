# Why this is a security risk to use simple profile and session id?

Using simple profile and session IDs can pose a security risk for your system. Complex IDs, such as UUID4, are difficult
to guess and provide a higher level of uniqueness. However, using simple and predictable IDs can enable malicious actors
to exploit vulnerabilities in your system. Here's why:

1. Fake Event Injection: If an attacker is aware of the event source ID (which is often publicly available) and has
   knowledge of either the session ID or profile ID, they can send a fake event that will be falsely associated with a
   legitimate profile. This can lead to data corruption and manipulation of your system.

2. Brute Force Attacks: When using numeric IDs, an attacker can perform brute force attacks by generating IDs within a
   defined range and attempting to register events in your system. Similarly, if simple session IDs are used, an
   attacker can try various combinations to gain access to profile session. Session is connected with profile so events
   with correct session will also be registered.

4. External System Vulnerabilities: When sending IDs from external systems, it becomes even more crucial to avoid using
   simple numeric profile or session IDs. This is because external systems may not have robust security measures in
   place, making them more susceptible to attacks. By using complex and unpredictable IDs, you enhance the security of
   your system and reduce the risk of unauthorized access.

To mitigate these security risks, it is recommended to implement complex and randomly generated IDs, such as UUID4, for
both profile and session identification. These IDs are difficult to guess, ensuring a higher level of security for your
system.

By following this best practice and avoiding the use of simple numeric IDs, you can significantly reduce the likelihood
of unauthorized access, fake event injection, and data corruption in your Tracardi workflow. By default, Tracardi use
UUID4 ids.