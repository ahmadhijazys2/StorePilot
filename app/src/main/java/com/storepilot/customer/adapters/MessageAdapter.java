package com.storepilot.customer.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.SupportMessage;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

// Chat message adapter — shows sent messages on the right, received on the left
public class MessageAdapter extends RecyclerView.Adapter<MessageAdapter.ViewHolder> {

    // Two view types: one for sent messages, one for received
    private static final int VIEW_SENT = 1;
    private static final int VIEW_RECEIVED = 2;

    private List<SupportMessage> messages;
    private final int currentUserId;
    private final SimpleDateFormat timeFormat = new SimpleDateFormat("h:mm a", Locale.getDefault());

    public MessageAdapter(List<SupportMessage> messages, int currentUserId) {
        this.messages = messages;
        this.currentUserId = currentUserId;
    }

    public void setMessages(List<SupportMessage> messages) {
        this.messages = messages;
        notifyDataSetChanged();
    }

    // Determine which layout to use based on who sent the message
    @Override
    public int getItemViewType(int position) {
        return messages.get(position).getSenderId() == currentUserId
                ? VIEW_SENT : VIEW_RECEIVED;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        int layout = viewType == VIEW_SENT
                ? R.layout.item_message_sent
                : R.layout.item_message_received;
        View v = LayoutInflater.from(parent.getContext()).inflate(layout, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        SupportMessage msg = messages.get(position);

        // Set the message text
        holder.tvMessageText.setText(msg.getMessageText());

        // Show formatted time
        holder.tvTimestamp.setText(timeFormat.format(new Date(msg.getTimestamp())));

        // Show sender name on received messages
        if (holder.tvSenderName != null) {
            // Manager/Owner messages show the role as sender label
            holder.tvSenderName.setText("Support Team");
        }
    }

    @Override
    public int getItemCount() { return messages.size(); }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvMessageText, tvTimestamp, tvSenderName;

        ViewHolder(View v) {
            super(v);
            tvMessageText = v.findViewById(R.id.tvMessageText);
            tvTimestamp = v.findViewById(R.id.tvTimestamp);
            tvSenderName = v.findViewById(R.id.tvSenderName); // may be null for sent layout
        }
    }
}
