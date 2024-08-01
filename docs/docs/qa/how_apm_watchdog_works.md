# How APM (Automatic Profile Merging) Watchdog works?

Here's a detailed breakdown of what it does:

1. **Check if APM is on**:

The code first checks if the APM (Automatic Profile Merging) system is enabled using tracardi.is_apm_on().

2. **Try-Catch Block**:

The whole process is wrapped in a try-catch block to handle any exceptions that may occur during execution. If an
exception occurs, it logs an error message.

3. **Find all predefined merging keys/fields**:

The code iterates through a dictionary FLAT_PROFILE_FIELD_MAPPING which contains fields of profiles and their
respective prefixes.

4. **Find Duplicated Profiles by Field**:

For each field, it gets duplicated profiles with duplicated fields values across
profiles. This function returns the count of duplicates. It logs the count of duplicated field values.

5.**Process Each Profile with Duplicated Field Values**:

For each duplicated field value, it retrieves the profiles that have that specific duplicated field value. Each profile
is then converted to a Profile entity.

6. **Recreate Hash IDs**:

For each profile, the system computes a new hashed value for the duplicated field value.
It checks if this hashed value is already in the profile’s IDs. If not, it logs an information message and creates the
missing hashed ID, then appends the new hashed value to the profile's IDs.

7. **Mark Profiles for Merging**:

The profile is marked for merging and sets the auto-merge fields in the profile’s metadata.
The profile is then saved back to the database.

8. **Logging and Error Handling**:

If any error occurs during the process, it catches the exception and logs an error message with details about the
failure.