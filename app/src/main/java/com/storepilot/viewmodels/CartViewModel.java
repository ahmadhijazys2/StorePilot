package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.CartItem;
import com.storepilot.repositories.CartRepository;

import java.util.List;

// ViewModel for the shopping cart — survives screen rotations
public class CartViewModel extends AndroidViewModel {

    private final CartRepository cartRepository;

    public CartViewModel(@NonNull Application application) {
        super(application);
        cartRepository = new CartRepository(application);
    }

    // Add a product to cart (or increase quantity)
    public void addToCart(int customerId, int productId) {
        cartRepository.addToCart(customerId, productId);
    }

    // Decrease quantity by 1, or remove if last unit
    public void removeOne(CartItem cartItem) {
        cartRepository.removeOneFromCart(cartItem);
    }

    // Remove the whole item from the cart
    public void removeFromCart(int cartItemId) {
        cartRepository.removeFromCart(cartItemId);
    }

    // Empty the cart completely
    public void clearCart(int customerId) {
        cartRepository.clearCart(customerId);
    }

    // Get live list of cart items for the UI
    public LiveData<List<CartItem>> getCartItems(int customerId) {
        return cartRepository.getCartItems(customerId);
    }

    // Get total item count for the cart badge
    public LiveData<Integer> getCartItemCount(int customerId) {
        return cartRepository.getCartItemCount(customerId);
    }
}
