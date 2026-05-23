package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.core.FirestoreManager;
import com.storepilot.db.dao.PurchaseDao;
import com.storepilot.db.entities.Purchase;

import java.util.List;

public class PurchaseRepository {

    private final PurchaseDao purchaseDao;

    public PurchaseRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        purchaseDao = db.purchaseDao();
    }

    public LiveData<List<Purchase>> getAllPurchases() { return purchaseDao.getAllPurchases(); }
    public LiveData<Purchase> getById(int id) { return purchaseDao.getById(id); }
    public LiveData<List<Purchase>> getPurchasesByDateRange(long startDate, long endDate) { return purchaseDao.getPurchasesByDateRange(startDate, endDate); }

    public void insert(Purchase purchase) {
        AppDatabase.dbExecutor.execute(() -> {
            purchaseDao.insert(purchase);
            FirestoreManager.savePurchase(purchase);
        });
    }

    public void update(Purchase purchase) {
        AppDatabase.dbExecutor.execute(() -> {
            purchaseDao.update(purchase);
            FirestoreManager.savePurchase(purchase);
        });
    }

    public void delete(Purchase purchase) {
        AppDatabase.dbExecutor.execute(() -> purchaseDao.delete(purchase));
    }
}
