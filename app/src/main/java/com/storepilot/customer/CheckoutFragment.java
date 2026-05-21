package com.storepilot.customer;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.SessionManager;
import com.storepilot.viewmodels.CartViewModel;
import com.storepilot.viewmodels.OrderViewModel;
import com.storepilot.viewmodels.ProductViewModel;

import java.util.ArrayList;

// Checkout screen — collects shipping address and payment method, then places the order
public class CheckoutFragment extends Fragment {

    private EditText etAddress;
    private RadioGroup rgPayment;
    private Button btnPlaceOrder;
    private CartViewModel cartViewModel;
    private OrderViewModel orderViewModel;
    private ProductViewModel productViewModel;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_checkout, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        etAddress = view.findViewById(R.id.etShippingAddress);
        rgPayment = view.findViewById(R.id.rgPaymentMethod);
        btnPlaceOrder = view.findViewById(R.id.btnPlaceOrder);

        cartViewModel = new ViewModelProvider(requireActivity()).get(CartViewModel.class);
        orderViewModel = new ViewModelProvider(this).get(OrderViewModel.class);
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        // Listen for successful order placement
        orderViewModel.orderPlaced.observe(getViewLifecycleOwner(), placed -> {
            if (Boolean.TRUE.equals(placed)) {
                // Show order confirmation screen
                requireActivity().getSupportFragmentManager()
                        .beginTransaction()
                        .replace(R.id.customerFragmentContainer, new OrderConfirmationFragment())
                        .commit();
            }
        });

        btnPlaceOrder.setOnClickListener(v -> {
            String address = etAddress.getText().toString().trim();
            if (address.isEmpty()) {
                Toast.makeText(requireContext(), "Please enter your shipping address.", Toast.LENGTH_SHORT).show();
                return;
            }

            // Map radio button to payment method string
            int selectedId = rgPayment.getCheckedRadioButtonId();
            String paymentMethod;
            if (selectedId == R.id.rbCash) {
                paymentMethod = "CASH_ON_DELIVERY";
            } else if (selectedId == R.id.rbPaypal) {
                paymentMethod = "PAYPAL";
            } else {
                paymentMethod = "CREDIT_CARD";
            }

            btnPlaceOrder.setEnabled(false);

            // Get cart and products to place the order
            cartViewModel.getCartItems(customerId).observe(getViewLifecycleOwner(), cartItems -> {
                productViewModel.getAllProducts().observe(getViewLifecycleOwner(), products -> {
                    if (cartItems == null || cartItems.isEmpty()) {
                        Toast.makeText(requireContext(), "Your cart is empty.", Toast.LENGTH_SHORT).show();
                        btnPlaceOrder.setEnabled(true);
                        return;
                    }
                    // Place the order
                    orderViewModel.placeOrder(customerId, paymentMethod, address,
                            cartItems, products != null ? products : new ArrayList<>());
                });
            });
        });
    }
}
