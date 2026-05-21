package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.CartItem;

import java.util.List;

@Dao
public interface CartDao {

    // Add a new product to the cart
    @Insert
    void insert(CartItem cartItem);

    // Update quantity of an existing cart item
    @Update
    void update(CartItem cartItem);

    // Get all cart items for a specific customer (live, updates UI automatically)
    @Query("SELECT * FROM cart_items WHERE customerId = :customerId")
    LiveData<List<CartItem>> getCartItems(int customerId);

    // Check if a product is already in the cart
    @Query("SELECT * FROM cart_items WHERE customerId = :customerId AND productId = :productId LIMIT 1")
    CartItem getCartItemByProduct(int customerId, int productId);

    // Remove a specific item from the cart
    @Query("DELETE FROM cart_items WHERE id = :cartItemId")
    void deleteById(int cartItemId);

    // Clear all items from cart after checkout
    @Query("DELETE FROM cart_items WHERE customerId = :customerId")
    void clearCart(int customerId);

    // Count how many items are in the cart (for badge on cart icon)
    @Query("SELECT COUNT(*) FROM cart_items WHERE customerId = :customerId")
    LiveData<Integer> getCartItemCount(int customerId);
}
