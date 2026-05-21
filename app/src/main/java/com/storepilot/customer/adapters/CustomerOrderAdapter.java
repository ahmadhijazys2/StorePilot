package com.storepilot.customer.adapters;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Order;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

// Shows a list of customer orders with their status
public class CustomerOrderAdapter extends RecyclerView.Adapter<CustomerOrderAdapter.ViewHolder> {

    private List<Order> orders;
    // Formatter for order dates
    private final SimpleDateFormat sdf = new SimpleDateFormat("MMM d, yyyy", Locale.getDefault());

    public CustomerOrderAdapter(List<Order> orders) {
        this.orders = orders;
    }

    public void setOrders(List<Order> orders) {
        this.orders = orders;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_customer_order, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Order order = orders.get(position);

        // Show order ID and date
        holder.tvOrderId.setText("Order #" + order.getId());
        holder.tvDate.setText(sdf.format(new Date(order.getCreatedAt())));
        holder.tvTotal.setText(String.format("$%.2f", order.getTotalPrice()));
        holder.tvPayment.setText(order.getPaymentMethod().replace("_", " "));
        holder.tvStatus.setText(order.getStatus());

        // Color-code the status badge
        switch (order.getStatus()) {
            case "PENDING":    holder.tvStatus.setTextColor(Color.parseColor("#FF9800")); break; // orange
            case "PROCESSING": holder.tvStatus.setTextColor(Color.parseColor("#2196F3")); break; // blue
            case "SHIPPED":    holder.tvStatus.setTextColor(Color.parseColor("#9C27B0")); break; // purple
            case "DELIVERED":  holder.tvStatus.setTextColor(Color.parseColor("#4CAF50")); break; // green
            case "CANCELLED":  holder.tvStatus.setTextColor(Color.parseColor("#F44336")); break; // red
        }
    }

    @Override
    public int getItemCount() { return orders.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvOrderId, tvDate, tvTotal, tvPayment, tvStatus;

        ViewHolder(View v) {
            super(v);
            tvOrderId = v.findViewById(R.id.tvOrderId);
            tvDate = v.findViewById(R.id.tvOrderDate);
            tvTotal = v.findViewById(R.id.tvOrderTotal);
            tvPayment = v.findViewById(R.id.tvPaymentMethod);
            tvStatus = v.findViewById(R.id.tvOrderStatus);
        }
    }
}
