package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.Index;
import androidx.room.PrimaryKey;

// Represents a user account — could be a customer or a store team member
@Entity(tableName = "users", indices = {
        @Index(value = "username", unique = true),
        @Index(value = "email", unique = true)
})
public class User {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // Display name shown in the app
    public String fullName;

    // Login username
    public String username;

    // Contact email (also used for login)
    public String email;

    // Phone number for contact
    public String phone;

    // Hashed password (never store plain text)
    public String passwordHash;

    // Salt used when hashing the password
    public String salt;

    // Role determines what the user can see: CUSTOMER, OWNER, STORE_MANAGER, SHIFT_MANAGER, EMPLOYEE
    public String role;

    // When the account was created
    public long createdAt;

    public User() {}

    // Constructor for registration (customers and staff)
    public User(String fullName, String username, String email, String phone,
                String passwordHash, String salt, String role, long createdAt) {
        this.fullName = fullName;
        this.username = username;
        this.email = email;
        this.phone = phone;
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.role = role;
        this.createdAt = createdAt;
    }

    // Legacy constructor for seeding existing staff accounts (no email/phone)
    public User(String username, String passwordHash, String salt, String role, long createdAt) {
        this.username = username;
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.role = role;
        this.createdAt = createdAt;
        this.fullName = username;
        this.email = username + "@storepilot.local";
        this.phone = "";
    }

    public int getId() { return id; }
    public String getFullName() { return fullName != null ? fullName : username; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
    public String getPasswordHash() { return passwordHash; }
    public String getSalt() { return salt; }
    public String getRole() { return role; }
    public long getCreatedAt() { return createdAt; }
}
