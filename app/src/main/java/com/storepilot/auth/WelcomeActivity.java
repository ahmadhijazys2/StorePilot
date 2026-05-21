package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;

// First screen users see when they open the app
public class WelcomeActivity extends BaseActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // If user is already logged in, skip the welcome screen
        if (SessionManager.getInstance().isLoggedIn()) {
            navigateByRole();
            return;
        }

        setContentView(R.layout.activity_welcome);

        Button btnLogin = findViewById(R.id.btnLogin);
        Button btnRegister = findViewById(R.id.btnRegister);

        // Go to login screen
        btnLogin.setOnClickListener(v ->
                startActivity(new Intent(this, LoginActivity.class)));

        // Go to registration screen
        btnRegister.setOnClickListener(v ->
                startActivity(new Intent(this, RegisterActivity.class)));
    }

    // Route user to the right app based on their role
    private void navigateByRole() {
        String role = SessionManager.getInstance().getUserRole();
        if ("CUSTOMER".equals(role)) {
            // Customers go to the shopping interface
            startActivity(new Intent(this, com.storepilot.customer.CustomerMainActivity.class));
        } else {
            // Managers and owners go to the management dashboard
            startActivity(new Intent(this, com.storepilot.MainActivity.class));
        }
        finish();
    }
}
