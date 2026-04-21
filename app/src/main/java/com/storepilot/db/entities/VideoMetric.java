package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.PrimaryKey;

@Entity(tableName = "video_metrics",
        foreignKeys = {
            @ForeignKey(entity = User.class, parentColumns = "id", childColumns = "recordedBy", onDelete = ForeignKey.SET_NULL)
        })
public class VideoMetric {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public String title;
    public String platform;
    public long views;
    public long likes;
    public long shares;
    public long comments;
    public long videoDate;
    public Integer recordedBy;

    public VideoMetric() {}

    public VideoMetric(String title, String platform, long views, long likes, long shares,
                       long comments, long videoDate, Integer recordedBy) {
        this.title = title;
        this.platform = platform;
        this.views = views;
        this.likes = likes;
        this.shares = shares;
        this.comments = comments;
        this.videoDate = videoDate;
        this.recordedBy = recordedBy;
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getPlatform() { return platform; }
    public long getViews() { return views; }
    public long getLikes() { return likes; }
    public long getShares() { return shares; }
    public long getComments() { return comments; }
    public long getVideoDate() { return videoDate; }
    public Integer getRecordedBy() { return recordedBy; }
}
