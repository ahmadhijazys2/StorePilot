package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "seasons")
public class Season {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public String name;
    public long startDate;
    public long endDate;
    public int alertDaysBeforeEnd = 30;
    public boolean isActive;
    public String notes;

    public Season() {}

    public Season(String name, long startDate, long endDate, int alertDaysBeforeEnd,
                  boolean isActive, String notes) {
        this.name = name;
        this.startDate = startDate;
        this.endDate = endDate;
        this.alertDaysBeforeEnd = alertDaysBeforeEnd;
        this.isActive = isActive;
        this.notes = notes;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public long getStartDate() { return startDate; }
    public long getEndDate() { return endDate; }
    public int getAlertDaysBeforeEnd() { return alertDaysBeforeEnd; }
    public boolean isActive() { return isActive; }
    public String getNotes() { return notes; }
}
