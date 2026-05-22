package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.viewmodels.AuthViewModel;

public class SetupActivity extends BaseActivity {

    private EditText etOwnerUsername, etOwnerPassword, etConfirmPassword;
    private Button btnCreate;
    private AuthViewModel authViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

        etOwnerUsername = findViewById(R.id.etOwnerUsername);
        etOwnerPassword = findViewById(R.id.etOwnerPassword);
        etConfirmPassword = findViewById(R.id.etConfirmPassword);
        btnCreate = findViewById(R.id.btnCreate);

        authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);

        authViewModel.setupComplete.observe(this, complete -> {
            if (Boolean.TRUE.equals(complete)) {
                Toast.makeText(this, getString(R.string.setup_complete), Toast.LENGTH_SHORT).show();
                startActivity(new Intent(this, LoginActivity.class));
                finish();
            }
        });

        btnCreate.setOnClickListener(v -> {
            String username = etOwnerUsername.getText().toString().trim();
            String password = etOwnerPassword.getText().toString();
            String confirm = etConfirmPassword.getText().toString();

            if (username.isEmpty() || password.isEmpty() || confirm.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }
            if (!password.equals(confirm)) {
                Toast.makeText(this, getString(R.string.error_passwords_no_match), Toast.LENGTH_SHORT).show();
                return;
            }
            if (password.length() < 6) {
                Toast.makeText(this, getString(R.string.error_password_too_short), Toast.LENGTH_SHORT).show();
                return;
            }

            authViewModel.setupOwner(username, password, false);
        });
    }
}
