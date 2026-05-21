package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.CartDao;
import com.storepilot.db.entities.CartItem;

import java.util.List;

// Handles all cart operations between ViewModel and the database
public class CartRepository {

    private final CartDao cartDao;

    public CartRepository(Application application) {
        // Get the database and its cart DAO
        AppDatabase db = AppDatabase.getInstance(application);
        cartDao = db.cartDao();
    }

    // Add an item to the cart or increase quantity if already there
    public void addToCart(int customerId, int productId) {
        AppDatabase.dbExecutor.execute(() -> {
            CartItem existing = cartDao.getCartItemByProduct(customerId, productId);
            if (existing != null) {
                // Product already in cart — just increase quantity
                existing.setQuantity(existing.getQuantity() + 1);
                cartDao.update(existing);
            } else {
                // New cart item
                cartDao.insert(new CartItem(customerId, productId, 1));
            }
        });
    }

    // Remove one unit of a product, or delete the item if quantity reaches zero
    public void removeOneFromCart(CartItem cartItem) {
        AppDatabase.dbExecutor.execute(() -> {
            if (cartItem.getQuantity() > 1) {
                cartItem.setQuantity(cartItem.getQuantity() - 1);
                cartDao.update(cartItem);
            } else {
                cartDao.deleteById(cartItem.getId());
            }
        });
    }

    // Completely remove an item from the cart
    public void removeFromCart(int cartItemId) {
        AppDatabase.dbExecutor.execute(() -> cartDao.deleteById(cartItemId));
    }

    // Empty the whole cart (called after checkout)
    public void clearCart(int customerId) {
        AppDatabase.dbExecutor.execute(() -> cartDao.clearCart(customerId));
    }

    // Get live cart items for the UI
    public LiveData<List<CartItem>> getCartItems(int customerId) {
        return cartDao.getCartItems(customerId);
    }

    // Get the cart item count for the badge icon
    public LiveData<Integer> getCartItemCount(int customerId) {
        return cartDao.getCartItemCount(customerId);
    }
}
