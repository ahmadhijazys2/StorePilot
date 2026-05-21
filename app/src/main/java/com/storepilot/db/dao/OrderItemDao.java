package com.storepilot.db.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;

import com.storepilot.db.entities.OrderItem;

import java.util.List;

@Dao
public interface OrderItemDao {

    // Save one item that belongs to an order
    @Insert
    void insert(OrderItem orderItem);

    // Get all items that belong to a specific order
    @Query("SELECT * FROM order_items WHERE orderId = :orderId")
    List<OrderItem> getItemsForOrder(int orderId);

    // Count total units sold for a product (for best-seller analytics)
    @Query("SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE productId = :productId")
    int getTotalSoldForProduct(int productId);
}
