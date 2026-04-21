package com.storepilot.sales;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Sale;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class SaleAdapter extends RecyclerView.Adapter<SaleAdapter.ViewHolder> {

    private List<Sale> sales = new ArrayList<>();

    public void setSales(List<Sale> sales) {
        this.sales = sales != null ? sales : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_sale, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Sale sale = sales.get(position);
        holder.tvSaleDate.setText(new SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
                .format(new Date(sale.getSaleDate())));
        holder.tvSaleTotal.setText(String.format("$%.2f", sale.getTotalPrice()));
        holder.tvSaleQty.setText("Qty: " + sale.getQuantity());
        holder.tvSaleNotes.setText(sale.getNotes() != null ? sale.getNotes() : "");
    }

    @Override
    public int getItemCount() {
        return sales.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvSaleDate, tvSaleTotal, tvSaleQty, tvSaleNotes;

        ViewHolder(View itemView) {
            super(itemView);
            tvSaleDate = itemView.findViewById(R.id.tvSaleDate);
            tvSaleTotal = itemView.findViewById(R.id.tvSaleTotal);
            tvSaleQty = itemView.findViewById(R.id.tvSaleQty);
            tvSaleNotes = itemView.findViewById(R.id.tvSaleNotes);
        }
    }
}
