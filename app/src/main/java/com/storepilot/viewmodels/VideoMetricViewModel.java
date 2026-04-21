package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.VideoMetric;
import com.storepilot.repositories.VideoMetricRepository;

import java.util.List;

public class VideoMetricViewModel extends AndroidViewModel {

    private final VideoMetricRepository repository;

    public VideoMetricViewModel(@NonNull Application application) {
        super(application);
        repository = new VideoMetricRepository(application);
    }

    public LiveData<List<VideoMetric>> getAllMetrics() {
        return repository.getAllMetrics();
    }

    public LiveData<VideoMetric> getById(int id) {
        return repository.getById(id);
    }

    public void insert(VideoMetric metric) {
        repository.insert(metric);
    }

    public void update(VideoMetric metric) {
        repository.update(metric);
    }

    public void delete(VideoMetric metric) {
        repository.delete(metric);
    }
}
