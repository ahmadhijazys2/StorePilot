package com.storepilot.seasons;

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
import com.storepilot.R;
import com.storepilot.viewmodels.SeasonViewModel;

public class SeasonListFragment extends Fragment {

    private RecyclerView recyclerView;
    private FloatingActionButton fabAdd;
    private SeasonAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_season_list, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        recyclerView = view.findViewById(R.id.recyclerSeasons);
        fabAdd = view.findViewById(R.id.fabAddSeason);
        adapter = new SeasonAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);

        SeasonViewModel vm = new ViewModelProvider(this).get(SeasonViewModel.class);
        vm.getAllSeasons().observe(getViewLifecycleOwner(), seasons -> adapter.setSeasons(seasons));

        fabAdd.setOnClickListener(v ->
                startActivity(new Intent(getActivity(), AddEditSeasonActivity.class)));
    }
}
