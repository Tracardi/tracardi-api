# Merge Profile Action

When there is a new Personally Identifiable Information(PII) appended to a profile then the profile may 
need merging with other profiles in the system. This is the way you maintain a consistent user profile.

Once the merge profile action is used in the workflow it will mark profile to be merged at the end of workflow. 
To complete merging you will have to provide a merge key in configuration tab of the merge profile node.

## Configuration

This node needs a merge key that will be used during merging. That can be e-mail, telephone number, id, etc. 
System will look for other profiles that have the same merge key, e.g. e-mail and will 
merge all found profiles into one record.  

If two or more keys are defined Tracardi will look for records that have all defined keys. 
For example if it is e-mail and name then record matched for merging will have both 
email and name equal to defined values. 

Provide merge key in form of JSON array. 

To access merge key data use dotted notation. Details on dotted notation can be found Notations / 
Dot notation in the documentation.

```json
{
  "mergeBy": ["event@properties.name"]
}

```

## Side effects

Profile merging will concatenate data even if there is a conflict in data. 
For example let's assume there is a user `John Doe` with email `john.does@mail.com` in storage. 
New data also has e-mail `john.does@mail.com` and name and surname equal to `Jonathan Doe`. 

We are using e-mail as primary merge key.

That means the record will be merged as: 

```yaml
name: [John, Jothatan] 
surname: [Doe]   
```

Conflicting name will have both values `[John, Jothatan]`.
