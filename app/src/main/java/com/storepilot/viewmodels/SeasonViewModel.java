package com.storepilot.viewmodels;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.storepilot.db.entities.Season;
import com.storepilot.repositories.SeasonRepository;

import java.util.List;

public class SeasonViewModel extends AndroidViewModel {

    private final SeasonRepository repository;

    public SeasonViewModel(@NonNull Application application) {
        super(application);
        repository = new SeasonRepository(application);
    }

    public LiveData<List<Season>> getAllSeasons() {
        return repository.getAllSeasons();
    }

    public LiveData<Season> getById(int id) {
        return repository.getById(id);
    }

    public LiveData<List<Season>> getSeasonsEndingSoon(long currentDate) {
        return repository.getSeasonsEndingSoon(currentDate);
    }

    public void insert(Season season) {
        repository.insert(season);
    }

    public void update(Season season) {
        repository.update(season);
    }

    public void delete(Season season) {
        repository.delete(season);
    }
}
