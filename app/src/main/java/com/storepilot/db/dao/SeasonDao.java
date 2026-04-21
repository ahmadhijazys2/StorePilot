package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Season;

import java.util.List;

@Dao
public interface SeasonDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Season season);

    @Update
    void update(Season season);

    @Delete
    void delete(Season season);

    @Query("SELECT * FROM seasons ORDER BY startDate DESC")
    LiveData<List<Season>> getAllSeasons();

    @Query("SELECT * FROM seasons WHERE id = :id LIMIT 1")
    LiveData<Season> getById(int id);

    @Query("SELECT * FROM seasons WHERE endDate <= (:currentDate + (alertDaysBeforeEnd * 86400000)) AND isActive = 1 ORDER BY endDate ASC")
    LiveData<List<Season>> getSeasonsEndingSoon(long currentDate);
}
