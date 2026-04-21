package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.SaleDao;
import com.storepilot.db.entities.Sale;

import java.util.List;

public class SaleRepository {

    private final SaleDao saleDao;

    public SaleRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        saleDao = db.saleDao();
    }

    public LiveData<List<Sale>> getAllSales() {
        return saleDao.getAllSales();
    }

    public LiveData<Sale> getById(int id) {
        return saleDao.getById(id);
    }

    public LiveData<List<Sale>> getSalesByDateRange(long startDate, long endDate) {
        return saleDao.getSalesByDateRange(startDate, endDate);
    }

    public LiveData<Double> getSalesTotalByRange(long startDate, long endDate) {
        return saleDao.getSalesTotalByRange(startDate, endDate);
    }

    public LiveData<Double> getSalesTotalByWeek(long refDate) {
        return saleDao.getSalesTotalByWeek(refDate);
    }

    public LiveData<Double> getSalesTotalByMonth(long refDate) {
        return saleDao.getSalesTotalByMonth(refDate);
    }

    public LiveData<Double> getSalesTotalByYear(long refDate) {
        return saleDao.getSalesTotalByYear(refDate);
    }

    public LiveData<Double> getTodaySalesTotal(long startOfDay, long endOfDay) {
        return saleDao.getTodaySalesTotal(startOfDay, endOfDay);
    }

    public void insert(Sale sale) {
        AppDatabase.dbExecutor.execute(() -> saleDao.insert(sale));
    }

    public void update(Sale sale) {
        AppDatabase.dbExecutor.execute(() -> saleDao.update(sale));
    }

    public void delete(Sale sale) {
        AppDatabase.dbExecutor.execute(() -> saleDao.delete(sale));
    }
}
