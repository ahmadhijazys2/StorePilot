package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

// Represents a customer order placed in the store
@Entity(tableName = "orders")
public class Order {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // The customer who placed this order
    public int customerId;

    // Total amount for the entire order
    public double totalPrice;

    // Current status: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED
    public String status;

    // When the order was placed
    public long createdAt;

    // How the customer wants to pay
    public String paymentMethod; // CASH_ON_DELIVERY, CREDIT_CARD, PAYPAL

    // Delivery address entered by customer
    public String shippingAddress;

    public Order() {}

    public Order(int customerId, double totalPrice, String status,
                 long createdAt, String paymentMethod, String shippingAddress) {
        this.customerId = customerId;
        this.totalPrice = totalPrice;
        this.status = status;
        this.createdAt = createdAt;
        this.paymentMethod = paymentMethod;
        this.shippingAddress = shippingAddress;
    }

    public int getId() { return id; }
    public int getCustomerId() { return customerId; }
    public double getTotalPrice() { return totalPrice; }
    public String getStatus() { return status; }
    public long getCreatedAt() { return createdAt; }
    public String getPaymentMethod() { return paymentMethod; }
    public String getShippingAddress() { return shippingAddress; }
}
