package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.PrimaryKey;

@Entity(tableName = "tasks",
        foreignKeys = {
            @ForeignKey(entity = User.class, parentColumns = "id", childColumns = "assignedTo", onDelete = ForeignKey.SET_NULL),
            @ForeignKey(entity = User.class, parentColumns = "id", childColumns = "createdBy", onDelete = ForeignKey.SET_NULL)
        })
public class Task {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public String title;
    public String description;
    public Integer assignedTo;
    public Integer createdBy;
    public String status; // TODO, IN_PROGRESS, DONE
    public String priority; // LOW, MEDIUM, HIGH
    public boolean isPrivate;
    public long dueDate;
    public long createdAt;

    public Task() {}

    public Task(String title, String description, Integer assignedTo, Integer createdBy,
                String status, String priority, boolean isPrivate, long dueDate, long createdAt) {
        this.title = title;
        this.description = description;
        this.assignedTo = assignedTo;
        this.createdBy = createdBy;
        this.status = status;
        this.priority = priority;
        this.isPrivate = isPrivate;
        this.dueDate = dueDate;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public Integer getAssignedTo() { return assignedTo; }
    public Integer getCreatedBy() { return createdBy; }
    public String getStatus() { return status; }
    public String getPriority() { return priority; }
    public boolean isPrivate() { return isPrivate; }
    public long getDueDate() { return dueDate; }
    public long getCreatedAt() { return createdAt; }
}
