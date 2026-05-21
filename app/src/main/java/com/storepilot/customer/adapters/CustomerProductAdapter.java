package com.storepilot.customer.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Product;

import java.util.List;

// Shows products as cards in the customer's home/catalog grid
public class CustomerProductAdapter extends RecyclerView.Adapter<CustomerProductAdapter.ViewHolder> {

    // Callback for when a product card is tapped (open detail)
    public interface OnProductClick { void onClick(Product product); }
    // Callback for when the Add to Cart button is tapped
    public interface OnAddToCart { void onAdd(Product product); }

    private List<Product> products;
    private final OnProductClick clickListener;
    private final OnAddToCart addToCartListener;

    public CustomerProductAdapter(List<Product> products,
                                  OnProductClick clickListener,
                                  OnAddToCart addToCartListener) {
        this.products = products;
        this.clickListener = clickListener;
        this.addToCartListener = addToCartListener;
    }

    // Replace the list and refresh the grid
    public void setProducts(List<Product> newList) {
        this.products = newList;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_customer_product, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Product p = products.get(position);

        // Fill in product details
        holder.tvName.setText(p.getName());
        holder.tvCategory.setText(p.getCategory());
        holder.tvPrice.setText(String.format("$%.2f", p.getPrice()));

        // Show availability status
        if (p.getQuantity() > 0) {
            holder.tvStock.setText("In Stock");
            holder.tvStock.setTextColor(0xFF4CAF50); // green
        } else {
            holder.tvStock.setText("Out of Stock");
            holder.tvStock.setTextColor(0xFFF44336); // red
        }

        // Tap anywhere on card to view product details
        holder.itemView.setOnClickListener(v -> clickListener.onClick(p));

        // Add to cart button
        holder.btnAddToCart.setOnClickListener(v -> addToCartListener.onAdd(p));
        holder.btnAddToCart.setEnabled(p.getQuantity() > 0);
    }

    @Override
    public int getItemCount() { return products.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvName, tvCategory, tvPrice, tvStock;
        Button btnAddToCart;

        ViewHolder(View v) {
            super(v);
            tvName = v.findViewById(R.id.tvProductName);
            tvCategory = v.findViewById(R.id.tvProductCategory);
            tvPrice = v.findViewById(R.id.tvProductPrice);
            tvStock = v.findViewById(R.id.tvProductStock);
            btnAddToCart = v.findViewById(R.id.btnAddToCart);
        }
    }
}
