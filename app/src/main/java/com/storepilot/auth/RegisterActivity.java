package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.storepilot.R;
import com.storepilot.core.AppDatabase;
import com.storepilot.core.BaseActivity;
import com.storepilot.db.entities.User;

// Registration screen — creates a new user account
public class RegisterActivity extends BaseActivity {

    private EditText etFullName, etUsername, etEmail, etPhone, etPassword, etConfirmPassword;
    private Spinner spinnerRole;
    private Button btnRegister;
    private TextView tvLoginLink;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // Find all the form fields
        etFullName = findViewById(R.id.etFullName);
        etUsername = findViewById(R.id.etUsername);
        etEmail = findViewById(R.id.etEmail);
        etPhone = findViewById(R.id.etPhone);
        etPassword = findViewById(R.id.etPassword);
        etConfirmPassword = findViewById(R.id.etConfirmPassword);
        spinnerRole = findViewById(R.id.spinnerRole);
        btnRegister = findViewById(R.id.btnRegister);
        tvLoginLink = findViewById(R.id.tvLoginLink);

        // Populate the role dropdown
        String[] roles = {"Customer", "Manager", "Owner"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, roles);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerRole.setAdapter(adapter);

        // Handle register button click
        btnRegister.setOnClickListener(v -> attemptRegister());

        // Navigate back to login
        tvLoginLink.setOnClickListener(v -> {
            startActivity(new Intent(this, LoginActivity.class));
            finish();
        });
    }

    // Validate the form and create the account
    private void attemptRegister() {
        String fullName = etFullName.getText().toString().trim();
        String username = etUsername.getText().toString().trim();
        String email = etEmail.getText().toString().trim();
        String phone = etPhone.getText().toString().trim();
        String password = etPassword.getText().toString();
        String confirmPassword = etConfirmPassword.getText().toString();

        // Check all required fields are filled
        if (fullName.isEmpty() || username.isEmpty() || email.isEmpty() ||
                password.isEmpty() || confirmPassword.isEmpty()) {
            Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
            return;
        }

        // Check passwords match
        if (!password.equals(confirmPassword)) {
            Toast.makeText(this, getString(R.string.error_passwords_no_match), Toast.LENGTH_SHORT).show();
            return;
        }

        // Minimum password length
        if (password.length() < 6) {
            Toast.makeText(this, getString(R.string.error_password_too_short), Toast.LENGTH_SHORT).show();
            return;
        }

        // Map the spinner selection to a role string
        String selectedRole = spinnerRole.getSelectedItem().toString();
        String role;
        switch (selectedRole) {
            case "Manager": role = "STORE_MANAGER"; break;
            case "Owner":   role = "OWNER"; break;
            default:        role = "CUSTOMER"; break;
        }

        // Disable button to prevent double-tap
        btnRegister.setEnabled(false);

        // Hash the password and save the user in background
        String finalRole = role;
        AppDatabase.dbExecutor.execute(() -> {
            String salt = CryptoUtil.generateSalt();
            String hash = CryptoUtil.hashPassword(password, salt);

            User newUser = new User(fullName, username, email, phone, hash, salt, finalRole,
                    System.currentTimeMillis());

            try {
                AppDatabase.getInstance(getApplication()).userDao().insert(newUser);

                // Navigate to login after successful registration
                runOnUiThread(() -> {
                    Toast.makeText(this, "Account created! Please log in.", Toast.LENGTH_SHORT).show();
                    startActivity(new Intent(this, LoginActivity.class));
                    finish();
                });
            } catch (Exception e) {
                // Username or email already exists
                runOnUiThread(() -> {
                    btnRegister.setEnabled(true);
                    Toast.makeText(this, "Username or email already taken.", Toast.LENGTH_SHORT).show();
                });
            }
        });
    }
}
