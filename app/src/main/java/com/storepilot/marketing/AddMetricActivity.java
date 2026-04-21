package com.storepilot.marketing;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.VideoMetric;
import com.storepilot.viewmodels.VideoMetricViewModel;

public class AddMetricActivity extends BaseActivity {

    private EditText etTitle, etPlatform, etViews, etLikes, etShares, etComments;
    private Button btnSaveMetric;
    private VideoMetricViewModel viewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_metric);

        etTitle = findViewById(R.id.etMetricTitle);
        etPlatform = findViewById(R.id.etMetricPlatform);
        etViews = findViewById(R.id.etMetricViews);
        etLikes = findViewById(R.id.etMetricLikes);
        etShares = findViewById(R.id.etMetricShares);
        etComments = findViewById(R.id.etMetricComments);
        btnSaveMetric = findViewById(R.id.btnSaveMetric);

        viewModel = new ViewModelProvider(this).get(VideoMetricViewModel.class);

        btnSaveMetric.setOnClickListener(v -> {
            String title = etTitle.getText().toString().trim();
            String platform = etPlatform.getText().toString().trim();
            String viewsStr = etViews.getText().toString().trim();

            if (title.isEmpty() || platform.isEmpty() || viewsStr.isEmpty()) {
                Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
                return;
            }

            long views = Long.parseLong(viewsStr);
            long likes = etLikes.getText().toString().isEmpty() ? 0 : Long.parseLong(etLikes.getText().toString());
            long shares = etShares.getText().toString().isEmpty() ? 0 : Long.parseLong(etShares.getText().toString());
            long comments = etComments.getText().toString().isEmpty() ? 0 : Long.parseLong(etComments.getText().toString());
            int userId = SessionManager.getInstance().getLoggedInUser() != null
                    ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

            VideoMetric metric = new VideoMetric(title, platform, views, likes, shares, comments,
                    System.currentTimeMillis(), userId);
            viewModel.insert(metric);
            finish();
        });
    }
}
