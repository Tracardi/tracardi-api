# What is the minimum ram mysql needs to run Tracardi?

To determine the minimum memory requirements for MySQL to run stably without restarting, we need to consider a
conservative estimate that allows for basic functionality. Here's a breakdown of the minimum memory requirements:

1. Base MySQL process: 256MB - 512MB

2. InnoDB Buffer Pool: At least 128MB, preferably 256MB or more

3. Operating System: 512MB - 1GB (not strictly for MySQL, but necessary for system stability)

4. Connection handling: Approximately 1MB per connection (assuming a small number of concurrent connections)

5. Query execution: A small buffer for sorting and joins, around 64MB - 128MB

6. Other MySQL buffers and caches: Around 128MB - 256MB

Adding these up, a very minimal setup that could run without frequent restarts might be:

- Total minimum: 1GB - 2GB of RAM

However, it's important to note that this is an absolute minimum and not recommended for any production use. With this
configuration:

1. Performance would be poor
2. The system might struggle with complex queries or multiple concurrent connections
3. There would be little room for data growth or increased load

For a small production environment or a test setup that needs to be somewhat stable, I would recommend at least 4GB of
RAM as a starting point. This would allow:

- 2GB for InnoDB Buffer Pool
- 1GB for MySQL process and other buffers
- 1GB for the operating system

Remember, these are very conservative estimates. In a real production environment, especially one running an application
like Tracardi, you'd typically want significantly more memory to ensure good performance and stability. The actual
requirements would depend on your specific database size, query patterns, and concurrent user load.