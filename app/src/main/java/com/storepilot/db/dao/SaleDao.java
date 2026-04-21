package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Sale;

import java.util.List;

@Dao
public interface SaleDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Sale sale);

    @Update
    void update(Sale sale);

    @Delete
    void delete(Sale sale);

    @Query("SELECT * FROM sales ORDER BY saleDate DESC")
    LiveData<List<Sale>> getAllSales();

    @Query("SELECT * FROM sales WHERE id = :id LIMIT 1")
    LiveData<Sale> getById(int id);

    @Query("SELECT * FROM sales WHERE saleDate BETWEEN :startDate AND :endDate ORDER BY saleDate DESC")
    LiveData<List<Sale>> getSalesByDateRange(long startDate, long endDate);

    @Query("SELECT SUM(totalPrice) FROM sales WHERE saleDate BETWEEN :startDate AND :endDate")
    LiveData<Double> getSalesTotalByRange(long startDate, long endDate);

    @Query("SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y-%W', saleDate/1000, 'unixepoch') = strftime('%Y-%W', :refDate/1000, 'unixepoch')")
    LiveData<Double> getSalesTotalByWeek(long refDate);

    @Query("SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y-%m', saleDate/1000, 'unixepoch') = strftime('%Y-%m', :refDate/1000, 'unixepoch')")
    LiveData<Double> getSalesTotalByMonth(long refDate);

    @Query("SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y', saleDate/1000, 'unixepoch') = strftime('%Y', :refDate/1000, 'unixepoch')")
    LiveData<Double> getSalesTotalByYear(long refDate);

    @Query("SELECT SUM(totalPrice) FROM sales WHERE saleDate >= :startOfDay AND saleDate < :endOfDay")
    LiveData<Double> getTodaySalesTotal(long startOfDay, long endOfDay);
}
