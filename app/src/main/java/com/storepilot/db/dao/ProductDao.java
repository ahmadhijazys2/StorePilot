package com.storepilot.db.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.storepilot.db.entities.Product;

import java.util.List;

@Dao
public interface ProductDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Product product);

    @Update
    void update(Product product);

    @Delete
    void delete(Product product);

    @Query("SELECT * FROM products ORDER BY name ASC")
    LiveData<List<Product>> getAllProducts();

    @Query("SELECT * FROM products WHERE id = :id LIMIT 1")
    LiveData<Product> getById(int id);

    @Query("SELECT * FROM products WHERE quantity <= :threshold ORDER BY quantity ASC")
    LiveData<List<Product>> getLowStockProducts(int threshold);

    @Query("SELECT p.* FROM products p " +
           "INNER JOIN (SELECT productId, SUM(quantity) as totalSold FROM sales " +
           "WHERE saleDate BETWEEN :startDate AND :endDate GROUP BY productId " +
           "ORDER BY totalSold DESC LIMIT 10) s ON p.id = s.productId " +
           "ORDER BY s.totalSold DESC")
    LiveData<List<Product>> getTopSellingProducts(long startDate, long endDate);

    @Query("SELECT * FROM products WHERE id = :id LIMIT 1")
    Product getByIdSync(int id);

    // Alias used in ProductDetailFragment
    @Query("SELECT * FROM products WHERE id = :id LIMIT 1")
    Product findById(int id);

    // Count products with low stock (for dashboard alert)
    @Query("SELECT COUNT(*) FROM products WHERE quantity <= :threshold")
    LiveData<Integer> getLowStockCount(int threshold);

    // Synchronous version used by LowStockReceiver on background thread
    @Query("SELECT COUNT(*) FROM products WHERE quantity <= :threshold")
    int getLowStockCountSync(int threshold);
}
