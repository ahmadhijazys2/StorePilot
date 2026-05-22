package com.storepilot.auth;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;

public class RoleSelectionActivity extends BaseActivity {

    public static final String EXTRA_ROLE = "extra_role";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_role_selection);

        Button btnOwner = findViewById(R.id.btnRoleOwner);
        Button btnCustomer = findViewById(R.id.btnRoleCustomer);

        btnOwner.setOnClickListener(v -> openRegister("Owner"));
        btnCustomer.setOnClickListener(v -> openRegister("Customer"));
    }

    private void openRegister(String role) {
        Intent intent = new Intent(this, RegisterActivity.class);
        intent.putExtra(EXTRA_ROLE, role);
        startActivity(intent);
    }
}
