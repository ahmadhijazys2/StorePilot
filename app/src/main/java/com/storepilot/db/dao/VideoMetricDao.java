package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.VideoMetric;

import java.util.List;

@Dao
public interface VideoMetricDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(VideoMetric metric);

    @Update
    void update(VideoMetric metric);

    @Delete
    void delete(VideoMetric metric);

    @Query("SELECT * FROM video_metrics ORDER BY videoDate DESC")
    LiveData<List<VideoMetric>> getAllMetrics();

    @Query("SELECT * FROM video_metrics WHERE id = :id LIMIT 1")
    LiveData<VideoMetric> getById(int id);
}
