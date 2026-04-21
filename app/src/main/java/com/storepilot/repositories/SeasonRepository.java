package com.storepilot.repositories;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.storepilot.core.AppDatabase;
import com.storepilot.db.dao.SeasonDao;
import com.storepilot.db.entities.Season;

import java.util.List;

public class SeasonRepository {

    private final SeasonDao seasonDao;

    public SeasonRepository(Application application) {
        AppDatabase db = AppDatabase.getInstance(application);
        seasonDao = db.seasonDao();
    }

    public LiveData<List<Season>> getAllSeasons() {
        return seasonDao.getAllSeasons();
    }

    public LiveData<Season> getById(int id) {
        return seasonDao.getById(id);
    }

    public LiveData<List<Season>> getSeasonsEndingSoon(long currentDate) {
        return seasonDao.getSeasonsEndingSoon(currentDate);
    }

    public void insert(Season season) {
        AppDatabase.dbExecutor.execute(() -> seasonDao.insert(season));
    }

    public void update(Season season) {
        AppDatabase.dbExecutor.execute(() -> seasonDao.update(season));
    }

    public void delete(Season season) {
        AppDatabase.dbExecutor.execute(() -> seasonDao.delete(season));
    }
}
