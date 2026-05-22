package com.storepilot.auth;

/**
 * Firebase project credentials.
 * Replace the placeholder values below with your actual Firebase project settings.
 * Get these from: Firebase Console → Project Settings → Your apps → Web app config
 * (or Android app config under google-services.json values).
 *
 * HOW TO CONNECT YOUR FIREBASE PROJECT:
 * 1. Go to https://console.firebase.google.com
 * 2. Create or open your project
 * 3. Go to Project Settings → General → Your apps
 * 4. Add an Android app with package name: com.storepilot
 * 5. Download google-services.json and place it in the app/ directory
 *    OR fill in the values below for manual initialization (no plugin needed)
 * 6. In Firebase Console → Authentication → Sign-in method → Enable Email/Password
 *
 * FIREBASE SERVICES USED:
 * - Firebase Authentication (Email/Password sign-in)
 */
public class FirebaseConfig {
    // Replace with your Firebase project's API key
    public static final String API_KEY = "YOUR_API_KEY_HERE";

    // Replace with your Firebase app ID (format: 1:000000000:android:xxxxxxxx)
    public static final String APP_ID = "YOUR_APP_ID_HERE";

    // Replace with your Firebase project ID (e.g. storepilot-12345)
    public static final String PROJECT_ID = "YOUR_PROJECT_ID_HERE";

    // Replace with your Firebase storage bucket (e.g. storepilot-12345.appspot.com)
    public static final String STORAGE_BUCKET = "YOUR_PROJECT_ID_HERE.appspot.com";

    // Replace with your Firebase sender ID (shown as "Sender ID" in Project Settings)
    public static final String MESSAGING_SENDER_ID = "YOUR_SENDER_ID_HERE";
}
