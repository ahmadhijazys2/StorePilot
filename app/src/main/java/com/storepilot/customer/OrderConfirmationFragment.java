package com.storepilot.customer;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.storepilot.R;

// Order confirmation screen shown after a successful checkout
public class OrderConfirmationFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_order_confirmation, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        Button btnViewOrders = view.findViewById(R.id.btnViewOrders);
        Button btnContinueShopping = view.findViewById(R.id.btnContinueShopping);

        // Navigate to order history
        btnViewOrders.setOnClickListener(v -> {
            requireActivity().getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.customerFragmentContainer, new OrderHistoryFragment())
                    .commit();
        });

        // Go back to shopping
        btnContinueShopping.setOnClickListener(v -> {
            requireActivity().getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.customerFragmentContainer, new CustomerHomeFragment())
                    .commit();
        });
    }
}
