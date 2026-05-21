package com.storepilot.customer;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.storepilot.R;
import com.storepilot.auth.LoginActivity;
import com.storepilot.core.SessionManager;

// Main activity for customers — hosts the bottom navigation and fragment container
public class CustomerMainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNav;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_customer_main);

        bottomNav = findViewById(R.id.customerBottomNav);

        // Load the home fragment by default
        if (savedInstanceState == null) {
            loadFragment(new CustomerHomeFragment());
        }

        // Handle bottom navigation tab switching
        bottomNav.setOnItemSelectedListener(item -> {
            int id = item.getItemId();
            if (id == R.id.nav_customer_home) {
                loadFragment(new CustomerHomeFragment());
                return true;
            } else if (id == R.id.nav_customer_cart) {
                loadFragment(new CartFragment());
                return true;
            } else if (id == R.id.nav_customer_orders) {
                loadFragment(new OrderHistoryFragment());
                return true;
            } else if (id == R.id.nav_customer_favorites) {
                loadFragment(new FavoritesFragment());
                return true;
            } else if (id == R.id.nav_customer_support) {
                loadFragment(new SupportChatFragment());
                return true;
            }
            return false;
        });
    }

    // Replace the main container with a new fragment
    private void loadFragment(Fragment fragment) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.customerFragmentContainer, fragment)
                .commit();
    }

    // Log out and return to login screen
    public void logout() {
        SessionManager.getInstance().logout();
        startActivity(new Intent(this, LoginActivity.class));
        finish();
    }
}
