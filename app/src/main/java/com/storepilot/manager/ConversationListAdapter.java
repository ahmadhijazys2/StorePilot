package com.storepilot.manager;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.User;

import java.util.List;

// Shows each customer conversation as a row in the support inbox list
public class ConversationListAdapter extends RecyclerView.Adapter<ConversationListAdapter.ViewHolder> {

    public interface OnConversationClick { void onClick(User customer); }

    private final List<User> customers;
    private final OnConversationClick listener;

    public ConversationListAdapter(List<User> customers, OnConversationClick listener) {
        this.customers = customers;
        this.listener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_conversation, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        User customer = customers.get(position);
        // Show customer name and a placeholder for last message preview
        holder.tvName.setText(customer.getFullName());
        holder.tvPreview.setText("Tap to view conversation");
        // Open the conversation on tap
        holder.itemView.setOnClickListener(v -> listener.onClick(customer));
    }

    @Override
    public int getItemCount() { return customers.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvName, tvPreview;

        ViewHolder(View v) {
            super(v);
            tvName = v.findViewById(R.id.tvCustomerName);
            tvPreview = v.findViewById(R.id.tvMessagePreview);
        }
    }
}
