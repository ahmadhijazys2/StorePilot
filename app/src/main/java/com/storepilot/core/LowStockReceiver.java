package com.storepilot.core;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * BroadcastReceiver triggered by AlarmManager every hour.
 * Checks for low-stock products and fires a notification if any are found.
 */
public class LowStockReceiver extends BroadcastReceiver {

    private static final int LOW_STOCK_THRESHOLD = 5;

    @Override
    public void onReceive(Context context, Intent intent) {
        AppDatabase.dbExecutor.execute(() -> {
            int count = AppDatabase.getInstance(context)
                    .productDao()
                    .getLowStockCountSync(LOW_STOCK_THRESHOLD);
            if (count > 0) {
                NotificationHelper.sendLowStockNotification(context, count);
            }
        });
    }
}
