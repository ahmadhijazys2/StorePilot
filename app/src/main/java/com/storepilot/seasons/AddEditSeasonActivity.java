package com.storepilot.seasons;

import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.db.entities.Season;
import com.storepilot.viewmodels.SeasonViewModel;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class AddEditSeasonActivity extends BaseActivity {

    public static final String EXTRA_SEASON_ID = "season_id";

    private EditText etSeasonName, etStartDate, etEndDate, etAlertDays, etSeasonNotes;
    private CheckBox cbIsActive;
    private Button btnSaveSeason;
    private SeasonViewModel seasonViewModel;
    private Season existingSeason = null;
    private final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_edit_season);

        etSeasonName = findViewById(R.id.etSeasonName);
        etStartDate = findViewById(R.id.etSeasonStartDate);
        etEndDate = findViewById(R.id.etSeasonEndDate);
        etAlertDays = findViewById(R.id.etAlertDays);
        etSeasonNotes = findViewById(R.id.etSeasonNotes);
        cbIsActive = findViewById(R.id.cbSeasonActive);
        btnSaveSeason = findViewById(R.id.btnSaveSeason);

        seasonViewModel = new ViewModelProvider(this).get(SeasonViewModel.class);

        int seasonId = getIntent().getIntExtra(EXTRA_SEASON_ID, -1);
        if (seasonId != -1) {
            seasonViewModel.getById(seasonId).observe(this, season -> {
                if (season != null && existingSeason == null) {
                    existingSeason = season;
                    etSeasonName.setText(season.getName());
                    etStartDate.setText(dateFormat.format(new Date(season.getStartDate())));
                    etEndDate.setText(dateFormat.format(new Date(season.getEndDate())));
                    etAlertDays.setText(String.valueOf(season.getAlertDaysBeforeEnd()));
                    etSeasonNotes.setText(season.getNotes());
                    cbIsActive.setChecked(season.isActive());
                }
            });
        }

        btnSaveSeason.setOnClickListener(v -> saveSeason());
    }

    private void saveSeason() {
        String name = etSeasonName.getText().toString().trim();
        String startStr = etStartDate.getText().toString().trim();
        String endStr = etEndDate.getText().toString().trim();
        String alertStr = etAlertDays.getText().toString().trim();
        String notes = etSeasonNotes.getText().toString().trim();
        boolean isActive = cbIsActive.isChecked();

        if (name.isEmpty() || startStr.isEmpty() || endStr.isEmpty()) {
            Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            long startDate = dateFormat.parse(startStr).getTime();
            long endDate = dateFormat.parse(endStr).getTime();
            int alertDays = alertStr.isEmpty() ? 30 : Integer.parseInt(alertStr);

            if (existingSeason != null) {
                existingSeason.name = name;
                existingSeason.startDate = startDate;
                existingSeason.endDate = endDate;
                existingSeason.alertDaysBeforeEnd = alertDays;
                existingSeason.notes = notes;
                existingSeason.isActive = isActive;
                seasonViewModel.update(existingSeason);
            } else {
                Season season = new Season(name, startDate, endDate, alertDays, isActive, notes);
                seasonViewModel.insert(season);
            }
            finish();
        } catch (ParseException e) {
            Toast.makeText(this, getString(R.string.error_invalid_date), Toast.LENGTH_SHORT).show();
        }
    }
}
