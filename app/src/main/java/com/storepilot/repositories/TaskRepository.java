package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.core.FirestoreManager;
import com.storepilot.db.dao.TaskDao;
import com.storepilot.db.entities.Task;

import java.util.List;

public class TaskRepository {

    private final TaskDao taskDao;

    public TaskRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        taskDao = db.taskDao();
    }

    public LiveData<List<Task>> getAllTasks() { return taskDao.getAllTasks(); }
    public LiveData<Task> getById(int id) { return taskDao.getById(id); }
    public LiveData<List<Task>> getTasksByUser(int userId) { return taskDao.getTasksByUser(userId); }
    public LiveData<List<Task>> getTasksByStatus(String status) { return taskDao.getTasksByStatus(status); }
    public LiveData<List<Task>> getTeamTasks() { return taskDao.getTeamTasks(); }
    public LiveData<List<Task>> getPrivateTasks(int userId) { return taskDao.getPrivateTasks(userId); }
    public LiveData<Integer> getPendingTaskCount(int userId) { return taskDao.getPendingTaskCount(userId); }

    public void insert(Task task) {
        AppDatabase.dbExecutor.execute(() -> {
            long newId = taskDao.insert(task);
            task.id = (int) newId;
            FirestoreManager.saveTask(task);
        });
    }

    public void update(Task task) {
        AppDatabase.dbExecutor.execute(() -> {
            taskDao.update(task);
            FirestoreManager.saveTask(task);
        });
    }

    public void delete(Task task) {
        AppDatabase.dbExecutor.execute(() -> {
            taskDao.delete(task);
            FirestoreManager.deleteTask(task.id);
        });
    }
}
