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
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.CustomerProductAdapter;
import com.storepilot.db.entities.Favorite;
import com.storepilot.db.entities.Product;
import com.storepilot.viewmodels.CartViewModel;
import com.storepilot.viewmodels.FavoritesViewModel;
import com.storepilot.viewmodels.ProductViewModel;

import java.util.ArrayList;
import java.util.List;

// Customer's wishlist — shows products the customer has favorited
public class FavoritesFragment extends Fragment {

    private RecyclerView rvFavorites;
    private TextView tvEmpty;
    private FavoritesViewModel favoritesViewModel;
    private ProductViewModel productViewModel;
    private CartViewModel cartViewModel;
    private CustomerProductAdapter adapter;

    // Cached latest values from both LiveData streams
    private List<Favorite> latestFavorites = new ArrayList<>();
    private List<Product> latestProducts = new ArrayList<>();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_favorites, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvFavorites = view.findViewById(R.id.rvFavorites);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        rvFavorites.setLayoutManager(new GridLayoutManager(requireContext(), 2));

        favoritesViewModel = new ViewModelProvider(this).get(FavoritesViewModel.class);
        productViewModel = new ViewModelProvider(this).get(ProductViewModel.class);
        cartViewModel = new ViewModelProvider(requireActivity()).get(CartViewModel.class);

        int customerId = SessionManager.getInstance().getLoggedInUser().getId();

        adapter = new CustomerProductAdapter(new ArrayList<>(), product -> {
            ProductDetailFragment detail = new ProductDetailFragment();
            Bundle args = new Bundle();
            args.putInt("productId", product.getId());
            detail.setArguments(args);
            requireActivity().getSupportFragmentManager()
                    .beginTransaction()
                    .replace(R.id.customerFragmentContainer, detail)
                    .addToBackStack(null)
                    .commit();
        }, product -> cartViewModel.addToCart(customerId, product.getId()));

        rvFavorites.setAdapter(adapter);

        // Observe favorites and products independently, then combine when either changes
        favoritesViewModel.getFavorites(customerId).observe(getViewLifecycleOwner(), favorites -> {
            latestFavorites = favorites != null ? favorites : new ArrayList<>();
            updateFavoritesDisplay();
        });

        productViewModel.getAllProducts().observe(getViewLifecycleOwner(), products -> {
            latestProducts = products != null ? products : new ArrayList<>();
            updateFavoritesDisplay();
        });
    }

    // Build the product list from the intersection of favorites and all products
    private void updateFavoritesDisplay() {
        List<Product> favProducts = new ArrayList<>();
        for (Favorite fav : latestFavorites) {
            for (Product p : latestProducts) {
                if (p.getId() == fav.getProductId()) {
                    favProducts.add(p);
                    break;
                }
            }
        }
        adapter.setProducts(favProducts);
        boolean empty = favProducts.isEmpty();
        tvEmpty.setVisibility(empty ? View.VISIBLE : View.GONE);
        rvFavorites.setVisibility(empty ? View.GONE : View.VISIBLE);
    }
}
