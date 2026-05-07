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
import com.storepilot.db.entities.Purchase;
import java.lang.Class;
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
public final class PurchaseDao_Impl implements PurchaseDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<Purchase> __insertionAdapterOfPurchase;

  private final EntityDeletionOrUpdateAdapter<Purchase> __deletionAdapterOfPurchase;

  private final EntityDeletionOrUpdateAdapter<Purchase> __updateAdapterOfPurchase;

  public PurchaseDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfPurchase = new EntityInsertionAdapter<Purchase>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `purchases` (`id`,`productId`,`quantity`,`totalCost`,`purchaseDate`,`purchasedBy`,`supplier`,`notes`) VALUES (nullif(?, 0),?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Purchase entity) {
        statement.bindLong(1, entity.id);
        if (entity.productId == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.productId);
        }
        statement.bindLong(3, entity.quantity);
        statement.bindDouble(4, entity.totalCost);
        statement.bindLong(5, entity.purchaseDate);
        if (entity.purchasedBy == null) {
          statement.bindNull(6);
        } else {
          statement.bindLong(6, entity.purchasedBy);
        }
        if (entity.supplier == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.supplier);
        }
        if (entity.notes == null) {
          statement.bindNull(8);
        } else {
          statement.bindString(8, entity.notes);
        }
      }
    };
    this.__deletionAdapterOfPurchase = new EntityDeletionOrUpdateAdapter<Purchase>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `purchases` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Purchase entity) {
        statement.bindLong(1, entity.id);
      }
    };
    this.__updateAdapterOfPurchase = new EntityDeletionOrUpdateAdapter<Purchase>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `purchases` SET `id` = ?,`productId` = ?,`quantity` = ?,`totalCost` = ?,`purchaseDate` = ?,`purchasedBy` = ?,`supplier` = ?,`notes` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Purchase entity) {
        statement.bindLong(1, entity.id);
        if (entity.productId == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.productId);
        }
        statement.bindLong(3, entity.quantity);
        statement.bindDouble(4, entity.totalCost);
        statement.bindLong(5, entity.purchaseDate);
        if (entity.purchasedBy == null) {
          statement.bindNull(6);
        } else {
          statement.bindLong(6, entity.purchasedBy);
        }
        if (entity.supplier == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.supplier);
        }
        if (entity.notes == null) {
          statement.bindNull(8);
        } else {
          statement.bindString(8, entity.notes);
        }
        statement.bindLong(9, entity.id);
      }
    };
  }

  @Override
  public long insert(final Purchase purchase) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfPurchase.insertAndReturnId(purchase);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void delete(final Purchase purchase) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __deletionAdapterOfPurchase.handle(purchase);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void update(final Purchase purchase) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __updateAdapterOfPurchase.handle(purchase);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<Purchase>> getAllPurchases() {
    final String _sql = "SELECT * FROM purchases ORDER BY purchaseDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"purchases"}, false, new Callable<List<Purchase>>() {
      @Override
      @Nullable
      public List<Purchase> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalCost = CursorUtil.getColumnIndexOrThrow(_cursor, "totalCost");
          final int _cursorIndexOfPurchaseDate = CursorUtil.getColumnIndexOrThrow(_cursor, "purchaseDate");
          final int _cursorIndexOfPurchasedBy = CursorUtil.getColumnIndexOrThrow(_cursor, "purchasedBy");
          final int _cursorIndexOfSupplier = CursorUtil.getColumnIndexOrThrow(_cursor, "supplier");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Purchase> _result = new ArrayList<Purchase>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Purchase _item;
            _item = new Purchase();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _item.productId = null;
            } else {
              _item.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _item.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _item.totalCost = _cursor.getDouble(_cursorIndexOfTotalCost);
            _item.purchaseDate = _cursor.getLong(_cursorIndexOfPurchaseDate);
            if (_cursor.isNull(_cursorIndexOfPurchasedBy)) {
              _item.purchasedBy = null;
            } else {
              _item.purchasedBy = _cursor.getInt(_cursorIndexOfPurchasedBy);
            }
            if (_cursor.isNull(_cursorIndexOfSupplier)) {
              _item.supplier = null;
            } else {
              _item.supplier = _cursor.getString(_cursorIndexOfSupplier);
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
  public LiveData<Purchase> getById(final int id) {
    final String _sql = "SELECT * FROM purchases WHERE id = ? LIMIT 1";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, id);
    return __db.getInvalidationTracker().createLiveData(new String[] {"purchases"}, false, new Callable<Purchase>() {
      @Override
      @Nullable
      public Purchase call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalCost = CursorUtil.getColumnIndexOrThrow(_cursor, "totalCost");
          final int _cursorIndexOfPurchaseDate = CursorUtil.getColumnIndexOrThrow(_cursor, "purchaseDate");
          final int _cursorIndexOfPurchasedBy = CursorUtil.getColumnIndexOrThrow(_cursor, "purchasedBy");
          final int _cursorIndexOfSupplier = CursorUtil.getColumnIndexOrThrow(_cursor, "supplier");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final Purchase _result;
          if (_cursor.moveToFirst()) {
            _result = new Purchase();
            _result.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _result.productId = null;
            } else {
              _result.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _result.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _result.totalCost = _cursor.getDouble(_cursorIndexOfTotalCost);
            _result.purchaseDate = _cursor.getLong(_cursorIndexOfPurchaseDate);
            if (_cursor.isNull(_cursorIndexOfPurchasedBy)) {
              _result.purchasedBy = null;
            } else {
              _result.purchasedBy = _cursor.getInt(_cursorIndexOfPurchasedBy);
            }
            if (_cursor.isNull(_cursorIndexOfSupplier)) {
              _result.supplier = null;
            } else {
              _result.supplier = _cursor.getString(_cursorIndexOfSupplier);
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
  public LiveData<List<Purchase>> getPurchasesByDateRange(final long startDate,
      final long endDate) {
    final String _sql = "SELECT * FROM purchases WHERE purchaseDate BETWEEN ? AND ? ORDER BY purchaseDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 2);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, startDate);
    _argIndex = 2;
    _statement.bindLong(_argIndex, endDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"purchases"}, false, new Callable<List<Purchase>>() {
      @Override
      @Nullable
      public List<Purchase> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfTotalCost = CursorUtil.getColumnIndexOrThrow(_cursor, "totalCost");
          final int _cursorIndexOfPurchaseDate = CursorUtil.getColumnIndexOrThrow(_cursor, "purchaseDate");
          final int _cursorIndexOfPurchasedBy = CursorUtil.getColumnIndexOrThrow(_cursor, "purchasedBy");
          final int _cursorIndexOfSupplier = CursorUtil.getColumnIndexOrThrow(_cursor, "supplier");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Purchase> _result = new ArrayList<Purchase>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Purchase _item;
            _item = new Purchase();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfProductId)) {
              _item.productId = null;
            } else {
              _item.productId = _cursor.getInt(_cursorIndexOfProductId);
            }
            _item.quantity = _cursor.getInt(_cursorIndexOfQuantity);
            _item.totalCost = _cursor.getDouble(_cursorIndexOfTotalCost);
            _item.purchaseDate = _cursor.getLong(_cursorIndexOfPurchaseDate);
            if (_cursor.isNull(_cursorIndexOfPurchasedBy)) {
              _item.purchasedBy = null;
            } else {
              _item.purchasedBy = _cursor.getInt(_cursorIndexOfPurchasedBy);
            }
            if (_cursor.isNull(_cursorIndexOfSupplier)) {
              _item.supplier = null;
            } else {
              _item.supplier = _cursor.getString(_cursorIndexOfSupplier);
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

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
