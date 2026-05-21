package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

// A single item in the customer's shopping cart
@Entity(tableName = "cart_items")
public class CartItem {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // The customer who added this item
    public int customerId;

    // Which product was added
    public int productId;

    // How many of this product the customer wants
    public int quantity;

    public CartItem() {}

    public CartItem(int customerId, int productId, int quantity) {
        this.customerId = customerId;
        this.productId = productId;
        this.quantity = quantity;
    }

    public int getId() { return id; }
    public int getCustomerId() { return customerId; }
    public int getProductId() { return productId; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
}
