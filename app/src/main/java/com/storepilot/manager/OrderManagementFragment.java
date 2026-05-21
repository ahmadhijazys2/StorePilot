package com.storepilot.manager;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.manager.adapters.ManagerOrderAdapter;
import com.storepilot.viewmodels.OrderViewModel;

import java.util.ArrayList;

// Manager screen for viewing and updating all customer orders
public class OrderManagementFragment extends Fragment {

    private RecyclerView rvOrders;
    private TextView tvEmpty;
    private OrderViewModel orderViewModel;
    private ManagerOrderAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_order_management, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvOrders = view.findViewById(R.id.rvManagerOrders);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        rvOrders.setLayoutManager(new LinearLayoutManager(requireContext()));
        orderViewModel = new ViewModelProvider(this).get(OrderViewModel.class);

        // Adapter with status change callback
        adapter = new ManagerOrderAdapter(new ArrayList<>(), (order, newStatus) ->
                orderViewModel.updateOrderStatus(order, newStatus));
        rvOrders.setAdapter(adapter);

        // Load all orders from all customers
        orderViewModel.getAllOrders().observe(getViewLifecycleOwner(), orders -> {
            adapter.setOrders(orders != null ? orders : new ArrayList<>());
            boolean empty = orders == null || orders.isEmpty();
            tvEmpty.setVisibility(empty ? View.VISIBLE : View.GONE);
            rvOrders.setVisibility(empty ? View.GONE : View.VISIBLE);
        });
    }
}
