package com.storepilot.customer;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.MessageAdapter;
import com.storepilot.db.entities.User;
import com.storepilot.viewmodels.SupportViewModel;

import java.util.ArrayList;

// WhatsApp-style support chat screen for customers
public class SupportChatFragment extends Fragment {

    private RecyclerView rvMessages;
    private EditText etMessage;
    private ImageButton btnSend;
    private TextView tvEmpty;
    private SupportViewModel supportViewModel;
    private MessageAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_support_chat, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvMessages = view.findViewById(R.id.rvMessages);
        etMessage = view.findViewById(R.id.etMessage);
        btnSend = view.findViewById(R.id.btnSend);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        // Linear layout so messages appear in order, newest at bottom
        LinearLayoutManager layoutManager = new LinearLayoutManager(requireContext());
        layoutManager.setStackFromEnd(true);
        rvMessages.setLayoutManager(layoutManager);

        supportViewModel = new ViewModelProvider(this).get(SupportViewModel.class);

        User currentUser = SessionManager.getInstance().getLoggedInUser();
        int customerId = currentUser.getId();

        // Adapter shows sent messages on the right, received on the left
        adapter = new MessageAdapter(new ArrayList<>(), currentUser.getId());
        rvMessages.setAdapter(adapter);

        // Load messages and scroll to bottom when they update
        supportViewModel.getMessages(customerId).observe(getViewLifecycleOwner(), messages -> {
            adapter.setMessages(messages != null ? messages : new ArrayList<>());
            boolean empty = messages == null || messages.isEmpty();
            tvEmpty.setVisibility(empty ? View.VISIBLE : View.GONE);
            // Scroll to latest message
            if (!empty) {
                rvMessages.scrollToPosition(messages.size() - 1);
            }
        });

        // Mark all messages as read when the chat is opened
        supportViewModel.markRead(customerId);

        // Send button — post the message
        btnSend.setOnClickListener(v -> {
            String text = etMessage.getText().toString().trim();
            if (text.isEmpty()) return;

            supportViewModel.sendMessage(currentUser.getId(), currentUser.getRole(), text, customerId);
            etMessage.setText("");
        });
    }
}
