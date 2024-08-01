# There are prefixes in the profile IDS what they mean?

The prefixes `emm-`, `emb-`, `emp-`, `phm-`, `phw-`, `phb-`, and `pho-` in `profile.ids` are used to denote specific types of
profile identifiers based on the data source they represent. Here's what each prefix means:

1. **`emm-`**:
    - **Email Main**: This prefix is used for the main email address of the profile. It typically refers to the primary
      email address a user provides.

2. **`emb-`**:
    - **Email Business**: This prefix is used for the business email address of the profile. It's typically used in
      professional or business contexts.

3. **`emp-`**:
    - **Email Private**: This prefix is used for the private email address of the profile. It usually refers to a
      personal email address.

4. **`phm-`**:
    - **Phone Main**: This prefix is used for the main phone number of the profile. It typically refers to the primary
      contact number provided by the user.

5. **`phw-`**:
    - **Phone WhatsApp**: This prefix is used for the WhatsApp phone number of the profile. It refers to the phone
      number used for WhatsApp communications.

6. **`phb-`**:
    - **Phone Business**: This prefix is used for the business phone number of the profile. It refers to a phone number
      used in a professional or business setting.

7. **`pho-`**:
    - **Phone Other**: This prefix is used for any other phone numbers associated with the profile. It can include
      secondary numbers, home phones, or other contact numbers not categorized as main, WhatsApp, or business.

## Purpose of These Prefixes

These prefixes help in identifying and categorizing the sources of profile data. When profiles are merged, these
identifiers ensure that data from different sources is correctly attributed and merged into the corresponding profile
fields.