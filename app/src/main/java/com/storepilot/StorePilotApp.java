package com.storepilot;

import android.app.Application;

import com.google.firebase.FirebaseApp;
import com.storepilot.core.NotificationHelper;

public class StorePilotApp extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        FirebaseApp.initializeApp(this);
        NotificationHelper.createChannel(this);
    }
}
