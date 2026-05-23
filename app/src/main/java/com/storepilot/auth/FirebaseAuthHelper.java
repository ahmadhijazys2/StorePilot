package com.storepilot.auth;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.UserProfileChangeRequest;

/**
 * Firebase Authentication helper.
 * Firebase is initialized automatically via google-services.json.
 */
public class FirebaseAuthHelper {

    public interface AuthCallback {
        void onSuccess(String uid);
        void onFailure(String error);
    }

    private static FirebaseAuth getAuth() {
        return FirebaseAuth.getInstance();
    }

    /** Creates a Firebase account and saves username as displayName */
    public static void signUp(String email, String password, String username, AuthCallback callback) {
        getAuth().createUserWithEmailAndPassword(email, password)
                .addOnSuccessListener(result -> {
                    FirebaseUser user = result.getUser();
                    if (user == null) { callback.onSuccess("unknown"); return; }

                    UserProfileChangeRequest update = new UserProfileChangeRequest.Builder()
                            .setDisplayName(username)
                            .build();
                    user.updateProfile(update)
                            .addOnCompleteListener(t -> callback.onSuccess(user.getUid()));
                })
                .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
    }

    /** Signs in with email and password */
    public static void signIn(String email, String password, AuthCallback callback) {
        getAuth().signInWithEmailAndPassword(email, password)
                .addOnSuccessListener(result -> {
                    FirebaseUser user = result.getUser();
                    callback.onSuccess(user != null ? user.getUid() : "unknown");
                })
                .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
    }

    public static String getCurrentUsername() {
        FirebaseUser user = getAuth().getCurrentUser();
        return user != null ? user.getDisplayName() : null;
    }

    public static String getCurrentEmail() {
        FirebaseUser user = getAuth().getCurrentUser();
        return user != null ? user.getEmail() : null;
    }

    public static void signOut() {
        getAuth().signOut();
    }
}
