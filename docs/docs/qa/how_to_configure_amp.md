# How to enable ND configure AMP?

## Enabling Auto Profile Merging

1. **Add Environment Parameter**: Add the `AUTO_PROFILE_MERGING` environment parameter with a key of at least 20
   characters when starting the Tracardi API. This key is used for hashing emails and phone numbers, etc. to aid in profile
   identification. Keep this key confidential and note that changing it requires the system to recreate the merging
   process, which can be time-consuming.
2. **Docker Command**: Set the env variable when running docker.
   ```bash
   docker run \
   -e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
   -e REDIS_HOST=redis://<redis-ip>:6379 \
   -e MYSQL_HOST=<mysql-ip> \
   -e AUTO_PROFILE_MERGING=<your-hash-key> \
   tracardi/tracardi-api:<last-version>
   ```
   Replace `<elasticsearch-ip>`, `<redis-ip>`, `<mysql-ip>`, and `<last-version>` with your respective values.

## Running APM Worker

3. **Start APM Worker**: Execute the following Docker command to run the APM Worker.
   ```bash
   docker run \
   -e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
   -e REDIS_HOST=redis://<redis-ip>:6379 \
   -e MYSQL_HOST=<mysql-ip> \
   -e MODE=worker \
   -e PAUSE=5 \
   tracardi/apm:<last-version>
   ```


## How It Works

1. **Merging Keys**:
    - The following profile fields are used as merging keys:
        - `data.contact.email.main`
        - `data.contact.email.business`
        - `data.contact.email.private`
        - `data.contact.phone.main`
        - `data.contact.phone.business`
        - `data.contact.phone.whatsapp`
        - `data.contact.phone.mobile`
2. **Profile Monitoring**:
    - Tracardi continuously monitors changes in the merging key fields and saves hashes of all changed fields (see above) in the `profile.ids`.
3. **Profile IDs Management**:
    - IDs are stored in the `profile IDs` field with specific
      prefixes (`emm-`, `emb-`, `emp-`, `phm-`, `phw-`, `phb-`, `pho-`). E.g. `emm-` is a prefix for main email.
4. **Merging Process**:
    - Profiles flagged for merging are processed by a background worker, consolidating the profiles and updating
      the `ids` field with the merged profile's ID.
