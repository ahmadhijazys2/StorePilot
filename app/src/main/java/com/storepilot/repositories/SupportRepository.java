package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.SupportMessageDao;
import com.storepilot.db.entities.SupportMessage;

import java.util.List;

// Handles support chat messages between customers and the store team
public class SupportRepository {

    private final SupportMessageDao supportMessageDao;

    public SupportRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        supportMessageDao = db.supportMessageDao();
    }

    // Send a text message in the support chat
    public void sendMessage(int senderId, String senderRole, String text, int customerId) {
        AppDatabase.dbExecutor.execute(() -> {
            SupportMessage msg = new SupportMessage(senderId, senderRole, text, null,
                    System.currentTimeMillis(), customerId);
            supportMessageDao.insert(msg);
        });
    }

    // Send a message with an attached image
    public void sendImageMessage(int senderId, String senderRole, String imageUrl, int customerId) {
        AppDatabase.dbExecutor.execute(() -> {
            SupportMessage msg = new SupportMessage(senderId, senderRole, "", imageUrl,
                    System.currentTimeMillis(), customerId);
            supportMessageDao.insert(msg);
        });
    }

    // Get all messages in a customer's conversation (live updates)
    public LiveData<List<SupportMessage>> getMessagesForCustomer(int customerId) {
        return supportMessageDao.getMessagesForCustomer(customerId);
    }

    // Get list of customer IDs who have open conversations (for inbox)
    public LiveData<List<Integer>> getConversationCustomerIds() {
        return supportMessageDao.getConversationCustomerIds();
    }

    // Mark all messages in a conversation as read
    public void markAllAsRead(int customerId) {
        AppDatabase.dbExecutor.execute(() -> supportMessageDao.markAllAsRead(customerId));
    }

    // Get count of unread messages
    public LiveData<Integer> getUnreadCount(int customerId) {
        return supportMessageDao.getUnreadCount(customerId);
    }
}
