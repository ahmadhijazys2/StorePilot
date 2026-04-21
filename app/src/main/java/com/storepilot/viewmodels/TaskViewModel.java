package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Task;
import com.storepilot.repositories.TaskRepository;

import java.util.List;

public class TaskViewModel extends AndroidViewModel {

    private final TaskRepository repository;

    public TaskViewModel(@NonNull Application application) {
        super(application);
        repository = new TaskRepository(application);
    }

    public LiveData<List<Task>> getAllTasks() {
        return repository.getAllTasks();
    }

    public LiveData<Task> getById(int id) {
        return repository.getById(id);
    }

    public LiveData<List<Task>> getTasksByUser(int userId) {
        return repository.getTasksByUser(userId);
    }

    public LiveData<List<Task>> getTasksByStatus(String status) {
        return repository.getTasksByStatus(status);
    }

    public LiveData<List<Task>> getTeamTasks() {
        return repository.getTeamTasks();
    }

    public LiveData<List<Task>> getPrivateTasks(int userId) {
        return repository.getPrivateTasks(userId);
    }

    public LiveData<Integer> getPendingTaskCount(int userId) {
        return repository.getPendingTaskCount(userId);
    }

    public void insert(Task task) {
        repository.insert(task);
    }

    public void update(Task task) {
        repository.update(task);
    }

    public void delete(Task task) {
        repository.delete(task);
    }
}
