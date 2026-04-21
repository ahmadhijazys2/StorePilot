package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Task;

import java.util.List;

@Dao
public interface TaskDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Task task);

    @Update
    void update(Task task);

    @Delete
    void delete(Task task);

    @Query("SELECT * FROM tasks ORDER BY createdAt DESC")
    LiveData<List<Task>> getAllTasks();

    @Query("SELECT * FROM tasks WHERE id = :id LIMIT 1")
    LiveData<Task> getById(int id);

    @Query("SELECT * FROM tasks WHERE assignedTo = :userId ORDER BY createdAt DESC")
    LiveData<List<Task>> getTasksByUser(int userId);

    @Query("SELECT * FROM tasks WHERE status = :status ORDER BY createdAt DESC")
    LiveData<List<Task>> getTasksByStatus(String status);

    @Query("SELECT * FROM tasks WHERE isPrivate = 0 ORDER BY createdAt DESC")
    LiveData<List<Task>> getTeamTasks();

    @Query("SELECT * FROM tasks WHERE isPrivate = 1 AND createdBy = :userId ORDER BY createdAt DESC")
    LiveData<List<Task>> getPrivateTasks(int userId);

    @Query("SELECT COUNT(*) FROM tasks WHERE assignedTo = :userId AND status != 'DONE'")
    LiveData<Integer> getPendingTaskCount(int userId);
}
