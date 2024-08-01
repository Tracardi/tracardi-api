To set up an AWS S3 bucket and obtain the necessary access keys, you'll need to follow several steps.
These steps involve creating an S3 bucket and generating an AWS access key and secret access key. Here’s how you can do
it:

### 1. Sign In to the AWS Management Console

- First, log in to your AWS Management Console using your AWS account. If you don't have an account, you will need to
  sign up for one.

### 2. Create an S3 Bucket

- In the AWS Management Console, find and select the **S3** service under the Storage category or use the search bar.
- Click on **Create bucket**.
- Provide a **bucket name**. This name must be unique across all existing bucket names in Amazon S3.
- Select a **Region** that is closest to you or your users for the best performance.
- Leave the settings as they are for the most part, unless you have specific requirements. For a basic setup, you don't
  need to modify them.
- Click on **Create bucket** at the bottom of the page.

### 3. Obtain Your AWS Access Keys

For security reasons, it's recommended to create a new IAM user and grant it the necessary permissions to access only
the resources it needs (in this case, your S3 bucket).

#### Create a New IAM User:

- In the AWS Management Console, navigate to the **IAM** service.
- Go to **Users** > **Add user**.
- Enter a **user name** and select (if displayed) **Programmatic access** as the access type. This will enable an access key ID and
  secret access key for the AWS API, CLI, SDK, and other development tools.
- Click on **Next: Permissions**.

#### Set Permissions:

- Choose **Attach existing policies directly**.
- Search for and select the **AmazonS3FullAccess** policy. Note: For production environments or more secure setups, it's
  better to create a custom policy that grants only the permissions necessary.
- Click on **Next: Tags** (optional) and then **Next: Review**.
- Review your user details and click on **Create user**.

#### Obtain Access Keys:

- After the user is created, you’ll be taken to a screen showing the list of users. 
- Click on the created user
- Click on **Create Access Key**
- You will see **Access key best practices & alternatives**
- Select **Other** and click **Next**
- Fill the description tag. This is the name of the keys. It can be any name. Click **Create Access Key**
- Retrieve access keys **Access key ID** and **Secret access key**. Make
  sure to download or copy these keys and store them securely. You will not be able to see the secret access key again
  after this step.
