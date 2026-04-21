package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Purchase;

import java.util.List;

@Dao
public interface PurchaseDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Purchase purchase);

    @Update
    void update(Purchase purchase);

    @Delete
    void delete(Purchase purchase);

    @Query("SELECT * FROM purchases ORDER BY purchaseDate DESC")
    LiveData<List<Purchase>> getAllPurchases();

    @Query("SELECT * FROM purchases WHERE id = :id LIMIT 1")
    LiveData<Purchase> getById(int id);

    @Query("SELECT * FROM purchases WHERE purchaseDate BETWEEN :startDate AND :endDate ORDER BY purchaseDate DESC")
    LiveData<List<Purchase>> getPurchasesByDateRange(long startDate, long endDate);
}
