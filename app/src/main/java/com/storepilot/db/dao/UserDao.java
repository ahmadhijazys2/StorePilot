package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.User;

import java.util.List;

@Dao
public interface UserDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(User user);

    @Update
    void update(User user);

    @Delete
    void delete(User user);

    @Query("SELECT * FROM users WHERE username = :username LIMIT 1")
    User findByUsername(String username);

    @Query("SELECT * FROM users WHERE id = :id LIMIT 1")
    User findById(int id);

    @Query("SELECT * FROM users ORDER BY createdAt ASC")
    LiveData<List<User>> getAllUsers();

    @Query("SELECT COUNT(*) FROM users WHERE role = 'OWNER'")
    int getOwnerCount();

    // Find user by email (used for email-based login)
    @Query("SELECT * FROM users WHERE email = :email LIMIT 1")
    User findByEmail(String email);

    // Count total registered users (for dashboard stats)
    @Query("SELECT COUNT(*) FROM users")
    LiveData<Integer> getTotalUserCount();

    // Synchronous count for setup check on background thread
    @Query("SELECT COUNT(*) FROM users")
    int getUserCountSync();

    // Count only customers (for dashboard stats)
    @Query("SELECT COUNT(*) FROM users WHERE role = 'CUSTOMER'")
    LiveData<Integer> getCustomerCount();
}
