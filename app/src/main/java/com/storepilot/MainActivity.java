package com.storepilot;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.storepilot.auth.LoginActivity;
import com.storepilot.core.BaseActivity;
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

public class MainActivity extends BaseActivity {

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
            } else if (id == R.id.menu_logout) {
                SessionManager.getInstance().logout();
                startActivity(new Intent(this, LoginActivity.class));
                finish();
            }
            return true;
        });
        popupMenu.show();
    }
}
