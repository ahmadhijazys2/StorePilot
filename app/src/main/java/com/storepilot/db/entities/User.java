package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "users", indices = {@Index(value = "username", unique = true)})
public class User {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public String username;
    public String passwordHash;
    public String salt;
    public String role; // OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE
    public long createdAt;

    public User() {}

    public User(String username, String passwordHash, String salt, String role, long createdAt) {
        this.username = username;
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.role = role;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public String getUsername() { return username; }
    public String getPasswordHash() { return passwordHash; }
    public String getSalt() { return salt; }
    public String getRole() { return role; }
    public long getCreatedAt() { return createdAt; }
}
