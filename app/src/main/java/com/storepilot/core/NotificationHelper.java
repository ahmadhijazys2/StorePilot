package com.storepilot.core;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.storepilot.MainActivity;
import com.storepilot.R;

public class NotificationHelper {

    public static final String CHANNEL_ID = "storepilot_alerts";
    private static final String CHANNEL_NAME = "StorePilot Alerts";
    private static final int LOW_STOCK_NOTIF_ID = 1001;

    /** Call once when the app starts to register the notification channel (required on Android 8+) */
    public static void createChannel(Context context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID, CHANNEL_NAME, NotificationManager.IMPORTANCE_DEFAULT);
            channel.setDescription("Low stock and store alerts");
            NotificationManager manager = context.getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }
    }

    /** Sends a notification warning the owner about low-stock products */
    public static void sendLowStockNotification(Context context, int count) {
        Intent intent = new Intent(context, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);

        PendingIntent pendingIntent = PendingIntent.getActivity(
                context, 0, intent,
                PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle("Low Stock Alert")
                .setContentText(count + " product(s) are running low. Tap to review.")
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText(count + " product(s) have stock at or below 5 units. Open StorePilot to restock."))
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);

        NotificationManagerCompat.from(context).notify(LOW_STOCK_NOTIF_ID, builder.build());
    }
}
