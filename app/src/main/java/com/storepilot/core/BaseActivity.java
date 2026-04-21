package com.storepilot.core;

import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

public class BaseActivity extends AppCompatActivity {

    protected void hideViewIfUnauthorized(View view, String permission) {
        if (!PermissionManager.currentUserHasPermission(permission)) {
            view.setVisibility(View.GONE);
        } else {
            view.setVisibility(View.VISIBLE);
        }
    }

    protected boolean checkPermission(String permission) {
        return PermissionManager.currentUserHasPermission(permission);
    }
}
