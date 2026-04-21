package com.storepilot.core;

import android.content.Context;

import androidx.annotation.NonNull;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.sqlite.db.SupportSQLiteDatabase;

import com.storepilot.auth.CryptoUtil;
import com.storepilot.db.dao.ProductDao;
import com.storepilot.db.dao.PurchaseDao;
import com.storepilot.db.dao.SaleDao;
import com.storepilot.db.dao.SeasonDao;
import com.storepilot.db.dao.TaskDao;
import com.storepilot.db.dao.UserDao;
import com.storepilot.db.dao.VideoMetricDao;
import com.storepilot.db.entities.Product;
import com.storepilot.db.entities.Purchase;
import com.storepilot.db.entities.Sale;
import com.storepilot.db.entities.Season;
import com.storepilot.db.entities.Task;
import com.storepilot.db.entities.User;
import com.storepilot.db.entities.VideoMetric;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Database(
    entities = {User.class, Product.class, Sale.class, Purchase.class,
                VideoMetric.class, Season.class, Task.class},
    version = 1,
    exportSchema = false
)
public abstract class AppDatabase extends RoomDatabase {

    private static volatile AppDatabase INSTANCE;
    public static final ExecutorService dbExecutor = Executors.newFixedThreadPool(4);

    public abstract UserDao userDao();
    public abstract ProductDao productDao();
    public abstract SaleDao saleDao();
    public abstract PurchaseDao purchaseDao();
    public abstract VideoMetricDao videoMetricDao();
    public abstract SeasonDao seasonDao();
    public abstract TaskDao taskDao();

    public static AppDatabase getInstance(Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                            context.getApplicationContext(),
                            AppDatabase.class,
                            "storepilot.db")
                            .fallbackToDestructiveMigration()
                            .build();
                }
            }
        }
        return INSTANCE;
    }

    public void seedDemoData() {
        dbExecutor.execute(() -> {
            UserDao userDao = userDao();
            ProductDao productDao = productDao();
            SaleDao saleDao = saleDao();
            PurchaseDao purchaseDao = purchaseDao();
            SeasonDao seasonDao = seasonDao();
            TaskDao taskDao = taskDao();

            long now = System.currentTimeMillis();

            // --- Users ---
            String ownerSalt = CryptoUtil.generateSalt();
            User owner = new User("owner", CryptoUtil.hashPassword("ahmad123", ownerSalt), ownerSalt, "OWNER", now);
            long ownerId = userDao.insert(owner);

            String managerSalt = CryptoUtil.generateSalt();
            User manager = new User("manager", CryptoUtil.hashPassword("sss123", managerSalt), managerSalt, "STORE_MANAGER", now);
            long managerId = userDao.insert(manager);

            String empSalt = CryptoUtil.generateSalt();
            User employee = new User("employee", CryptoUtil.hashPassword("aaa123", empSalt), empSalt, "EMPLOYEE", now);
            long employeeId = userDao.insert(employee);

            // --- Products ---
            long p1 = productDao.insert(new Product("Classic White T-Shirt", "Tops", "M", "White", 50, 29.99, 10.00, "", now));
            long p2 = productDao.insert(new Product("Slim Fit Jeans", "Bottoms", "32", "Blue", 30, 79.99, 35.00, "", now));
            long p3 = productDao.insert(new Product("Floral Summer Dress", "Dresses", "S", "Red", 20, 59.99, 22.00, "", now));
            long p4 = productDao.insert(new Product("Leather Jacket", "Outerwear", "L", "Black", 5, 199.99, 90.00, "", now));
            long p5 = productDao.insert(new Product("Casual Sneakers", "Footwear", "42", "White", 15, 89.99, 40.00, "", now));

            // --- Sales ---
            long weekAgo = now - 7 * 24 * 60 * 60 * 1000L;
            saleDao.insert(new Sale((int) p1, 3, 89.97, now, (int) ownerId, "Walk-in customer"));
            saleDao.insert(new Sale((int) p2, 1, 79.99, weekAgo, (int) managerId, "Online order"));
            saleDao.insert(new Sale((int) p3, 2, 119.98, weekAgo - 86400000, (int) employeeId, ""));

            // --- Purchases ---
            purchaseDao.insert(new Purchase((int) p1, 100, 1000.00, weekAgo, (int) ownerId, "Supplier A", "Restock"));
            purchaseDao.insert(new Purchase((int) p2, 50, 1750.00, now - 14 * 86400000L, (int) managerId, "Supplier B", "Initial stock"));

            // --- Seasons ---
            long monthMs = 30L * 24 * 60 * 60 * 1000;
            seasonDao.insert(new Season("Summer 2024", now - monthMs, now + monthMs, 30, true, "Current season"));
            seasonDao.insert(new Season("Fall 2024", now + monthMs, now + 4 * monthMs, 30, false, "Upcoming season"));

            // --- Tasks ---
            taskDao.insert(new Task("Restock low inventory", "Check and reorder products below 10 units",
                    (int) managerId, (int) ownerId, "TODO", "HIGH", false, now + 3 * 86400000L, now));
            taskDao.insert(new Task("Update product photos", "Take new photos for summer collection",
                    (int) employeeId, (int) managerId, "IN_PROGRESS", "MEDIUM", false, now + 7 * 86400000L, now));
            taskDao.insert(new Task("Monthly sales report", "Prepare report for owner review",
                    (int) managerId, (int) ownerId, "TODO", "HIGH", false, now + 5 * 86400000L, now));
        });
    }
}
