package com.storepilot.manager;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.core.AppDatabase;
import com.storepilot.db.entities.User;
import com.storepilot.viewmodels.SupportViewModel;

import java.util.ArrayList;
import java.util.List;

// Manager inbox — lists all customers who have open support conversations
public class SupportConversationsFragment extends Fragment {

    private RecyclerView rvConversations;
    private TextView tvEmpty;
    private SupportViewModel supportViewModel;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_support_conversations, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        rvConversations = view.findViewById(R.id.rvConversations);
        tvEmpty = view.findViewById(R.id.tvEmpty);

        rvConversations.setLayoutManager(new LinearLayoutManager(requireContext()));
        supportViewModel = new ViewModelProvider(this).get(SupportViewModel.class);

        // Observe the list of customer IDs with conversations
        supportViewModel.getConversationIds().observe(getViewLifecycleOwner(), customerIds -> {
            if (customerIds == null || customerIds.isEmpty()) {
                tvEmpty.setVisibility(View.VISIBLE);
                rvConversations.setVisibility(View.GONE);
                return;
            }

            tvEmpty.setVisibility(View.GONE);
            rvConversations.setVisibility(View.VISIBLE);

            // Load user details for each conversation
            AppDatabase.dbExecutor.execute(() -> {
                List<User> customers = new ArrayList<>();
                for (int id : customerIds) {
                    User u = AppDatabase.getInstance(requireContext()).userDao().findById(id);
                    if (u != null) customers.add(u);
                }

                requireActivity().runOnUiThread(() -> {
                    // Build a simple list of conversation items
                    ConversationListAdapter adapter = new ConversationListAdapter(customers, customer -> {
                        // Open the chat for the selected customer
                        requireActivity().getSupportFragmentManager()
                                .beginTransaction()
                                .replace(R.id.fragmentContainer,
                                        SupportInboxFragment.forCustomer(customer.getId()))
                                .addToBackStack(null)
                                .commit();
                    });
                    rvConversations.setAdapter(adapter);
                });
            });
        });
    }
}
