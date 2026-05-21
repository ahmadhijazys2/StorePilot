package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

// One product line inside an order (e.g., 2x T-Shirt)
@Entity(tableName = "order_items")
public class OrderItem {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // Which order this item belongs to
    public int orderId;

    // Which product was ordered
    public int productId;

    // How many units of this product
    public int quantity;

    // Price per unit at time of purchase (snapshot)
    public double unitPrice;

    public OrderItem() {}

    public OrderItem(int orderId, int productId, int quantity, double unitPrice) {
        this.orderId = orderId;
        this.productId = productId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public int getId() { return id; }
    public int getOrderId() { return orderId; }
    public int getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public double getUnitPrice() { return unitPrice; }
}
