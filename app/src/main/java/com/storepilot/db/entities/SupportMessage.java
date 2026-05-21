package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

// A single message in the support chat between customer and store team
@Entity(tableName = "support_messages")
public class SupportMessage {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // ID of the user who sent the message
    public int senderId;

    // Role of the sender: CUSTOMER, MANAGER, OWNER, etc.
    public String senderRole;

    // The chat message text
    public String messageText;

    // Optional image attached to the message
    public String imageUrl;

    // When the message was sent
    public long timestamp;

    // Groups messages by customer conversation (customer's user ID)
    public int customerId;

    // Whether the recipient has read this message
    public boolean isRead;

    public SupportMessage() {}

    public SupportMessage(int senderId, String senderRole, String messageText,
                          String imageUrl, long timestamp, int customerId) {
        this.senderId = senderId;
        this.senderRole = senderRole;
        this.messageText = messageText;
        this.imageUrl = imageUrl;
        this.timestamp = timestamp;
        this.customerId = customerId;
        this.isRead = false;
    }

    public int getId() { return id; }
    public int getSenderId() { return senderId; }
    public String getSenderRole() { return senderRole; }
    public String getMessageText() { return messageText; }
    public String getImageUrl() { return imageUrl; }
    public long getTimestamp() { return timestamp; }
    public int getCustomerId() { return customerId; }
    public boolean isRead() { return isRead; }
    public void setRead(boolean read) { isRead = read; }
}
