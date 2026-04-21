package com.storepilot.admin;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.viewmodels.AuthViewModel;

import java.util.List;

public class UserManagementFragment extends Fragment {

    private RecyclerView recyclerView;
    private UserAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_user_management, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        recyclerView = view.findViewById(R.id.recyclerUsers);
        adapter = new UserAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);

        // Use AuthViewModel's repository indirectly via a shared ViewModel
        // For simplicity, load users via a ProductViewModel equivalent
        com.storepilot.repositories.UserRepository repo =
                new com.storepilot.repositories.UserRepository(requireActivity().getApplication());
        repo.getAllUsers().observe(getViewLifecycleOwner(), users -> adapter.setUsers(users));
    }
}
