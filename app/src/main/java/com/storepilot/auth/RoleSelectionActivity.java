package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.text.InputType;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;

public class RoleSelectionActivity extends BaseActivity {

    public static final String EXTRA_ROLE = "extra_role";
    private static final String OWNER_SECRET_CODE = "777";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_role_selection);

        Button btnOwner = findViewById(R.id.btnRoleOwner);
        Button btnCustomer = findViewById(R.id.btnRoleCustomer);

        btnOwner.setOnClickListener(v -> showOwnerCodeDialog());
        btnCustomer.setOnClickListener(v -> openRegister("Customer"));
    }

    private void showOwnerCodeDialog() {
        EditText input = new EditText(this);
        input.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD);
        input.setHint("Enter owner code");
        input.setPadding(48, 32, 48, 32);

        new AlertDialog.Builder(this)
                .setTitle("Owner Verification")
                .setMessage("Enter the owner secret code to continue.")
                .setView(input)
                .setPositiveButton("Confirm", (dialog, which) -> {
                    String code = input.getText().toString().trim();
                    if (OWNER_SECRET_CODE.equals(code)) {
                        openRegister("Owner");
                    } else {
                        Toast.makeText(this, "Incorrect code. Access denied.", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void openRegister(String role) {
        Intent intent = new Intent(this, RegisterActivity.class);
        intent.putExtra(EXTRA_ROLE, role);
        startActivity(intent);
    }
}
