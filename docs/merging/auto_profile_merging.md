# Auto Profile Merging Documentation

## Overview

Auto Profile Merging (APM) is a feature introduced in Tracardi version 0.8.2, aimed at streamlining the process of
merging user profiles. It automatically merges profiles when specific predefined fields, which are considered as merging
keys, contain matching data.

### Merging Keys

The following profile fields are designated as merging keys:

- `data.contact.email.main`
- `data.contact.email.business`
- `data.contact.email.private`
- `data.contact.phone.main`
- `data.contact.phone.business`
- `data.contact.phone.whatsapp`
- `data.contact.phone.mobile`

Any changes in these fields will initiate the merging process, where the system searches for profiles with identical
data in these fields and merges them.

## Configuration

### Enabling Auto Profile Merging

To activate APM, follow these steps:

1. Add the `AUTO_PROFILE_MERGING` environment parameter with a key of at least 20 characters when starting the Tracardi
   API (include it in the Docker command). This key is used for hashing emails and phone numbers, aiding in profile
   identification. Keep this key confidential and note that changing it requires the system to recreate the merging
   process, which can be time-consuming.
2. Enabling the `AUTO_PROFILE_MERGING` parameter will also automatically enable the generation and storage of unique IDs
   for every email address processed by the system.

## How It Works

- The system monitors changes in the profile. When a change is detected in the fields designated as merging keys, it
  generates a unique ID for each phone number and email.
- These IDs are unique to each system installation, ensuring privacy and security. The `AUTO_PROFILE_MERGING` key is
  used as a salt before hashing the email addresses.
- Generated IDs are stored in the 'profile IDs' field with specific prefixes:
    - Email IDs use prefixes like 'emm-' for main, 'emb-' for business, and 'emp-' for private emails.
    - Phone IDs use 'phm-' for main, 'phw-' for WhatsApp, 'phb-' for business, and 'pho-' for mobile phones.
- Profiles flagged for merging are processed by a background worker, which consolidates them accordingly.