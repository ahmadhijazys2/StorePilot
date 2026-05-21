package com.storepilot.customer;

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
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.CustomerOrderAdapter;
import com.storepilot.viewmodels.OrderViewModel;

import java.util.ArrayList;

// Shows the customer's past and current orders
public class OrderHistoryFragment extends Fragment {

    private RecyclerView rvOrders;
    private TextView tvEmpty;
    private OrderViewModel orderViewModel;
    private CustomerOrderAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_order_history, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvOrders = view.findViewById(R.id.rvOrders);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        rvOrders.setLayoutManager(new LinearLayoutManager(requireContext()));
        adapter = new CustomerOrderAdapter(new ArrayList<>());
        rvOrders.setAdapter(adapter);

        orderViewModel = new ViewModelProvider(this).get(OrderViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        // Load and display orders for this customer
        orderViewModel.getOrdersByCustomer(customerId).observe(getViewLifecycleOwner(), orders -> {
            adapter.setOrders(orders != null ? orders : new ArrayList<>());
            boolean empty = orders == null || orders.isEmpty();
            tvEmpty.setVisibility(empty ? View.VISIBLE : View.GONE);
            rvOrders.setVisibility(empty ? View.GONE : View.VISIBLE);
        });
    }
}
