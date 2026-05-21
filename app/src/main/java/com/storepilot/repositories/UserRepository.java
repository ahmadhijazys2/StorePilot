package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.UserDao;
import com.storepilot.db.entities.User;

import java.util.List;

public class UserRepository {

    private final UserDao userDao;

    public UserRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        userDao = db.userDao();
    }

    public LiveData<List<User>> getAllUsers() {
        return userDao.getAllUsers();
    }

    public void insert(User user) {
        AppDatabase.dbExecutor.execute(() -> userDao.insert(user));
    }

    public void update(User user) {
        AppDatabase.dbExecutor.execute(() -> userDao.update(user));
    }

    public void delete(User user) {
        AppDatabase.dbExecutor.execute(() -> userDao.delete(user));
    }

    public User findByUsername(String username) {
        return userDao.findByUsername(username);
    }

    public int getOwnerCount() {
        return userDao.getOwnerCount();
    }

    // Returns total user count synchronously (for setup check on background thread)
    public int getUserCountSync() {
        return userDao.getUserCountSync();
    }

    // Find user by email address (used for email-based login)
    public User findByEmail(String email) {
        return userDao.findByEmail(email);
    }
}
