package com.storepilot.reports;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.google.android.material.chip.Chip;
import com.storepilot.R;
import com.storepilot.viewmodels.ReportsViewModel;

import java.text.NumberFormat;
import java.util.Calendar;
import java.util.Locale;

public class ReportsFragment extends Fragment {

    private TextView tvSalesTotal;
    private Chip chipWeek, chipMonth, chipYear;
    private ReportsViewModel viewModel;
    private final androidx.lifecycle.MutableLiveData<Integer> filterMode =
            new androidx.lifecycle.MutableLiveData<>(1); // 0=week,1=month,2=year

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_reports, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        tvSalesTotal = view.findViewById(R.id.tvReportSalesTotal);
        chipWeek = view.findViewById(R.id.chipWeek);
        chipMonth = view.findViewById(R.id.chipMonth);
        chipYear = view.findViewById(R.id.chipYear);

        viewModel = new ViewModelProvider(this).get(ReportsViewModel.class);

        long now = System.currentTimeMillis();

        androidx.lifecycle.LiveData<Double> salesData =
                androidx.lifecycle.Transformations.switchMap(filterMode, mode -> {
                    if (mode == null || mode == 1) return viewModel.getSalesTotalByMonth(now);
                    if (mode == 0) return viewModel.getSalesTotalByWeek(now);
                    return viewModel.getSalesTotalByYear(now);
                });
        salesData.observe(getViewLifecycleOwner(), this::showTotal);

        chipWeek.setOnClickListener(v -> filterMode.setValue(0));
        chipMonth.setOnClickListener(v -> filterMode.setValue(1));
        chipYear.setOnClickListener(v -> filterMode.setValue(2));

        chipMonth.setChecked(true);
    }

    private void showTotal(Double total) {
        double value = (total != null) ? total : 0.0;
        tvSalesTotal.setText(NumberFormat.getCurrencyInstance(Locale.US).format(value));
    }
}
