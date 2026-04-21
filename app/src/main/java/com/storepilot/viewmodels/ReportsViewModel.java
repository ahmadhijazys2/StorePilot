package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Product;
import com.storepilot.repositories.ProductRepository;
import com.storepilot.repositories.SaleRepository;

import java.util.List;

public class ReportsViewModel extends AndroidViewModel {

    private final SaleRepository saleRepository;
    private final ProductRepository productRepository;

    public ReportsViewModel(@NonNull Application application) {
        super(application);
        saleRepository = new SaleRepository(application);
        productRepository = new ProductRepository(application);
    }

    public LiveData<Double> getSalesTotalByWeek(long refDate) {
        return saleRepository.getSalesTotalByWeek(refDate);
    }

    public LiveData<Double> getSalesTotalByMonth(long refDate) {
        return saleRepository.getSalesTotalByMonth(refDate);
    }

    public LiveData<Double> getSalesTotalByYear(long refDate) {
        return saleRepository.getSalesTotalByYear(refDate);
    }

    public LiveData<Double> getSalesTotalByRange(long startDate, long endDate) {
        return saleRepository.getSalesTotalByRange(startDate, endDate);
    }

    public LiveData<List<Product>> getTopSellingProducts(long startDate, long endDate) {
        return productRepository.getTopSellingProducts(startDate, endDate);
    }

    public LiveData<List<Product>> getLowStockProducts(int threshold) {
        return productRepository.getLowStockProducts(threshold);
    }
}
