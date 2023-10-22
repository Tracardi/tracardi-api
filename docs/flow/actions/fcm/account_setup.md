To use Firebase Cloud Messaging (FCM) for sending push notifications, you need to register and set up a Firebase project. Here's how you can do it:

1. **Visit Firebase Console:**
   Go to the Firebase Console at [https://console.firebase.google.com/](https://console.firebase.google.com/).

2. **Sign In or Create an Account:**
   If you don't have a Google account, you'll need to create one. If you have a Google account, sign in to the Firebase Console using your Google credentials.

3. **Create a New Project:**
   Once you're logged in, you can create a new Firebase project by clicking on the "Add Project" button.

4. **Enter Project Name:**
   Give your project a name and optionally choose a region for your project's data storage.

5. **Agree to the Terms:**
   Review and agree to the terms of service and click "Continue."

6. **Choose Google Analytics Setting (Optional):**
   You can choose whether or not to enable Google Analytics for your project. You can always enable it later if you wish.

7. **Creating Project:**
   Firebase will create your project. This might take a moment.

8. **Access Your Project:**
   Once the project is created, you'll be taken to the project dashboard.

9. **Set Up Your App:**
   To use FCM, you'll need to set up your mobile app within the Firebase project. Click on "Add app" and select the appropriate platform (iOS, Android, or web) for your application. Follow the setup instructions provided.

10. **Obtain Server Key:**
    To send push notifications from your server or backend, you'll need the `Server Key` or `Legacy Server Key`. You can find this key under Project settings > Cloud Messaging. This key is used for authentication when sending notifications.

11. **Obtain App Tokens:**
    Each mobile app instance will have a unique FCM token (device token). You can obtain this token on the device and use it to send notifications to specific devices.

Once your Firebase project is set up, you can start sending push notifications to your mobile app using FCM. Make sure to replace `'your-fcm-server-key'` in your code with the actual Server Key obtained from your Firebase project.

Please note that Firebase Console and services may change or be updated, so refer to the Firebase documentation for the most current information and setup instructions.