package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.core.FirestoreManager;
import com.storepilot.db.dao.CartDao;
import com.storepilot.db.dao.OrderDao;
import com.storepilot.db.dao.OrderItemDao;
import com.storepilot.db.dao.ProductDao;
import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Order;
import com.storepilot.db.entities.OrderItem;
import com.storepilot.db.entities.Product;

import java.util.List;

public class OrderRepository {

    private final OrderDao orderDao;
    private final OrderItemDao orderItemDao;
    private final CartDao cartDao;
    private final ProductDao productDao;

    public OrderRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        orderDao      = db.orderDao();
        orderItemDao  = db.orderItemDao();
        cartDao       = db.cartDao();
        productDao    = db.productDao();
    }

    public void placeOrder(int customerId, String paymentMethod,
                           String shippingAddress, List<CartItem> cartItems,
                           List<Product> products, Runnable onSuccess) {
        AppDatabase.dbExecutor.execute(() -> {
            double total = 0;
            for (CartItem ci : cartItems) {
                for (Product p : products) {
                    if (p.getId() == ci.getProductId()) {
                        total += p.getPrice() * ci.getQuantity();
                        break;
                    }
                }
            }

            Order order = new Order(customerId, total, "PENDING",
                    System.currentTimeMillis(), paymentMethod, shippingAddress);
            long orderId = orderDao.insert(order);
            order.id = (int) orderId;

            // Sync order to Firestore
            FirestoreManager.saveOrder(order);

            for (CartItem ci : cartItems) {
                for (Product p : products) {
                    if (p.getId() == ci.getProductId()) {
                        orderItemDao.insert(new OrderItem((int) orderId,
                                p.getId(), ci.getQuantity(), p.getPrice()));
                        p.quantity = Math.max(0, p.quantity - ci.getQuantity());
                        productDao.update(p);
                        // Sync updated product stock to Firestore
                        FirestoreManager.saveProduct(p);
                        break;
                    }
                }
            }

            cartDao.clearCart(customerId);
            if (onSuccess != null) onSuccess.run();
        });
    }

    public void updateOrderStatus(Order order, String newStatus) {
        AppDatabase.dbExecutor.execute(() -> {
            order.status = newStatus;
            orderDao.update(order);
            FirestoreManager.updateOrderStatus(order.id, newStatus);
        });
    }

    public LiveData<List<Order>> getOrdersByCustomer(int customerId) { return orderDao.getOrdersByCustomer(customerId); }
    public LiveData<List<Order>> getAllOrders() { return orderDao.getAllOrders(); }
    public LiveData<Double> getTodayRevenue(long startOfDay) { return orderDao.getTodayRevenue(startOfDay); }
    public LiveData<Integer> getTodayOrderCount(long startOfDay) { return orderDao.getTodayOrderCount(startOfDay); }
}
