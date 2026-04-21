package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Purchase;
import com.storepilot.repositories.PurchaseRepository;

import java.util.List;

public class PurchaseViewModel extends AndroidViewModel {

    private final PurchaseRepository repository;

    public PurchaseViewModel(@NonNull Application application) {
        super(application);
        repository = new PurchaseRepository(application);
    }

    public LiveData<List<Purchase>> getAllPurchases() {
        return repository.getAllPurchases();
    }

    public LiveData<Purchase> getById(int id) {
        return repository.getById(id);
    }

    public LiveData<List<Purchase>> getPurchasesByDateRange(long startDate, long endDate) {
        return repository.getPurchasesByDateRange(startDate, endDate);
    }

    public void insert(Purchase purchase) {
        repository.insert(purchase);
    }

    public void update(Purchase purchase) {
        repository.update(purchase);
    }

    public void delete(Purchase purchase) {
        repository.delete(purchase);
    }
}
