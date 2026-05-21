package com.storepilot.manager;

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
import com.storepilot.core.AppDatabase;
import com.storepilot.core.SessionManager;
import com.storepilot.customer.adapters.MessageAdapter;
import com.storepilot.db.entities.User;
import com.storepilot.viewmodels.SupportViewModel;

import java.util.ArrayList;

// Manager's support chat — shows conversation with a specific customer and allows replies
public class SupportInboxFragment extends Fragment {

    // The customer ID whose conversation is being viewed
    private int targetCustomerId;
    private RecyclerView rvMessages;
    private EditText etReply;
    private ImageButton btnSend;
    private TextView tvCustomerName, tvEmpty;
    private SupportViewModel supportViewModel;
    private MessageAdapter adapter;

    // Pass the customer ID when navigating to this fragment
    public static SupportInboxFragment forCustomer(int customerId) {
        SupportInboxFragment f = new SupportInboxFragment();
        Bundle args = new Bundle();
        args.putInt("customerId", customerId);
        f.setArguments(args);
        return f;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_support_inbox, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        targetCustomerId = getArguments() != null ? getArguments().getInt("customerId", -1) : -1;

        rvMessages = view.findViewById(R.id.rvMessages);
        etReply = view.findViewById(R.id.etReply);
        btnSend = view.findViewById(R.id.btnSendReply);
        tvCustomerName = view.findViewById(R.id.tvCustomerName);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        LinearLayoutManager lm = new LinearLayoutManager(requireContext());
        lm.setStackFromEnd(true);
        rvMessages.setLayoutManager(lm);

        supportViewModel = new ViewModelProvider(this).get(SupportViewModel.class);

        User currentUser = SessionManager.getInstance().getLoggedInUser();

        // Show the customer's name in the toolbar
        AppDatabase.dbExecutor.execute(() -> {
            User customer = AppDatabase.getInstance(requireContext()).userDao().findById(targetCustomerId);
            if (customer != null && getActivity() != null) {
                requireActivity().runOnUiThread(() ->
                        tvCustomerName.setText(customer.getFullName()));
            }
        });

        // Use the manager's ID as currentUserId so sent messages appear on the right
        adapter = new MessageAdapter(new ArrayList<>(), currentUser.getId());
        rvMessages.setAdapter(adapter);

        // Load conversation messages
        supportViewModel.getMessages(targetCustomerId).observe(getViewLifecycleOwner(), messages -> {
            adapter.setMessages(messages != null ? messages : new ArrayList<>());
            boolean empty = messages == null || messages.isEmpty();
            tvEmpty.setVisibility(empty ? View.VISIBLE : View.GONE);
            if (!empty) rvMessages.scrollToPosition(messages.size() - 1);
        });

        // Mark messages as read when manager opens the conversation
        supportViewModel.markRead(targetCustomerId);

        // Send a reply from the manager
        btnSend.setOnClickListener(v -> {
            String text = etReply.getText().toString().trim();
            if (text.isEmpty()) return;
            supportViewModel.sendMessage(currentUser.getId(), currentUser.getRole(), text, targetCustomerId);
            etReply.setText("");
        });
    }
}
