package com.storepilot.manager.adapters;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Order;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

// Manager order list — shows all orders with status update dropdowns
public class ManagerOrderAdapter extends RecyclerView.Adapter<ManagerOrderAdapter.ViewHolder> {

    public interface OnStatusChange { void onChange(Order order, String newStatus); }

    private List<Order> orders;
    private final OnStatusChange statusChangeListener;
    private final SimpleDateFormat sdf = new SimpleDateFormat("MMM d, yyyy HH:mm", Locale.getDefault());

    // Available order statuses the manager can set
    private static final String[] STATUSES = {"PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"};

    public ManagerOrderAdapter(List<Order> orders, OnStatusChange listener) {
        this.orders = orders;
        this.statusChangeListener = listener;
    }

    public void setOrders(List<Order> orders) {
        this.orders = orders;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_manager_order, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Order order = orders.get(position);

        holder.tvOrderId.setText("Order #" + order.getId());
        holder.tvCustomerId.setText("Customer #" + order.getCustomerId());
        holder.tvDate.setText(sdf.format(new Date(order.getCreatedAt())));
        holder.tvTotal.setText(String.format("$%.2f", order.getTotalPrice()));
        holder.tvPayment.setText(order.getPaymentMethod().replace("_", " "));

        // Show the current status with a color
        holder.tvCurrentStatus.setText(order.getStatus());
        colorStatus(holder.tvCurrentStatus, order.getStatus());

        // Set up the status spinner to the current status
        ArrayAdapter<String> spinnerAdapter = new ArrayAdapter<>(
                holder.itemView.getContext(),
                android.R.layout.simple_spinner_item,
                STATUSES);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        holder.spinnerStatus.setAdapter(spinnerAdapter);

        // Pre-select the current status in the spinner
        for (int i = 0; i < STATUSES.length; i++) {
            if (STATUSES[i].equals(order.getStatus())) {
                holder.spinnerStatus.setSelection(i);
                break;
            }
        }

        // When manager changes the spinner, update the order status
        holder.spinnerStatus.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener() {
            boolean firstTime = true;
            @Override
            public void onItemSelected(android.widget.AdapterView<?> parent, View view, int pos, long id) {
                if (firstTime) { firstTime = false; return; } // skip initial selection
                String newStatus = STATUSES[pos];
                if (!newStatus.equals(order.getStatus())) {
                    statusChangeListener.onChange(order, newStatus);
                }
            }
            @Override public void onNothingSelected(android.widget.AdapterView<?> parent) {}
        });
    }

    // Apply color based on status string
    private void colorStatus(TextView tv, String status) {
        switch (status) {
            case "PENDING":    tv.setTextColor(Color.parseColor("#FF9800")); break;
            case "PROCESSING": tv.setTextColor(Color.parseColor("#2196F3")); break;
            case "SHIPPED":    tv.setTextColor(Color.parseColor("#9C27B0")); break;
            case "DELIVERED":  tv.setTextColor(Color.parseColor("#4CAF50")); break;
            case "CANCELLED":  tv.setTextColor(Color.parseColor("#F44336")); break;
        }
    }

    @Override
    public int getItemCount() { return orders.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvOrderId, tvCustomerId, tvDate, tvTotal, tvPayment, tvCurrentStatus;
        Spinner spinnerStatus;

        ViewHolder(View v) {
            super(v);
            tvOrderId = v.findViewById(R.id.tvManagerOrderId);
            tvCustomerId = v.findViewById(R.id.tvManagerCustomerId);
            tvDate = v.findViewById(R.id.tvManagerOrderDate);
            tvTotal = v.findViewById(R.id.tvManagerOrderTotal);
            tvPayment = v.findViewById(R.id.tvManagerPayment);
            tvCurrentStatus = v.findViewById(R.id.tvManagerCurrentStatus);
            spinnerStatus = v.findViewById(R.id.spinnerOrderStatus);
        }
    }
}
