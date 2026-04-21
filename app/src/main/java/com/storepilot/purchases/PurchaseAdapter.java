package com.storepilot.purchases;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Purchase;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class PurchaseAdapter extends RecyclerView.Adapter<PurchaseAdapter.ViewHolder> {

    private List<Purchase> purchases = new ArrayList<>();

    public void setPurchases(List<Purchase> purchases) {
        this.purchases = purchases != null ? purchases : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_purchase, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Purchase p = purchases.get(position);
        holder.tvPurchaseDate.setText(new SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
                .format(new Date(p.getPurchaseDate())));
        holder.tvPurchaseTotal.setText(String.format("$%.2f", p.getTotalCost()));
        holder.tvPurchaseSupplier.setText(p.getSupplier() != null ? p.getSupplier() : "");
        holder.tvPurchaseQty.setText("Qty: " + p.getQuantity());
    }

    @Override
    public int getItemCount() {
        return purchases.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvPurchaseDate, tvPurchaseTotal, tvPurchaseSupplier, tvPurchaseQty;

        ViewHolder(View itemView) {
            super(itemView);
            tvPurchaseDate = itemView.findViewById(R.id.tvPurchaseDate);
            tvPurchaseTotal = itemView.findViewById(R.id.tvPurchaseTotal);
            tvPurchaseSupplier = itemView.findViewById(R.id.tvPurchaseSupplier);
            tvPurchaseQty = itemView.findViewById(R.id.tvPurchaseQty);
        }
    }
}
