package com.storepilot.auth;

import android.content.Context;
import android.util.Log;

import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

/**
 * Handles Firebase Authentication using manual initialization.
 * This approach does NOT require google-services.json or the google-services Gradle plugin.
 * Fill in FirebaseConfig with your real project values to activate.
 */
public class FirebaseAuthHelper {

    private static final String TAG = "FirebaseAuthHelper";
    private static FirebaseAuth firebaseAuth;

    public interface AuthCallback {
        void onSuccess(String uid);
        void onFailure(String error);
    }

    public static void init(Context context) {
        if (FirebaseConfig.API_KEY.startsWith("YOUR_")) {
            Log.w(TAG, "Firebase not configured — fill in FirebaseConfig.java to enable cloud auth");
            return;
        }
        try {
            if (FirebaseApp.getApps(context).isEmpty()) {
                FirebaseOptions options = new FirebaseOptions.Builder()
                        .setApiKey(FirebaseConfig.API_KEY)
                        .setApplicationId(FirebaseConfig.APP_ID)
                        .setProjectId(FirebaseConfig.PROJECT_ID)
                        .setStorageBucket(FirebaseConfig.STORAGE_BUCKET)
                        .setGcmSenderId(FirebaseConfig.MESSAGING_SENDER_ID)
                        .build();
                FirebaseApp.initializeApp(context, options);
            }
            firebaseAuth = FirebaseAuth.getInstance();
        } catch (Exception e) {
            Log.e(TAG, "Firebase init failed: " + e.getMessage());
        }
    }

    public static boolean isConfigured() {
        return firebaseAuth != null && !FirebaseConfig.API_KEY.startsWith("YOUR_");
    }

    public static void signUp(String email, String password, AuthCallback callback) {
        if (!isConfigured()) {
            callback.onSuccess("local-only");
            return;
        }
        firebaseAuth.createUserWithEmailAndPassword(email, password)
                .addOnSuccessListener(result -> {
                    FirebaseUser user = result.getUser();
                    callback.onSuccess(user != null ? user.getUid() : "unknown");
                })
                .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
    }

    public static void signIn(String email, String password, AuthCallback callback) {
        if (!isConfigured()) {
            callback.onSuccess("local-only");
            return;
        }
        firebaseAuth.signInWithEmailAndPassword(email, password)
                .addOnSuccessListener(result -> {
                    FirebaseUser user = result.getUser();
                    callback.onSuccess(user != null ? user.getUid() : "unknown");
                })
                .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
    }

    public static void signOut() {
        if (isConfigured()) {
            firebaseAuth.signOut();
        }
    }
}
