package com.storepilot.core;

import com.google.firebase.auth.FirebaseAuth;
import com.storepilot.db.entities.User;

public class SessionManager {

    private static SessionManager instance;
    private User loggedInUser;

    private SessionManager() {}

    public static synchronized SessionManager getInstance() {
        if (instance == null) instance = new SessionManager();
        return instance;
    }

    public void setLoggedInUser(User user) { this.loggedInUser = user; }
    public User getLoggedInUser()          { return loggedInUser; }
    public boolean isLoggedIn()            { return loggedInUser != null; }

    public String getUserRole() {
        return loggedInUser != null ? loggedInUser.getRole() : null;
    }

    /** Clears the local session and signs out of Firebase Authentication */
    public void logout() {
        loggedInUser = null;
        FirebaseAuth.getInstance().signOut();
    }
}
