package com.storepilot.tasks;

import android.content.Intent;
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

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.tabs.TabLayout;
import com.storepilot.R;
import com.storepilot.core.PermissionManager;
import com.storepilot.core.SessionManager;
import com.storepilot.viewmodels.TaskViewModel;

public class TaskListFragment extends Fragment {

    private RecyclerView recyclerView;
    private FloatingActionButton fabAdd;
    private TabLayout tabLayout;
    private TaskAdapter adapter;
    private TaskViewModel taskViewModel;

    // Single MutableLiveData-backed selection to avoid multiple observers
    private androidx.lifecycle.MutableLiveData<Integer> selectedTab =
            new androidx.lifecycle.MutableLiveData<>(0);

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_task_list, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        recyclerView = view.findViewById(R.id.recyclerTasks);
        fabAdd = view.findViewById(R.id.fabAddTask);
        tabLayout = view.findViewById(R.id.tabLayoutTasks);

        adapter = new TaskAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);

        taskViewModel = new ViewModelProvider(this).get(TaskViewModel.class);

        int userId = SessionManager.getInstance().getLoggedInUser() != null
                ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

        // Use switchMap to avoid stacking observers on tab change
        androidx.lifecycle.LiveData<java.util.List<com.storepilot.db.entities.Task>> tasksLiveData =
                androidx.lifecycle.Transformations.switchMap(selectedTab, tab -> {
                    if (tab == null || tab == 0) return taskViewModel.getTasksByUser(userId);
                    if (tab == 1) return taskViewModel.getTeamTasks();
                    return taskViewModel.getPrivateTasks(userId);
                });
        tasksLiveData.observe(getViewLifecycleOwner(), tasks -> adapter.setTasks(tasks));

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                selectedTab.setValue(tab.getPosition());
            }
            @Override public void onTabUnselected(TabLayout.Tab tab) {}
            @Override public void onTabReselected(TabLayout.Tab tab) {}
        });

        fabAdd.setOnClickListener(v ->
                startActivity(new Intent(getActivity(), AddEditTaskActivity.class)));
    }
}
