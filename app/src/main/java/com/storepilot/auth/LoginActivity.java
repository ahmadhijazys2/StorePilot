package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.MainActivity;
import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.CustomerMainActivity;
import com.storepilot.viewmodels.AuthViewModel;

// Login screen — validates credentials and routes user to the right app experience
public class LoginActivity extends BaseActivity {

    private EditText etUsername, etPassword;
    private Button btnLogin;
    private TextView tvDemoHint, tvRegisterLink, tvForgotPassword;
    private AuthViewModel authViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Find UI elements
        etUsername = findViewById(R.id.etUsername);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);
        tvDemoHint = findViewById(R.id.tvDemoHint);
        tvRegisterLink = findViewById(R.id.tvRegisterLink);
        tvForgotPassword = findViewById(R.id.tvForgotPassword);

        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        // If no accounts exist yet, go to setup screen
        authViewModel.needsSetup.observe(this, needsSetup -> {
            if (Boolean.TRUE.equals(needsSetup)) {
                startActivity(new Intent(this, SetupActivity.class));
                finish();
            }
        });

        // Login succeeded — route to the correct screen based on role
        authViewModel.loginSuccess.observe(this, success -> {
            if (Boolean.TRUE.equals(success)) {
                String role = SessionManager.getInstance().getUserRole();
                if ("CUSTOMER".equals(role)) {
                    // Customers go to the store shopping interface
                    startActivity(new Intent(this, CustomerMainActivity.class));
                } else {
                    // Managers and owners go to the dashboard
                    startActivity(new Intent(this, MainActivity.class));
                }
                finish();
            }
        });

        // Show login error message
        authViewModel.loginError.observe(this, error -> {
            if (error != null) {
                Toast.makeText(this, error, Toast.LENGTH_SHORT).show();
            }
        });

        // Attempt login when button is pressed
        btnLogin.setOnClickListener(v -> {
            String username = etUsername.getText().toString().trim();
            String password = etPassword.getText().toString();
            if (username.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }
            authViewModel.login(username, password);
        });

        // Navigate to register screen
        if (tvRegisterLink != null) {
            tvRegisterLink.setOnClickListener(v ->
                    startActivity(new Intent(this, RegisterActivity.class)));
        }

        // Forgot password placeholder
        if (tvForgotPassword != null) {
            tvForgotPassword.setOnClickListener(v ->
                    Toast.makeText(this, "Please contact your store admin.", Toast.LENGTH_SHORT).show());
        }

        // Check if database needs initial setup
        authViewModel.checkNeedsSetup();
    }
}
