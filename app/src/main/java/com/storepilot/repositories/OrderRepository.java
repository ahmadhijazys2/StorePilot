package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.CartDao;
import com.storepilot.db.dao.OrderDao;
import com.storepilot.db.dao.OrderItemDao;
import com.storepilot.db.dao.ProductDao;
import com.storepilot.db.entities.CartItem;
import com.storepilot.db.entities.Order;
import com.storepilot.db.entities.OrderItem;
import com.storepilot.db.entities.Product;

import java.util.List;

// Handles creating and reading orders
public class OrderRepository {

    private final OrderDao orderDao;
    private final OrderItemDao orderItemDao;
    private final CartDao cartDao;
    private final ProductDao productDao;

    public OrderRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        orderDao = db.orderDao();
        orderItemDao = db.orderItemDao();
        cartDao = db.cartDao();
        productDao = db.productDao();
    }

    // Place an order using the items currently in the cart
    public void placeOrder(int customerId, String paymentMethod,
                           String shippingAddress, List<CartItem> cartItems,
                           List<Product> products, Runnable onSuccess) {
        AppDatabase.dbExecutor.execute(() -> {
            // Calculate total price from cart
            double total = 0;
            for (int i = 0; i < cartItems.size(); i++) {
                CartItem ci = cartItems.get(i);
                // Find matching product to get its price
                for (Product p : products) {
                    if (p.getId() == ci.getProductId()) {
                        total += p.getPrice() * ci.getQuantity();
                        break;
                    }
                }
            }

            // Create the order record
            Order order = new Order(customerId, total, "PENDING",
                    System.currentTimeMillis(), paymentMethod, shippingAddress);
            long orderId = orderDao.insert(order);

            // Save each cart item as an order item
            for (CartItem ci : cartItems) {
                for (Product p : products) {
                    if (p.getId() == ci.getProductId()) {
                        orderItemDao.insert(new OrderItem((int) orderId,
                                p.getId(), ci.getQuantity(), p.getPrice()));
                        // Reduce stock quantity
                        p.quantity = Math.max(0, p.quantity - ci.getQuantity());
                        productDao.update(p);
                        break;
                    }
                }
            }

            // Clear the cart after successful order placement
            cartDao.clearCart(customerId);

            // Notify caller on completion
            if (onSuccess != null) onSuccess.run();
        });
    }

    // Update order status (manager action: PENDING → PROCESSING → SHIPPED → DELIVERED)
    public void updateOrderStatus(Order order, String newStatus) {
        AppDatabase.dbExecutor.execute(() -> {
            order.status = newStatus;
            orderDao.update(order);
        });
    }

    // Get customer's order history
    public LiveData<List<Order>> getOrdersByCustomer(int customerId) {
        return orderDao.getOrdersByCustomer(customerId);
    }

    // Get all orders (for manager view)
    public LiveData<List<Order>> getAllOrders() {
        return orderDao.getAllOrders();
    }

    // Get today's total revenue
    public LiveData<Double> getTodayRevenue(long startOfDay) {
        return orderDao.getTodayRevenue(startOfDay);
    }

    // Get today's order count
    public LiveData<Integer> getTodayOrderCount(long startOfDay) {
        return orderDao.getTodayOrderCount(startOfDay);
    }
}
