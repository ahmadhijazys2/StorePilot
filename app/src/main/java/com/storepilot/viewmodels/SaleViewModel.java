package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Sale;
import com.storepilot.repositories.SaleRepository;

import java.util.List;

public class SaleViewModel extends AndroidViewModel {

    private final SaleRepository repository;

    public SaleViewModel(@NonNull Application application) {
        super(application);
        repository = new SaleRepository(application);
    }

    public LiveData<List<Sale>> getAllSales() {
        return repository.getAllSales();
    }

    public LiveData<Sale> getById(int id) {
        return repository.getById(id);
    }

    public LiveData<List<Sale>> getSalesByDateRange(long startDate, long endDate) {
        return repository.getSalesByDateRange(startDate, endDate);
    }

    public LiveData<Double> getSalesTotalByRange(long startDate, long endDate) {
        return repository.getSalesTotalByRange(startDate, endDate);
    }

    public LiveData<Double> getSalesTotalByWeek(long refDate) {
        return repository.getSalesTotalByWeek(refDate);
    }

    public LiveData<Double> getSalesTotalByMonth(long refDate) {
        return repository.getSalesTotalByMonth(refDate);
    }

    public LiveData<Double> getSalesTotalByYear(long refDate) {
        return repository.getSalesTotalByYear(refDate);
    }

    public LiveData<Double> getTodaySalesTotal(long startOfDay, long endOfDay) {
        return repository.getTodaySalesTotal(startOfDay, endOfDay);
    }

    public void insert(Sale sale) {
        repository.insert(sale);
    }

    public void update(Sale sale) {
        repository.update(sale);
    }

    public void delete(Sale sale) {
        repository.delete(sale);
    }
}
