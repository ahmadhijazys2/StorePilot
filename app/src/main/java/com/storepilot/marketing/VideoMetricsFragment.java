package com.storepilot.marketing;

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
import com.storepilot.viewmodels.VideoMetricViewModel;

public class VideoMetricsFragment extends Fragment {

    private RecyclerView recyclerView;
    private FloatingActionButton fabAdd;
    private VideoMetricAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_video_metrics, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        recyclerView = view.findViewById(R.id.recyclerVideoMetrics);
        fabAdd = view.findViewById(R.id.fabAddMetric);
        adapter = new VideoMetricAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);

        VideoMetricViewModel vm = new ViewModelProvider(this).get(VideoMetricViewModel.class);
        vm.getAllMetrics().observe(getViewLifecycleOwner(), metrics -> adapter.setMetrics(metrics));

        fabAdd.setOnClickListener(v ->
                startActivity(new Intent(getActivity(), AddMetricActivity.class)));
    }
}
