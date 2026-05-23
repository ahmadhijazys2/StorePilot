package com.storepilot;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.view.Menu;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.storepilot.auth.LoginActivity;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.LowStockReceiver;
import com.storepilot.core.PermissionManager;
import com.storepilot.core.SessionManager;
import com.storepilot.dashboard.DashboardFragment;
import com.storepilot.inventory.ProductListFragment;
import com.storepilot.purchases.PurchaseHistoryFragment;
import com.storepilot.marketing.VideoMetricsFragment;
import com.storepilot.reports.ReportsFragment;
import com.storepilot.sales.SalesHistoryFragment;
import com.storepilot.seasons.SeasonListFragment;
import com.storepilot.tasks.TaskListFragment;
import com.storepilot.admin.UserManagementFragment;
import com.storepilot.manager.OrderManagementFragment;
import com.storepilot.manager.SupportConversationsFragment;

public class MainActivity extends BaseActivity {

    private static final int REQUEST_NOTIFICATION_PERMISSION = 100;
    private BottomNavigationView bottomNavigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (!SessionManager.getInstance().isLoggedIn()) {
            startActivity(new Intent(this, LoginActivity.class));
            finish();
            return;
        }

        setContentView(R.layout.activity_main);

        // Request notification permission on Android 13+
        requestNotificationPermissionIfNeeded();

        bottomNavigationView = findViewById(R.id.bottomNavigation);

        bottomNavigationView.setOnItemSelectedListener(item -> {
            int id = item.getItemId();
            if (id == R.id.nav_dashboard) {
                loadFragment(new DashboardFragment());
                return true;
            } else if (id == R.id.nav_inventory) {
                loadFragment(new ProductListFragment());
                return true;
            } else if (id == R.id.nav_sales) {
                loadFragment(new SalesHistoryFragment());
                return true;
            } else if (id == R.id.nav_tasks) {
                loadFragment(new TaskListFragment());
                return true;
            } else if (id == R.id.nav_more) {
                showMoreMenu();
                return true;
            }
            return false;
        });

        if (savedInstanceState == null) {
            bottomNavigationView.setSelectedItemId(R.id.nav_dashboard);
        }
    }

    private void requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(
                        this,
                        new String[]{Manifest.permission.POST_NOTIFICATIONS},
                        REQUEST_NOTIFICATION_PERMISSION
                );
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_NOTIFICATION_PERMISSION) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Notifications enabled", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Notifications blocked — enable in Settings", Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        return super.onCreateOptionsMenu(menu);
    }

    private void loadFragment(Fragment fragment) {
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        transaction.replace(R.id.fragmentContainer, fragment);
        transaction.commit();
    }

    private void showMoreMenu() {
        androidx.appcompat.widget.PopupMenu popupMenu =
                new androidx.appcompat.widget.PopupMenu(this, findViewById(R.id.nav_more));
        popupMenu.getMenuInflater().inflate(R.menu.more_menu, popupMenu.getMenu());

        Menu menu = popupMenu.getMenu();
        menu.findItem(R.id.menu_purchases).setVisible(
                checkPermission(PermissionManager.MANAGE_PURCHASES));
        menu.findItem(R.id.menu_marketing).setVisible(
                checkPermission(PermissionManager.VIEW_MARKETING));
        menu.findItem(R.id.menu_reports).setVisible(
                checkPermission(PermissionManager.VIEW_REPORTS));
        menu.findItem(R.id.menu_seasons).setVisible(
                checkPermission(PermissionManager.MANAGE_SEASONS));
        menu.findItem(R.id.menu_admin).setVisible(
                checkPermission(PermissionManager.VIEW_ADMIN));
        // Test notification visible to owner and manager only
        menu.findItem(R.id.menu_test_notification).setVisible(
                checkPermission(PermissionManager.VIEW_REPORTS));

        popupMenu.setOnMenuItemClickListener(item -> {
            int id = item.getItemId();
            if (id == R.id.menu_purchases) {
                loadFragment(new PurchaseHistoryFragment());
            } else if (id == R.id.menu_marketing) {
                loadFragment(new VideoMetricsFragment());
            } else if (id == R.id.menu_reports) {
                loadFragment(new ReportsFragment());
            } else if (id == R.id.menu_seasons) {
                loadFragment(new SeasonListFragment());
            } else if (id == R.id.menu_admin) {
                loadFragment(new UserManagementFragment());
            } else if (id == R.id.menu_orders) {
                loadFragment(new OrderManagementFragment());
            } else if (id == R.id.menu_support) {
                loadFragment(new SupportConversationsFragment());
            } else if (id == R.id.menu_logout) {
                SessionManager.getInstance().logout();
                startActivity(new Intent(this, LoginActivity.class));
                finish();
            } else if (id == R.id.menu_test_notification) {
                Toast.makeText(this, "Checking low stock...", Toast.LENGTH_SHORT).show();
                LowStockReceiver.checkNow(this, true);
            }
            return true;
        });
        popupMenu.show();
    }
}
