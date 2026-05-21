package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Order;

import java.util.List;

@Dao
public interface OrderDao {

    // Insert a new order and return the new row ID
    @Insert
    long insert(Order order);

    // Update an existing order (used to change status)
    @Update
    void update(Order order);

    // Get all orders for a specific customer (for order history screen)
    @Query("SELECT * FROM orders WHERE customerId = :customerId ORDER BY createdAt DESC")
    LiveData<List<Order>> getOrdersByCustomer(int customerId);

    // Get all orders (for manager's order management screen)
    @Query("SELECT * FROM orders ORDER BY createdAt DESC")
    LiveData<List<Order>> getAllOrders();

    // Get orders with a specific status (e.g., filter by PENDING)
    @Query("SELECT * FROM orders WHERE status = :status ORDER BY createdAt DESC")
    LiveData<List<Order>> getOrdersByStatus(String status);

    // Get total revenue from delivered orders today
    @Query("SELECT COALESCE(SUM(totalPrice), 0) FROM orders WHERE status = 'DELIVERED' AND createdAt >= :startOfDay")
    LiveData<Double> getTodayRevenue(long startOfDay);

    // Count how many orders were placed today
    @Query("SELECT COUNT(*) FROM orders WHERE createdAt >= :startOfDay")
    LiveData<Integer> getTodayOrderCount(long startOfDay);

    // Get a single order by ID
    @Query("SELECT * FROM orders WHERE id = :orderId")
    Order getOrderById(int orderId);
}
