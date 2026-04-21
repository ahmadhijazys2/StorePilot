package com.storepilot.inventory;

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
import com.storepilot.viewmodels.ProductViewModel;

public class ProductDetailsFragment extends Fragment {

    private static final String ARG_PRODUCT_ID = "productId";

    public static ProductDetailsFragment newInstance(int productId) {
        ProductDetailsFragment fragment = new ProductDetailsFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_PRODUCT_ID, productId);
        fragment.setArguments(args);
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_product_details, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        TextView tvName = view.findViewById(R.id.tvDetailName);
        TextView tvCategory = view.findViewById(R.id.tvDetailCategory);
        TextView tvSize = view.findViewById(R.id.tvDetailSize);
        TextView tvColor = view.findViewById(R.id.tvDetailColor);
        TextView tvQuantity = view.findViewById(R.id.tvDetailQuantity);
        TextView tvPrice = view.findViewById(R.id.tvDetailPrice);
        TextView tvCostPrice = view.findViewById(R.id.tvDetailCostPrice);

        int productId = getArguments() != null ? getArguments().getInt(ARG_PRODUCT_ID, -1) : -1;
        if (productId == -1) return;

        ProductViewModel vm = new ViewModelProvider(this).get(ProductViewModel.class);
        vm.getById(productId).observe(getViewLifecycleOwner(), product -> {
            if (product != null) {
                tvName.setText(product.getName());
                tvCategory.setText(product.getCategory());
                tvSize.setText(product.getSize());
                tvColor.setText(product.getColor());
                tvQuantity.setText(String.valueOf(product.getQuantity()));
                tvPrice.setText(String.format("$%.2f", product.getPrice()));
                tvCostPrice.setText(String.format("$%.2f", product.getCostPrice()));
            }
        });
    }
}
