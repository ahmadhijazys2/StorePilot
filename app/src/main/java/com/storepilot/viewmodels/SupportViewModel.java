package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.SupportMessage;
import com.storepilot.repositories.SupportRepository;

import java.util.List;

// ViewModel for the support chat screens
public class SupportViewModel extends AndroidViewModel {

    private final SupportRepository supportRepository;

    public SupportViewModel(@NonNull Application application) {
        super(application);
        supportRepository = new SupportRepository(application);
    }

    // Send a text message to support (or reply as manager)
    public void sendMessage(int senderId, String senderRole, String text, int customerId) {
        supportRepository.sendMessage(senderId, senderRole, text, customerId);
    }

    // Send a message with an image attachment
    public void sendImageMessage(int senderId, String senderRole, String imageUrl, int customerId) {
        supportRepository.sendImageMessage(senderId, senderRole, imageUrl, customerId);
    }

    // Observe messages in a conversation (auto-updates when new messages arrive)
    public LiveData<List<SupportMessage>> getMessages(int customerId) {
        return supportRepository.getMessagesForCustomer(customerId);
    }

    // Get all customer IDs with open conversations (for manager inbox)
    public LiveData<List<Integer>> getConversationIds() {
        return supportRepository.getConversationCustomerIds();
    }

    // Mark all messages in a conversation as read
    public void markRead(int customerId) {
        supportRepository.markAllAsRead(customerId);
    }

    // Get unread message count for a conversation
    public LiveData<Integer> getUnreadCount(int customerId) {
        return supportRepository.getUnreadCount(customerId);
    }
}
