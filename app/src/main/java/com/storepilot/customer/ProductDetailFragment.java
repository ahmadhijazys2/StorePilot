package com.storepilot.customer;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.AppDatabase;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.Product;
import com.storepilot.viewmodels.CartViewModel;
import com.storepilot.viewmodels.FavoritesViewModel;

// Shows full details for a single product
public class ProductDetailFragment extends Fragment {

    private int productId;
    private CartViewModel cartViewModel;
    private FavoritesViewModel favoritesViewModel;
    private Button btnFavorite;
    private boolean isFavorited = false;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_product_detail, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // Read product ID passed from the product list
        productId = getArguments() != null ? getArguments().getInt("productId", -1) : -1;

        TextView tvName = view.findViewById(R.id.tvProductName);
        TextView tvCategory = view.findViewById(R.id.tvCategory);
        TextView tvPrice = view.findViewById(R.id.tvPrice);
        TextView tvDescription = view.findViewById(R.id.tvDescription);
        TextView tvStock = view.findViewById(R.id.tvStock);
        Button btnAddToCart = view.findViewById(R.id.btnAddToCart);
        btnFavorite = view.findViewById(R.id.btnFavorite);
        ImageView ivBack = view.findViewById(R.id.ivBack);

        cartViewModel = new ViewModelProvider(requireActivity()).get(CartViewModel.class);
        favoritesViewModel = new ViewModelProvider(this).get(FavoritesViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        // Load product from the database in background
        AppDatabase.dbExecutor.execute(() -> {
            Product product = AppDatabase.getInstance(requireContext())
                    .productDao().findById(productId);
            if (product == null) return;

            // Update UI on the main thread
            requireActivity().runOnUiThread(() -> {
                tvName.setText(product.getName());
                tvCategory.setText(product.getCategory() + " • " + product.getColor() + " • " + product.getSize());
                tvPrice.setText(String.format("$%.2f", product.getPrice()));
                tvDescription.setText("A quality " + product.getName().toLowerCase() +
                        " from our " + product.getCategory() + " collection.");
                tvStock.setText(product.getQuantity() > 0
                        ? "In Stock (" + product.getQuantity() + " available)"
                        : "Out of Stock");

                // Disable cart button if out of stock
                btnAddToCart.setEnabled(product.getQuantity() > 0);
            });

            // Check if product is already in favorites
            AppDatabase db = AppDatabase.getInstance(requireContext());
            isFavorited = db.favoriteDao().getFavorite(customerId, productId) != null;
            requireActivity().runOnUiThread(() ->
                    btnFavorite.setText(isFavorited ? "♥ Saved" : "♡ Save"));
        });

        // Add product to cart
        btnAddToCart.setOnClickListener(v -> {
            cartViewModel.addToCart(customerId, productId);
            Toast.makeText(requireContext(), "Added to cart!", Toast.LENGTH_SHORT).show();
        });

        // Toggle favorite
        btnFavorite.setOnClickListener(v -> {
            favoritesViewModel.toggleFavorite(customerId, productId);
            isFavorited = !isFavorited;
            btnFavorite.setText(isFavorited ? "♥ Saved" : "♡ Save");
            Toast.makeText(requireContext(),
                    isFavorited ? "Saved to wishlist" : "Removed from wishlist",
                    Toast.LENGTH_SHORT).show();
        });

        // Go back to previous screen
        ivBack.setOnClickListener(v -> requireActivity().onBackPressed());
    }
}
