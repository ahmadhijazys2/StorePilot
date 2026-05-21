package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;

import com.storepilot.db.entities.Favorite;

import java.util.List;

@Dao
public interface FavoriteDao {

    // Add a product to favorites
    @Insert
    void insert(Favorite favorite);

    // Remove a product from favorites by ID
    @Query("DELETE FROM favorites WHERE id = :favoriteId")
    void deleteById(int favoriteId);

    // Remove a specific product from a customer's favorites
    @Query("DELETE FROM favorites WHERE customerId = :customerId AND productId = :productId")
    void deleteByProduct(int customerId, int productId);

    // Get all favorites for a customer
    @Query("SELECT * FROM favorites WHERE customerId = :customerId ORDER BY addedAt DESC")
    LiveData<List<Favorite>> getFavoritesByCustomer(int customerId);

    // Check if a product is already favorited by a customer
    @Query("SELECT * FROM favorites WHERE customerId = :customerId AND productId = :productId LIMIT 1")
    Favorite getFavorite(int customerId, int productId);
}
