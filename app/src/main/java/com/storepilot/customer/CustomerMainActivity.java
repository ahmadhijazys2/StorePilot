package com.storepilot.customer;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageButton;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.storepilot.R;
import com.storepilot.auth.LoginActivity;
import com.storepilot.core.SessionManager;

public class CustomerMainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNav;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_customer_main);

        bottomNav = findViewById(R.id.customerBottomNav);

        // Logout button in toolbar
        ImageButton btnLogout = findViewById(R.id.btnCustomerLogout);
        btnLogout.setOnClickListener(v -> showLogoutDialog());

        if (savedInstanceState == null) {
            loadFragment(new CustomerHomeFragment());
        }

        bottomNav.setOnItemSelectedListener(item -> {
            int id = item.getItemId();
            if (id == R.id.nav_customer_home) {
                loadFragment(new CustomerHomeFragment()); return true;
            } else if (id == R.id.nav_customer_cart) {
                loadFragment(new CartFragment()); return true;
            } else if (id == R.id.nav_customer_orders) {
                loadFragment(new OrderHistoryFragment()); return true;
            } else if (id == R.id.nav_customer_favorites) {
                loadFragment(new FavoritesFragment()); return true;
            } else if (id == R.id.nav_customer_support) {
                loadFragment(new SupportChatFragment()); return true;
            }
            return false;
        });
    }

    private void showLogoutDialog() {
        new AlertDialog.Builder(this)
                .setTitle("Sign Out")
                .setMessage("Are you sure you want to sign out?")
                .setPositiveButton("Sign Out", (d, w) -> logout())
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void loadFragment(Fragment fragment) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.customerFragmentContainer, fragment)
                .commit();
    }

    public void logout() {
        SessionManager.getInstance().logout(); // also calls FirebaseAuth.signOut()
        Intent intent = new Intent(this, LoginActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(intent);
        finish();
    }
}
