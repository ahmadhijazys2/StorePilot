package com.storepilot.core;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.storepilot.auth.CryptoUtil;
import com.storepilot.db.dao.CartDao;
import com.storepilot.db.dao.FavoriteDao;
import com.storepilot.db.dao.OrderDao;
import com.storepilot.db.dao.OrderItemDao;
import com.storepilot.db.dao.ProductDao;
import com.storepilot.db.dao.PurchaseDao;
import com.storepilot.db.dao.SaleDao;
import com.storepilot.db.dao.SeasonDao;
import com.storepilot.db.dao.SupportMessageDao;
import com.storepilot.db.dao.TaskDao;
import com.storepilot.db.dao.UserDao;
import com.storepilot.db.dao.VideoMetricDao;
import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Favorite;
import com.storepilot.db.entities.Order;
import com.storepilot.db.entities.OrderItem;
import com.storepilot.db.entities.Product;
import com.storepilot.db.entities.Purchase;
import com.storepilot.db.entities.Sale;
import com.storepilot.db.entities.Season;
import com.storepilot.db.entities.SupportMessage;
import com.storepilot.db.entities.Task;
import com.storepilot.db.entities.User;
import com.storepilot.db.entities.VideoMetric;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// Room database — the single source of truth for all app data
@Database(
    entities = {
        User.class, Product.class, Sale.class, Purchase.class,
        VideoMetric.class, Season.class, Task.class,
        Order.class, OrderItem.class, CartItem.class,
        SupportMessage.class, Favorite.class
    },
    version = 2, // bumped because we added new tables and User columns
    exportSchema = false
)
public abstract class AppDatabase extends RoomDatabase {

    private static volatile AppDatabase INSTANCE;

    // Thread pool for running database queries off the main thread
    public static final ExecutorService dbExecutor = Executors.newFixedThreadPool(4);

    // --- DAO accessors ---
    public abstract UserDao userDao();
    public abstract ProductDao productDao();
    public abstract SaleDao saleDao();
    public abstract PurchaseDao purchaseDao();
    public abstract VideoMetricDao videoMetricDao();
    public abstract SeasonDao seasonDao();
    public abstract TaskDao taskDao();
    public abstract OrderDao orderDao();
    public abstract OrderItemDao orderItemDao();
    public abstract CartDao cartDao();
    public abstract SupportMessageDao supportMessageDao();
    public abstract FavoriteDao favoriteDao();

    // Get the singleton database instance
    public static AppDatabase getInstance(Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                            context.getApplicationContext(),
                            AppDatabase.class,
                            "storepilot.db")
                            // Wipe and rebuild if schema changes (safe for development)
                            .fallbackToDestructiveMigration()
                            .build();
                }
            }
        }
        return INSTANCE;
    }

    // Seed the database with demo data for testing
    public void seedDemoData() {
        dbExecutor.execute(() -> {
            UserDao userDao = userDao();
            ProductDao productDao = productDao();
            SaleDao saleDao = saleDao();
            PurchaseDao purchaseDao = purchaseDao();
            SeasonDao seasonDao = seasonDao();
            TaskDao taskDao = taskDao();
            OrderDao orderDao = orderDao();
            OrderItemDao orderItemDao = orderItemDao();
            SupportMessageDao supportMessageDao = supportMessageDao();

            long now = System.currentTimeMillis();

            // --- Staff Users ---
            String ownerSalt = CryptoUtil.generateSalt();
            User owner = new User("owner", CryptoUtil.hashPassword("ahmad123", ownerSalt), ownerSalt, "OWNER", now);
            long ownerId = userDao.insert(owner);

            String managerSalt = CryptoUtil.generateSalt();
            User manager = new User("manager", CryptoUtil.hashPassword("sss123", managerSalt), managerSalt, "STORE_MANAGER", now);
            long managerId = userDao.insert(manager);

            String empSalt = CryptoUtil.generateSalt();
            User employee = new User("employee", CryptoUtil.hashPassword("aaa123", empSalt), empSalt, "EMPLOYEE", now);
            userDao.insert(employee);

            // --- Demo Customer ---
            String custSalt = CryptoUtil.generateSalt();
            User customer = new User("John Smith", "customer", "customer@demo.com", "+1234567890",
                    CryptoUtil.hashPassword("demo123", custSalt), custSalt, "CUSTOMER", now);
            long custId = userDao.insert(customer);

            // --- Products ---
            long p1 = productDao.insert(new Product("Classic White T-Shirt", "Tops", "M", "White", 50, 29.99, 10.00, "", now));
            long p2 = productDao.insert(new Product("Slim Fit Jeans", "Bottoms", "32", "Blue", 30, 79.99, 35.00, "", now));
            long p3 = productDao.insert(new Product("Floral Summer Dress", "Dresses", "S", "Red", 20, 59.99, 22.00, "", now));
            long p4 = productDao.insert(new Product("Leather Jacket", "Outerwear", "L", "Black", 5, 199.99, 90.00, "", now));
            long p5 = productDao.insert(new Product("Casual Sneakers", "Footwear", "42", "White", 15, 89.99, 40.00, "", now));
            long p6 = productDao.insert(new Product("Summer Hat", "Accessories", "One Size", "Beige", 25, 24.99, 8.00, "", now));
            long p7 = productDao.insert(new Product("Sports Hoodie", "Tops", "L", "Gray", 18, 69.99, 28.00, "", now));
            long p8 = productDao.insert(new Product("Running Shorts", "Bottoms", "M", "Black", 40, 34.99, 12.00, "", now));

            // --- Staff Sales ---
            long weekAgo = now - 7 * 24 * 60 * 60 * 1000L;
            saleDao.insert(new Sale((int) p1, 3, 89.97, now, (int) ownerId, "Walk-in customer"));
            saleDao.insert(new Sale((int) p2, 1, 79.99, weekAgo, (int) managerId, "Online order"));
            saleDao.insert(new Sale((int) p3, 2, 119.98, weekAgo - 86400000, (int) managerId, ""));

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
                    (int) managerId, (int) ownerId, "IN_PROGRESS", "MEDIUM", false, now + 7 * 86400000L, now));

            // --- Demo Customer Orders ---
            long orderId1 = orderDao.insert(new Order((int) custId, 109.98, "DELIVERED", weekAgo, "CREDIT_CARD", "123 Main St, New York"));
            orderItemDao.insert(new OrderItem((int) orderId1, (int) p1, 2, 29.99));
            orderItemDao.insert(new OrderItem((int) orderId1, (int) p6, 2, 24.99));

            long orderId2 = orderDao.insert(new Order((int) custId, 79.99, "PROCESSING", now - 86400000, "PAYPAL", "123 Main St, New York"));
            orderItemDao.insert(new OrderItem((int) orderId2, (int) p2, 1, 79.99));

            long orderId3 = orderDao.insert(new Order((int) custId, 199.99, "PENDING", now - 3600000, "CASH_ON_DELIVERY", "456 Oak Ave, Brooklyn"));
            orderItemDao.insert(new OrderItem((int) orderId3, (int) p4, 1, 199.99));

            // --- Demo Support Chat ---
            supportMessageDao.insert(new SupportMessage((int) custId, "CUSTOMER",
                    "Hi! Do you have this jacket in size M?", null, now - 7200000, (int) custId));
            supportMessageDao.insert(new SupportMessage((int) managerId, "STORE_MANAGER",
                    "Hello! Yes, we have the Leather Jacket in size M. Would you like to place an order?", null, now - 3600000, (int) custId));
            supportMessageDao.insert(new SupportMessage((int) custId, "CUSTOMER",
                    "Yes please! How long does delivery take?", null, now - 1800000, (int) custId));
        });
    }
}
