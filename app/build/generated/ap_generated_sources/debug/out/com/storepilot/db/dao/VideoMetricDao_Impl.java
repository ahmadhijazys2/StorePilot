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
import com.storepilot.db.entities.VideoMetric;
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
public final class VideoMetricDao_Impl implements VideoMetricDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<VideoMetric> __insertionAdapterOfVideoMetric;

  private final EntityDeletionOrUpdateAdapter<VideoMetric> __deletionAdapterOfVideoMetric;

  private final EntityDeletionOrUpdateAdapter<VideoMetric> __updateAdapterOfVideoMetric;

  public VideoMetricDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfVideoMetric = new EntityInsertionAdapter<VideoMetric>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `video_metrics` (`id`,`title`,`platform`,`views`,`likes`,`shares`,`comments`,`videoDate`,`recordedBy`) VALUES (nullif(?, 0),?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final VideoMetric entity) {
        statement.bindLong(1, entity.id);
        if (entity.title == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.title);
        }
        if (entity.platform == null) {
          statement.bindNull(3);
        } else {
          statement.bindString(3, entity.platform);
        }
        statement.bindLong(4, entity.views);
        statement.bindLong(5, entity.likes);
        statement.bindLong(6, entity.shares);
        statement.bindLong(7, entity.comments);
        statement.bindLong(8, entity.videoDate);
        if (entity.recordedBy == null) {
          statement.bindNull(9);
        } else {
          statement.bindLong(9, entity.recordedBy);
        }
      }
    };
    this.__deletionAdapterOfVideoMetric = new EntityDeletionOrUpdateAdapter<VideoMetric>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `video_metrics` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final VideoMetric entity) {
        statement.bindLong(1, entity.id);
      }
    };
    this.__updateAdapterOfVideoMetric = new EntityDeletionOrUpdateAdapter<VideoMetric>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `video_metrics` SET `id` = ?,`title` = ?,`platform` = ?,`views` = ?,`likes` = ?,`shares` = ?,`comments` = ?,`videoDate` = ?,`recordedBy` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          final VideoMetric entity) {
        statement.bindLong(1, entity.id);
        if (entity.title == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.title);
        }
        if (entity.platform == null) {
          statement.bindNull(3);
        } else {
          statement.bindString(3, entity.platform);
        }
        statement.bindLong(4, entity.views);
        statement.bindLong(5, entity.likes);
        statement.bindLong(6, entity.shares);
        statement.bindLong(7, entity.comments);
        statement.bindLong(8, entity.videoDate);
        if (entity.recordedBy == null) {
          statement.bindNull(9);
        } else {
          statement.bindLong(9, entity.recordedBy);
        }
        statement.bindLong(10, entity.id);
      }
    };
  }

  @Override
  public long insert(final VideoMetric metric) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      final long _result = __insertionAdapterOfVideoMetric.insertAndReturnId(metric);
      __db.setTransactionSuccessful();
      return _result;
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void delete(final VideoMetric metric) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __deletionAdapterOfVideoMetric.handle(metric);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public void update(final VideoMetric metric) {
    __db.assertNotSuspendingTransaction();
    __db.beginTransaction();
    try {
      __updateAdapterOfVideoMetric.handle(metric);
      __db.setTransactionSuccessful();
    } finally {
      __db.endTransaction();
    }
  }

  @Override
  public LiveData<List<VideoMetric>> getAllMetrics() {
    final String _sql = "SELECT * FROM video_metrics ORDER BY videoDate DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return __db.getInvalidationTracker().createLiveData(new String[] {"video_metrics"}, false, new Callable<List<VideoMetric>>() {
      @Override
      @Nullable
      public List<VideoMetric> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTitle = CursorUtil.getColumnIndexOrThrow(_cursor, "title");
          final int _cursorIndexOfPlatform = CursorUtil.getColumnIndexOrThrow(_cursor, "platform");
          final int _cursorIndexOfViews = CursorUtil.getColumnIndexOrThrow(_cursor, "views");
          final int _cursorIndexOfLikes = CursorUtil.getColumnIndexOrThrow(_cursor, "likes");
          final int _cursorIndexOfShares = CursorUtil.getColumnIndexOrThrow(_cursor, "shares");
          final int _cursorIndexOfComments = CursorUtil.getColumnIndexOrThrow(_cursor, "comments");
          final int _cursorIndexOfVideoDate = CursorUtil.getColumnIndexOrThrow(_cursor, "videoDate");
          final int _cursorIndexOfRecordedBy = CursorUtil.getColumnIndexOrThrow(_cursor, "recordedBy");
          final List<VideoMetric> _result = new ArrayList<VideoMetric>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final VideoMetric _item;
            _item = new VideoMetric();
            _item.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfTitle)) {
              _item.title = null;
            } else {
              _item.title = _cursor.getString(_cursorIndexOfTitle);
            }
            if (_cursor.isNull(_cursorIndexOfPlatform)) {
              _item.platform = null;
            } else {
              _item.platform = _cursor.getString(_cursorIndexOfPlatform);
            }
            _item.views = _cursor.getLong(_cursorIndexOfViews);
            _item.likes = _cursor.getLong(_cursorIndexOfLikes);
            _item.shares = _cursor.getLong(_cursorIndexOfShares);
            _item.comments = _cursor.getLong(_cursorIndexOfComments);
            _item.videoDate = _cursor.getLong(_cursorIndexOfVideoDate);
            if (_cursor.isNull(_cursorIndexOfRecordedBy)) {
              _item.recordedBy = null;
            } else {
              _item.recordedBy = _cursor.getInt(_cursorIndexOfRecordedBy);
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
  public LiveData<VideoMetric> getById(final int id) {
    final String _sql = "SELECT * FROM video_metrics WHERE id = ? LIMIT 1";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, id);
    return __db.getInvalidationTracker().createLiveData(new String[] {"video_metrics"}, false, new Callable<VideoMetric>() {
      @Override
      @Nullable
      public VideoMetric call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTitle = CursorUtil.getColumnIndexOrThrow(_cursor, "title");
          final int _cursorIndexOfPlatform = CursorUtil.getColumnIndexOrThrow(_cursor, "platform");
          final int _cursorIndexOfViews = CursorUtil.getColumnIndexOrThrow(_cursor, "views");
          final int _cursorIndexOfLikes = CursorUtil.getColumnIndexOrThrow(_cursor, "likes");
          final int _cursorIndexOfShares = CursorUtil.getColumnIndexOrThrow(_cursor, "shares");
          final int _cursorIndexOfComments = CursorUtil.getColumnIndexOrThrow(_cursor, "comments");
          final int _cursorIndexOfVideoDate = CursorUtil.getColumnIndexOrThrow(_cursor, "videoDate");
          final int _cursorIndexOfRecordedBy = CursorUtil.getColumnIndexOrThrow(_cursor, "recordedBy");
          final VideoMetric _result;
          if (_cursor.moveToFirst()) {
            _result = new VideoMetric();
            _result.id = _cursor.getInt(_cursorIndexOfId);
            if (_cursor.isNull(_cursorIndexOfTitle)) {
              _result.title = null;
            } else {
              _result.title = _cursor.getString(_cursorIndexOfTitle);
            }
            if (_cursor.isNull(_cursorIndexOfPlatform)) {
              _result.platform = null;
            } else {
              _result.platform = _cursor.getString(_cursorIndexOfPlatform);
            }
            _result.views = _cursor.getLong(_cursorIndexOfViews);
            _result.likes = _cursor.getLong(_cursorIndexOfLikes);
            _result.shares = _cursor.getLong(_cursorIndexOfShares);
            _result.comments = _cursor.getLong(_cursorIndexOfComments);
            _result.videoDate = _cursor.getLong(_cursorIndexOfVideoDate);
            if (_cursor.isNull(_cursorIndexOfRecordedBy)) {
              _result.recordedBy = null;
            } else {
              _result.recordedBy = _cursor.getInt(_cursorIndexOfRecordedBy);
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

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
