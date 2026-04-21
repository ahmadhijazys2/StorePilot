package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.ProductDao;
import com.storepilot.db.entities.Product;

import java.util.List;

public class ProductRepository {

    private final ProductDao productDao;

    public ProductRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        productDao = db.productDao();
    }

    public LiveData<List<Product>> getAllProducts() {
        return productDao.getAllProducts();
    }

    public LiveData<Product> getById(int id) {
        return productDao.getById(id);
    }

    public LiveData<List<Product>> getLowStockProducts(int threshold) {
        return productDao.getLowStockProducts(threshold);
    }

    public LiveData<List<Product>> getTopSellingProducts(long startDate, long endDate) {
        return productDao.getTopSellingProducts(startDate, endDate);
    }

    public void insert(Product product) {
        AppDatabase.dbExecutor.execute(() -> productDao.insert(product));
    }

    public void update(Product product) {
        AppDatabase.dbExecutor.execute(() -> productDao.update(product));
    }

    public void delete(Product product) {
        AppDatabase.dbExecutor.execute(() -> productDao.delete(product));
    }
}
