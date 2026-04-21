package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.VideoMetricDao;
import com.storepilot.db.entities.VideoMetric;

import java.util.List;

public class VideoMetricRepository {

    private final VideoMetricDao videoMetricDao;

    public VideoMetricRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        videoMetricDao = db.videoMetricDao();
    }

    public LiveData<List<VideoMetric>> getAllMetrics() {
        return videoMetricDao.getAllMetrics();
    }

    public LiveData<VideoMetric> getById(int id) {
        return videoMetricDao.getById(id);
    }

    public void insert(VideoMetric metric) {
        AppDatabase.dbExecutor.execute(() -> videoMetricDao.insert(metric));
    }

    public void update(VideoMetric metric) {
        AppDatabase.dbExecutor.execute(() -> videoMetricDao.update(metric));
    }

    public void delete(VideoMetric metric) {
        AppDatabase.dbExecutor.execute(() -> videoMetricDao.delete(metric));
    }
}
