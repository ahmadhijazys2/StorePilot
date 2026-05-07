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
import com.storepilot.db.entities.Season;
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
public final class SeasonDao_Impl implements SeasonDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<Season> __insertionAdapterOfSeason;

  private final EntityDeletionOrUpdateAdapter<Season> __deletionAdapterOfSeason;

  private final EntityDeletionOrUpdateAdapter<Season> __updateAdapterOfSeason;

  public SeasonDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfSeason = new EntityInsertionAdapter<Season>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `seasons` (`id`,`name`,`startDate`,`endDate`,`alertDaysBeforeEnd`,`isActive`,`notes`) VALUES (nullif(?, 0),?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Season entity) {
        statement.bindLong(1, entity.id);
        if (entity.name == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.name);
        }
        statement.bindLong(3, entity.startDate);
        statement.bindLong(4, entity.endDate);
        statement.bindLong(5, entity.alertDaysBeforeEnd);
        final int _tmp = entity.isActive ? 1 : 0;
        statement.bindLong(6, _tmp);
        if (entity.notes == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.notes);
        }
      }
    };
    this.__deletionAdapterOfSeason = new EntityDeletionOrUpdateAdapter<Season>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `seasons` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Season entity) {
        statement.bindLong(1, entity.id);
      }
    };
    this.__updateAdapterOfSeason = new EntityDeletionOrUpdateAdapter<Season>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `seasons` SET `id` = ?,`name` = ?,`startDate` = ?,`endDate` = ?,`alertDaysBeforeEnd` = ?,`isActive` = ?,`notes` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement, final Season entity) {
        statement.bindLong(1, entity.id);
        if (entity.name == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.name);
        }
        statement.bindLong(3, entity.startDate);
        statement.bindLong(4, entity.endDate);
        statement.bindLong(5, entity.alertDaysBeforeEnd);
        final int _tmp = entity.isActive ? 1 : 0;
        statement.bindLong(6, _tmp);
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
  public long insert(final Season season) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfSeason.insertAndReturnId(season);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void delete(final Season season) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __deletionAdapterOfSeason.handle(season);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void update(final Season season) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __updateAdapterOfSeason.handle(season);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<Season>> getAllSeasons() {
    final String _sql = "SELECT * FROM seasons ORDER BY startDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"seasons"}, false, new Callable<List<Season>>() {
      @Override
      @Nullable
      public List<Season> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfStartDate = CursorUtil.getColumnIndexOrThrow(_cursor, "startDate");
          final int _cursorIndexOfEndDate = CursorUtil.getColumnIndexOrThrow(_cursor, "endDate");
          final int _cursorIndexOfAlertDaysBeforeEnd = CursorUtil.getColumnIndexOrThrow(_cursor, "alertDaysBeforeEnd");
          final int _cursorIndexOfIsActive = CursorUtil.getColumnIndexOrThrow(_cursor, "isActive");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Season> _result = new ArrayList<Season>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Season _item;
            _item = new Season();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfName)) {
              _item.name = null;
            } else {
              _item.name = _cursor.getString(_cursorIndexOfName);
            }
            _item.startDate = _cursor.getLong(_cursorIndexOfStartDate);
            _item.endDate = _cursor.getLong(_cursorIndexOfEndDate);
            _item.alertDaysBeforeEnd = _cursor.getInt(_cursorIndexOfAlertDaysBeforeEnd);
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsActive);
            _item.isActive = _tmp != 0;
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
  public LiveData<Season> getById(final int id) {
    final String _sql = "SELECT * FROM seasons WHERE id = ? LIMIT 1";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, id);
    return __db.getInvalidationTracker().createLiveData(new String[] {"seasons"}, false, new Callable<Season>() {
      @Override
      @Nullable
      public Season call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfStartDate = CursorUtil.getColumnIndexOrThrow(_cursor, "startDate");
          final int _cursorIndexOfEndDate = CursorUtil.getColumnIndexOrThrow(_cursor, "endDate");
          final int _cursorIndexOfAlertDaysBeforeEnd = CursorUtil.getColumnIndexOrThrow(_cursor, "alertDaysBeforeEnd");
          final int _cursorIndexOfIsActive = CursorUtil.getColumnIndexOrThrow(_cursor, "isActive");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final Season _result;
          if (_cursor.moveToFirst()) {
            _result = new Season();
            _result.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfName)) {
              _result.name = null;
            } else {
              _result.name = _cursor.getString(_cursorIndexOfName);
            }
            _result.startDate = _cursor.getLong(_cursorIndexOfStartDate);
            _result.endDate = _cursor.getLong(_cursorIndexOfEndDate);
            _result.alertDaysBeforeEnd = _cursor.getInt(_cursorIndexOfAlertDaysBeforeEnd);
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsActive);
            _result.isActive = _tmp != 0;
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
  public LiveData<List<Season>> getSeasonsEndingSoon(final long currentDate) {
    final String _sql = "SELECT * FROM seasons WHERE endDate <= (? + (alertDaysBeforeEnd * 86400000)) AND isActive = 1 ORDER BY endDate ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, currentDate);
    return __db.getInvalidationTracker().createLiveData(new String[] {"seasons"}, false, new Callable<List<Season>>() {
      @Override
      @Nullable
      public List<Season> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfName = CursorUtil.getColumnIndexOrThrow(_cursor, "name");
          final int _cursorIndexOfStartDate = CursorUtil.getColumnIndexOrThrow(_cursor, "startDate");
          final int _cursorIndexOfEndDate = CursorUtil.getColumnIndexOrThrow(_cursor, "endDate");
          final int _cursorIndexOfAlertDaysBeforeEnd = CursorUtil.getColumnIndexOrThrow(_cursor, "alertDaysBeforeEnd");
          final int _cursorIndexOfIsActive = CursorUtil.getColumnIndexOrThrow(_cursor, "isActive");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final List<Season> _result = new ArrayList<Season>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Season _item;
            _item = new Season();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfName)) {
              _item.name = null;
            } else {
              _item.name = _cursor.getString(_cursorIndexOfName);
            }
            _item.startDate = _cursor.getLong(_cursorIndexOfStartDate);
            _item.endDate = _cursor.getLong(_cursorIndexOfEndDate);
            _item.alertDaysBeforeEnd = _cursor.getInt(_cursorIndexOfAlertDaysBeforeEnd);
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsActive);
            _item.isActive = _tmp != 0;
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
