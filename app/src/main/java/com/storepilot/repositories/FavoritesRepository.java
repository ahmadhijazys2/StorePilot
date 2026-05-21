package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.FavoriteDao;
import com.storepilot.db.entities.Favorite;

import java.util.List;

// Handles customer wishlist/favorites
public class FavoritesRepository {

    private final FavoriteDao favoriteDao;

    public FavoritesRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        favoriteDao = db.favoriteDao();
    }

    // Toggle favorite: add if not there, remove if already favorited
    public void toggleFavorite(int customerId, int productId) {
        AppDatabase.dbExecutor.execute(() -> {
            Favorite existing = favoriteDao.getFavorite(customerId, productId);
            if (existing != null) {
                // Already favorited — remove it
                favoriteDao.deleteByProduct(customerId, productId);
            } else {
                // Not favorited yet — add it
                favoriteDao.insert(new Favorite(customerId, productId, System.currentTimeMillis()));
            }
        });
    }

    // Check if a product is in the customer's favorites
    public boolean isFavorite(int customerId, int productId) {
        return favoriteDao.getFavorite(customerId, productId) != null;
    }

    // Get all favorites for the wishlist screen (live updates)
    public LiveData<List<Favorite>> getFavoritesByCustomer(int customerId) {
        return favoriteDao.getFavoritesByCustomer(customerId);
    }
}
