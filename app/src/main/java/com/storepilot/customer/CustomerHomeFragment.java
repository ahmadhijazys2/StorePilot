package com.storepilot.customer;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.CustomerProductAdapter;
import com.storepilot.db.entities.Product;
import com.storepilot.viewmodels.CartViewModel;
import com.storepilot.viewmodels.ProductViewModel;

import java.util.ArrayList;
import java.util.List;

// Customer home screen showing all products in a searchable grid
public class CustomerHomeFragment extends Fragment {

    private RecyclerView rvProducts;
    private EditText etSearch;
    private TextView tvGreeting, tvEmpty;
    private ProductViewModel productViewModel;
    private CartViewModel cartViewModel;
    private CustomerProductAdapter adapter;

    // Full list of products for filtering
    private List<Product> allProducts = new ArrayList<>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_customer_home, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // Bind views
        rvProducts = view.findViewById(R.id.rvProducts);
        etSearch = view.findViewById(R.id.etSearch);
        tvGreeting = view.findViewById(R.id.tvGreeting);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        // Show personalized greeting
        String name = SessionManager.getInstance().getLoggedInUser().getFullName();
        tvGreeting.setText("Hello, " + name + " 👋");

        // Set up product grid (2 columns)
        rvProducts.setLayoutManager(new GridLayoutManager(requireContext(), 2));

        // Get ViewModels
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);
        cartViewModel = new ViewModelProvider(requireActivity()).get(CartViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        // Create adapter — handles product card clicks and add-to-cart
        adapter = new CustomerProductAdapter(new ArrayList<>(), product -> {
            // Navigate to product details screen
            ProductDetailFragment detail = new ProductDetailFragment();
            Bundle args = new Bundle();
            args.putInt("productId", product.getId());
            detail.setArguments(args);
            requireActivity().getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.customerFragmentContainer, detail)
                    .addToBackStack(null)
                    .commit();
        }, product -> {
            // Add to cart button tapped
            cartViewModel.addToCart(customerId, product.getId());
        });

        rvProducts.setAdapter(adapter);

        // Load products and update the grid
        productViewModel.getAllProducts().observe(getViewLifecycleOwner(), products -> {
            allProducts = products != null ? products : new ArrayList<>();
            filterProducts(etSearch.getText().toString());
        });

        // Live search as user types
        etSearch.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) {
                filterProducts(s.toString());
            }
            @Override public void afterTextChanged(Editable s) {}
        });
    }

    // Filter product list by name or category matching the search text
    private void filterProducts(String query) {
        List<Product> filtered = new ArrayList<>();
        String q = query.toLowerCase().trim();
        for (Product p : allProducts) {
            if (q.isEmpty() || p.getName().toLowerCase().contains(q)
                    || p.getCategory().toLowerCase().contains(q)) {
                filtered.add(p);
            }
        }
        adapter.setProducts(filtered);
        // Show empty state if no results
        tvEmpty.setVisibility(filtered.isEmpty() ? View.VISIBLE : View.GONE);
        rvProducts.setVisibility(filtered.isEmpty() ? View.GONE : View.VISIBLE);
    }
}
