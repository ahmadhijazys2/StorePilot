package com.storepilot.db.dao;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.lifecycle.LiveData;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.storepilot.db.entities.Sale;
import java.lang.Class;
import java.lang.Double;
import java.lang.Exception;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class SaleDao_Impl implements SaleDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<Sale> __insertionAdapterOfSale;

  private final EntityDeletionOrUpdateAdapter<Sale> __deletionAdapterOfSale;

  private final EntityDeletionOrUpdateAdapter<Sale> __updateAdapterOfSale;

  public SaleDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfSale = new EntityInsertionAdapter<Sale>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `sales` (`id`,`productId`,`quantity`,`totalPrice`,`saleDate`,`soldBy`,`notes`) VALUES (nullif(?, 0),?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Sale entity) {
        statement.bindLong(1, entity.id);
        if (entity.productId == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.productId);
        }
        statement.bindLong(3, entity.quantity);
        statement.bindDouble(4, entity.totalPrice);
        statement.bindLong(5, entity.saleDate);
        if (entity.soldBy == null) {
          statement.bindNull(6);
        } else {
          statement.bindLong(6, entity.soldBy);
        }
        if (entity.notes == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.notes);
        }
      }
    };
    this.__deletionAdapterOfSale = new EntityDeletionOrUpdateAdapter<Sale>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `sales` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Sale entity) {
        statement.bindLong(1, entity.id);
      }
    };
    this.__updateAdapterOfSale = new EntityDeletionOrUpdateAdapter<Sale>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `sales` SET `id` = ?,`productId` = ?,`quantity` = ?,`totalPrice` = ?,`saleDate` = ?,`soldBy` = ?,`notes` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Sale entity) {
        statement.bindLong(1, entity.id);
        if (entity.productId == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.productId);
        }
        statement.bindLong(3, entity.quantity);
        statement.bindDouble(4, entity.totalPrice);
        statement.bindLong(5, entity.saleDate);
        if (entity.soldBy == null) {
          statement.bindNull(6);
        } else {
          statement.bindLong(6, entity.soldBy);
        }
        if (entity.notes == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.notes);
        }
        statement.bindLong(8, entity.id);
      }
    };
  }

  @Override
  public long insert(final Sale sale) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfSale.insertAndReturnId(sale);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void delete(final Sale sale) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __deletionAdapterOfSale.handle(sale);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void update(final Sale sale) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __updateAdapterOfSale.handle(sale);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<Sale>> getAllSales() {
    final String _sql = "SELECT * FROM sales ORDER BY saleDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<List<Sale>>() {
      @Override
      @Nullable
      public List<Sale> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "totalPrice");
          final int _cursorIndexOfSaleDate = CursorUtil.getColumnIndexOrThrow(_cursor, "saleDate");
          final int _cursorIndexOfSoldBy = CursorUtil.getColumnIndexOrThrow(_cursor, "soldBy");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Sale> _result = new ArrayList<Sale>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Sale _item;
            _item = new Sale();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _item.productId = null;
            } else {
              _item.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _item.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _item.totalPrice = _cursor.getDouble(_cursorIndexOfTotalPrice);
            _item.saleDate = _cursor.getLong(_cursorIndexOfSaleDate);
            if (_cursor.isNull(_cursorIndexOfSoldBy)) {
              _item.soldBy = null;
            } else {
              _item.soldBy = _cursor.getInt(_cursorIndexOfSoldBy);
            }
            if (_cursor.isNull(_cursorIndexOfNotes)) {
              _item.notes = null;
            } else {
              _item.notes = _cursor.getString(_cursorIndexOfNotes);
            }
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Sale> getById(final int id) {
    final String _sql = "SELECT * FROM sales WHERE id = ? LIMIT 1";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, id);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Sale>() {
      @Override
      @Nullable
      public Sale call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "totalPrice");
          final int _cursorIndexOfSaleDate = CursorUtil.getColumnIndexOrThrow(_cursor, "saleDate");
          final int _cursorIndexOfSoldBy = CursorUtil.getColumnIndexOrThrow(_cursor, "soldBy");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final Sale _result;
          if (_cursor.moveToFirst()) {
            _result = new Sale();
            _result.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _result.productId = null;
            } else {
              _result.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _result.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _result.totalPrice = _cursor.getDouble(_cursorIndexOfTotalPrice);
            _result.saleDate = _cursor.getLong(_cursorIndexOfSaleDate);
            if (_cursor.isNull(_cursorIndexOfSoldBy)) {
              _result.soldBy = null;
            } else {
              _result.soldBy = _cursor.getInt(_cursorIndexOfSoldBy);
            }
            if (_cursor.isNull(_cursorIndexOfNotes)) {
              _result.notes = null;
            } else {
              _result.notes = _cursor.getString(_cursorIndexOfNotes);
            }
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<List<Sale>> getSalesByDateRange(final long startDate, final long endDate) {
    final String _sql = "SELECT * FROM sales WHERE saleDate BETWEEN ? AND ? ORDER BY saleDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 2);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, startDate);
    _argIndex = 2;
    _statement.bindLong(_argIndex, endDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<List<Sale>>() {
      @Override
      @Nullable
      public List<Sale> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "totalPrice");
          final int _cursorIndexOfSaleDate = CursorUtil.getColumnIndexOrThrow(_cursor, "saleDate");
          final int _cursorIndexOfSoldBy = CursorUtil.getColumnIndexOrThrow(_cursor, "soldBy");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Sale> _result = new ArrayList<Sale>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Sale _item;
            _item = new Sale();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _item.productId = null;
            } else {
              _item.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _item.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _item.totalPrice = _cursor.getDouble(_cursorIndexOfTotalPrice);
            _item.saleDate = _cursor.getLong(_cursorIndexOfSaleDate);
            if (_cursor.isNull(_cursorIndexOfSoldBy)) {
              _item.soldBy = null;
            } else {
              _item.soldBy = _cursor.getInt(_cursorIndexOfSoldBy);
            }
            if (_cursor.isNull(_cursorIndexOfNotes)) {
              _item.notes = null;
            } else {
              _item.notes = _cursor.getString(_cursorIndexOfNotes);
            }
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Double> getSalesTotalByRange(final long startDate, final long endDate) {
    final String _sql = "SELECT SUM(totalPrice) FROM sales WHERE saleDate BETWEEN ? AND ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 2);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, startDate);
    _argIndex = 2;
    _statement.bindLong(_argIndex, endDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Double> getSalesTotalByWeek(final long refDate) {
    final String _sql = "SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y-%W', saleDate/1000, 'unixepoch') = strftime('%Y-%W', ?/1000, 'unixepoch')";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, refDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Double> getSalesTotalByMonth(final long refDate) {
    final String _sql = "SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y-%m', saleDate/1000, 'unixepoch') = strftime('%Y-%m', ?/1000, 'unixepoch')";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, refDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Double> getSalesTotalByYear(final long refDate) {
    final String _sql = "SELECT SUM(totalPrice) FROM sales WHERE strftime('%Y', saleDate/1000, 'unixepoch') = strftime('%Y', ?/1000, 'unixepoch')";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, refDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public LiveData<Double> getTodaySalesTotal(final long startOfDay, final long endOfDay) {
    final String _sql = "SELECT SUM(totalPrice) FROM sales WHERE saleDate >= ? AND saleDate < ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 2);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, startOfDay);
    _argIndex = 2;
    _statement.bindLong(_argIndex, endOfDay);
    return __db.getInvalidationTracker().createLiveData(new String[] {"sales"}, false, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
