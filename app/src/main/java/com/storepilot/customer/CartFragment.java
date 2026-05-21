package com.storepilot.customer;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.core.AppDatabase;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.CartItemAdapter;
import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Product;
import com.storepilot.viewmodels.CartViewModel;
import com.storepilot.viewmodels.ProductViewModel;

import java.util.ArrayList;
import java.util.List;

// Shopping cart screen — shows items the customer wants to buy
public class CartFragment extends Fragment {

    private RecyclerView rvCart;
    private TextView tvTotal, tvEmpty;
    private Button btnCheckout;
    private CartViewModel cartViewModel;
    private ProductViewModel productViewModel;
    private CartItemAdapter adapter;

    // Current list of cart items (needed for checkout)
    private List<CartItem> currentCartItems = new ArrayList<>();
    // Product details matched to cart items
    private List<Product> currentProducts = new ArrayList<>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_cart, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvCart = view.findViewById(R.id.rvCart);
        tvTotal = view.findViewById(R.id.tvCartTotal);
        tvEmpty = view.findViewById(R.id.tvCartEmpty);
        btnCheckout = view.findViewById(R.id.btnCheckout);

        rvCart.setLayoutManager(new LinearLayoutManager(requireContext()));
        cartViewModel = new ViewModelProvider(requireActivity()).get(CartViewModel.class);
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        // Adapter handles quantity buttons and item removal
        adapter = new CartItemAdapter(new ArrayList<>(), new ArrayList<>(),
                cartItem -> cartViewModel.addToCart(customerId, cartItem.getProductId()),
                cartItem -> cartViewModel.removeOne(cartItem),
                cartItem -> cartViewModel.removeFromCart(cartItem.getId())
        );
        rvCart.setAdapter(adapter);

        // Load all products once (needed to show names and prices)
        productViewModel.getAllProducts().observe(getViewLifecycleOwner(), products -> {
            currentProducts = products != null ? products : new ArrayList<>();
            refreshCart();
        });

        // Observe cart items and update UI
        cartViewModel.getCartItems(customerId).observe(getViewLifecycleOwner(), cartItems -> {
            currentCartItems = cartItems != null ? cartItems : new ArrayList<>();
            refreshCart();
        });

        // Go to checkout screen
        btnCheckout.setOnClickListener(v -> {
            if (currentCartItems.isEmpty()) return;
            CheckoutFragment checkout = new CheckoutFragment();
            requireActivity().getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.customerFragmentContainer, checkout)
                    .addToBackStack(null)
                    .commit();
        });
    }

    // Update adapter and recalculate total price
    private void refreshCart() {
        adapter.update(currentCartItems, currentProducts);

        // Calculate total by matching cart items to product prices
        double total = 0;
        for (CartItem ci : currentCartItems) {
            for (Product p : currentProducts) {
                if (p.getId() == ci.getProductId()) {
                    total += p.getPrice() * ci.getQuantity();
                    break;
                }
            }
        }
        tvTotal.setText(String.format("Total: $%.2f", total));

        // Show empty state if cart is empty
        boolean isEmpty = currentCartItems.isEmpty();
        tvEmpty.setVisibility(isEmpty ? View.VISIBLE : View.GONE);
        rvCart.setVisibility(isEmpty ? View.GONE : View.VISIBLE);
        btnCheckout.setEnabled(!isEmpty);
    }
}
