# Pain-points in huge multi-tenant setups

When operating Tracardi in environments with a large number of tenants (over 100), several significant challenges arise:

1. **Index Capacity in Elasticsearch**: By its default settings, Elasticsearch (ES) can support up to 1000 indices.
   However, given that Tracardi, version prior 0.9.0, allocates approximately 16 indices per tenant, this limit can be reached rapidly as the number
   of tenants grows. It necessitates adjustments to Elasticsearch configurations to accommodate a greater number of
   indices.

2. **Performance Verification**: It's crucial to rigorously test the system to ascertain its efficiency and reliability
   under the strain of a multi-tenant arrangement (with exceeded 1000 indices). This ensures that the introduction of
   more tenants doesn’t compromise the performance of the system.

3. **Anticipated Software Updates**: The Tracardi development team is contemplating a migration of certain data types
   from Elasticsearch to MySQL. This transition introduces a dependency on a MySQL database, which requires careful
   integration and management alongside the existing Elasticsearch database. This should allow storing more tenant data
   per one ES cluster.

4. **Cluster Grouping**: To further support a growing number of tenants, it is necessary to establish multiple Tracardi
   clusters. Each of these clusters should be accessible through its own unique URL. Furthermore, each cluster can
   employ various data partitioning strategies, which allows for more tenants to be accommodated within one cluster. For
   details on data partitioning, refer to Tracardi's documentation.
