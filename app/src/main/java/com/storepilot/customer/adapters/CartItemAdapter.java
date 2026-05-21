package com.storepilot.customer.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Product;

import java.util.List;

// Adapter for the cart screen — shows items with quantity controls
public class CartItemAdapter extends RecyclerView.Adapter<CartItemAdapter.ViewHolder> {

    public interface CartAction { void on(CartItem item); }

    private List<CartItem> cartItems;
    private List<Product> products;
    private final CartAction onIncrease, onDecrease, onRemove;

    public CartItemAdapter(List<CartItem> cartItems, List<Product> products,
                           CartAction onIncrease, CartAction onDecrease, CartAction onRemove) {
        this.cartItems = cartItems;
        this.products = products;
        this.onIncrease = onIncrease;
        this.onDecrease = onDecrease;
        this.onRemove = onRemove;
    }

    // Update both cart items and product details at once
    public void update(List<CartItem> cartItems, List<Product> products) {
        this.cartItems = cartItems;
        this.products = products;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_cart, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        CartItem ci = cartItems.get(position);

        // Find matching product to show name and price
        Product product = null;
        for (Product p : products) {
            if (p.getId() == ci.getProductId()) {
                product = p;
                break;
            }
        }

        if (product != null) {
            holder.tvName.setText(product.getName());
            holder.tvUnitPrice.setText(String.format("$%.2f each", product.getPrice()));
            holder.tvSubtotal.setText(String.format("$%.2f", product.getPrice() * ci.getQuantity()));
        }

        // Show quantity
        holder.tvQuantity.setText(String.valueOf(ci.getQuantity()));

        // Quantity buttons
        holder.btnPlus.setOnClickListener(v -> onIncrease.on(ci));
        holder.btnMinus.setOnClickListener(v -> onDecrease.on(ci));
        holder.btnRemove.setOnClickListener(v -> onRemove.on(ci));
    }

    @Override
    public int getItemCount() { return cartItems.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvName, tvUnitPrice, tvQuantity, tvSubtotal;
        ImageButton btnPlus, btnMinus, btnRemove;

        ViewHolder(View v) {
            super(v);
            tvName = v.findViewById(R.id.tvCartItemName);
            tvUnitPrice = v.findViewById(R.id.tvUnitPrice);
            tvQuantity = v.findViewById(R.id.tvQuantity);
            tvSubtotal = v.findViewById(R.id.tvSubtotal);
            btnPlus = v.findViewById(R.id.btnIncrease);
            btnMinus = v.findViewById(R.id.btnDecrease);
            btnRemove = v.findViewById(R.id.btnRemoveItem);
        }
    }
}
