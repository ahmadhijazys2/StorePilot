package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Favorite;
import com.storepilot.repositories.FavoritesRepository;

import java.util.List;

// ViewModel for the customer's wishlist/favorites feature
public class FavoritesViewModel extends AndroidViewModel {

    private final FavoritesRepository favoritesRepository;

    public FavoritesViewModel(@NonNull Application application) {
        super(application);
        favoritesRepository = new FavoritesRepository(application);
    }

    // Add or remove a product from favorites
    public void toggleFavorite(int customerId, int productId) {
        favoritesRepository.toggleFavorite(customerId, productId);
    }

    // Get live list of favorites for the wishlist screen
    public LiveData<List<Favorite>> getFavorites(int customerId) {
        return favoritesRepository.getFavoritesByCustomer(customerId);
    }
}
