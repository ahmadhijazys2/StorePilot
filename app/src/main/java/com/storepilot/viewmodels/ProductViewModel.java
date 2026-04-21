package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Product;
import com.storepilot.repositories.ProductRepository;

import java.util.List;

public class ProductViewModel extends AndroidViewModel {

    private final ProductRepository repository;

    public ProductViewModel(@NonNull Application application) {
        super(application);
        repository = new ProductRepository(application);
    }

    public LiveData<List<Product>> getAllProducts() {
        return repository.getAllProducts();
    }

    public LiveData<Product> getById(int id) {
        return repository.getById(id);
    }

    public LiveData<List<Product>> getLowStockProducts(int threshold) {
        return repository.getLowStockProducts(threshold);
    }

    public LiveData<List<Product>> getTopSellingProducts(long startDate, long endDate) {
        return repository.getTopSellingProducts(startDate, endDate);
    }

    public void insert(Product product) {
        repository.insert(product);
    }

    public void update(Product product) {
        repository.update(product);
    }

    public void delete(Product product) {
        repository.delete(product);
    }
}
