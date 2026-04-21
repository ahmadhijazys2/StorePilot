package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.MainActivity;
import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.viewmodels.AuthViewModel;

public class LoginActivity extends BaseActivity {

    private EditText etUsername, etPassword;
    private Button btnLogin;
    private TextView tvDemoHint;
    private AuthViewModel authViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        etUsername = findViewById(R.id.etUsername);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);
        tvDemoHint = findViewById(R.id.tvDemoHint);

        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        authViewModel.needsSetup.observe(this, needsSetup -> {
            if (Boolean.TRUE.equals(needsSetup)) {
                startActivity(new Intent(this, SetupActivity.class));
                finish();
            }
        });

        authViewModel.loginSuccess.observe(this, success -> {
            if (Boolean.TRUE.equals(success)) {
                startActivity(new Intent(this, MainActivity.class));
                finish();
            }
        });

        authViewModel.loginError.observe(this, error -> {
            if (error != null) {
                Toast.makeText(this, error, Toast.LENGTH_SHORT).show();
            }
        });

        btnLogin.setOnClickListener(v -> {
            String username = etUsername.getText().toString().trim();
            String password = etPassword.getText().toString();
            if (username.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }
            authViewModel.login(username, password);
        });

        authViewModel.checkNeedsSetup();
    }
}
