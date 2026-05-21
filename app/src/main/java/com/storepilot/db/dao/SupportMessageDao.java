package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.SupportMessage;

import java.util.List;

@Dao
public interface SupportMessageDao {

    // Save a new support message
    @Insert
    void insert(SupportMessage message);

    // Mark messages as read
    @Update
    void update(SupportMessage message);

    // Get all messages for a customer's conversation (sorted oldest first)
    @Query("SELECT * FROM support_messages WHERE customerId = :customerId ORDER BY timestamp ASC")
    LiveData<List<SupportMessage>> getMessagesForCustomer(int customerId);

    // Get distinct customer IDs that have sent messages (for support inbox list)
    @Query("SELECT DISTINCT customerId FROM support_messages ORDER BY timestamp DESC")
    LiveData<List<Integer>> getConversationCustomerIds();

    // Get the latest message from each conversation (for inbox preview)
    @Query("SELECT * FROM support_messages WHERE customerId = :customerId ORDER BY timestamp DESC LIMIT 1")
    SupportMessage getLatestMessage(int customerId);

    // Count unread messages for a customer conversation
    @Query("SELECT COUNT(*) FROM support_messages WHERE customerId = :customerId AND isRead = 0 AND senderRole = 'CUSTOMER'")
    LiveData<Integer> getUnreadCount(int customerId);

    // Mark all messages in a conversation as read
    @Query("UPDATE support_messages SET isRead = 1 WHERE customerId = :customerId")
    void markAllAsRead(int customerId);
}
