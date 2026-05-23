package com.storepilot.core;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

import com.google.firebase.firestore.FirebaseFirestore;

public class LowStockReceiver extends BroadcastReceiver {

    public static final int LOW_STOCK_THRESHOLD = 5;

    @Override
    public void onReceive(Context context, Intent intent) {
        checkNow(context, false);
    }

    /**
     * Queries Firestore for products at or below LOW_STOCK_THRESHOLD and fires a notification.
     *
     * @param testMode if true, always fires a notification even when nothing is low
     *                 so you can verify the channel works during development
     */
    public static void checkNow(Context context, boolean testMode) {
        FirebaseFirestore.getInstance()
                .collection("products")
                .whereLessThanOrEqualTo("quantity", LOW_STOCK_THRESHOLD)
                .get()
                .addOnSuccessListener(snapshots -> {
                    int count = snapshots != null ? snapshots.size() : 0;
                    if (count > 0) {
                        NotificationHelper.sendLowStockNotification(context, count);
                    } else if (testMode) {
                        // No real low-stock items — send a demo notification so you can
                        // confirm the channel and permission are working
                        NotificationHelper.sendLowStockNotification(context, 1);
                        // Toast runs only in test mode (main thread not guaranteed here,
                        // but checkNow is called from the UI in test mode)
                        Toast.makeText(context,
                                "No real low-stock items — demo notification sent",
                                Toast.LENGTH_LONG).show();
                    }
                })
                .addOnFailureListener(e -> {
                    if (testMode) {
                        Toast.makeText(context,
                                "Firestore error: " + e.getMessage(),
                                Toast.LENGTH_LONG).show();
                    }
                });
    }
}
