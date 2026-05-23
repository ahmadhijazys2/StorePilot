package com.storepilot.dashboard;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.SessionManager;
import com.storepilot.viewmodels.OrderViewModel;
import com.storepilot.viewmodels.ProductViewModel;
import com.storepilot.viewmodels.SaleViewModel;
import com.storepilot.viewmodels.SeasonViewModel;
import com.storepilot.viewmodels.TaskViewModel;

import java.text.NumberFormat;
import java.util.Calendar;
import java.util.Locale;

public class DashboardFragment extends Fragment {

    private TextView tvSeasonAlert, tvTodaySales, tvLowStockCount, tvPendingTasks;
    private TextView tvTodayOrders;
    private View cardSeasonAlert;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        cardSeasonAlert = view.findViewById(R.id.cardSeasonAlert);
        tvSeasonAlert = view.findViewById(R.id.tvSeasonAlert);
        tvTodaySales = view.findViewById(R.id.tvTodaySales);
        tvLowStockCount = view.findViewById(R.id.tvLowStockCount);
        tvPendingTasks = view.findViewById(R.id.tvPendingTasks);
        tvTodayOrders = view.findViewById(R.id.tvTodayOrders);

        SeasonViewModel seasonVM = new ViewModelProvider(this).get(SeasonViewModel.class);
        SaleViewModel saleVM = new ViewModelProvider(this).get(SaleViewModel.class);
        ProductViewModel productVM = new ViewModelProvider(this).get(ProductViewModel.class);
        TaskViewModel taskVM = new ViewModelProvider(this).get(TaskViewModel.class);

        long now = System.currentTimeMillis();

        // Season alert
        seasonVM.getSeasonsEndingSoon(now).observe(getViewLifecycleOwner(), seasons -> {
            if (seasons != null && !seasons.isEmpty()) {
                cardSeasonAlert.setVisibility(View.VISIBLE);
                tvSeasonAlert.setText(getString(R.string.season_ending_soon, seasons.get(0).getName()));
            } else {
                cardSeasonAlert.setVisibility(View.GONE);
            }
        });

        // Today's sales
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        long startOfDay = cal.getTimeInMillis();
        long endOfDay = startOfDay + 86400000L;

        saleVM.getTodaySalesTotal(startOfDay, endOfDay).observe(getViewLifecycleOwner(), total -> {
            double value = (total != null) ? total : 0.0;
            tvTodaySales.setText(NumberFormat.getCurrencyInstance(Locale.US).format(value));
        });

        // Low stock (threshold = 10)
        productVM.getLowStockProducts(10).observe(getViewLifecycleOwner(), products -> {
            int count = (products != null) ? products.size() : 0;
            tvLowStockCount.setText(String.valueOf(count));
        });

        // Pending tasks
        int userId = SessionManager.getInstance().getLoggedInUser() != null
                ? SessionManager.getInstance().getLoggedInUser().getId() : 0;
        taskVM.getPendingTaskCount(userId).observe(getViewLifecycleOwner(), count -> {
            tvPendingTasks.setText(String.valueOf(count != null ? count : 0));
        });

        // Today's order count and revenue from customer orders
        OrderViewModel orderVM = new ViewModelProvider(this).get(OrderViewModel.class);
        orderVM.getTodayOrderCount(startOfDay).observe(getViewLifecycleOwner(), count -> {
            if (tvTodayOrders != null)
                tvTodayOrders.setText(String.valueOf(count != null ? count : 0));
        });
    }
}
