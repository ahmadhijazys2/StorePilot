package com.storepilot.db.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

// Tracks which products a customer has saved to their wishlist/favorites
@Entity(tableName = "favorites")
public class Favorite {

    @PrimaryKey(autoGenerate = true)
    public int id;

    // The customer who favorited this product
    public int customerId;

    // The product they liked
    public int productId;

    // When they added it to favorites
    public long addedAt;

    public Favorite() {}

    public Favorite(int customerId, int productId, long addedAt) {
        this.customerId = customerId;
        this.productId = productId;
        this.addedAt = addedAt;
    }

    public int getId() { return id; }
    public int getCustomerId() { return customerId; }
    public int getProductId() { return productId; }
    public long getAddedAt() { return addedAt; }
}
