package com.storepilot.tasks;

import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.ArrayAdapter;
import android.widget.Toast;

import androidx.lifecycle.ViewModelProvider;

import com.storepilot.R;
import com.storepilot.core.BaseActivity;
import com.storepilot.core.SessionManager;
import com.storepilot.db.entities.Task;
import com.storepilot.viewmodels.TaskViewModel;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Locale;

public class AddEditTaskActivity extends BaseActivity {

    public static final String EXTRA_TASK_ID = "task_id";

    private EditText etTaskTitle, etTaskDescription, etAssignedTo, etDueDate;
    private Spinner spinnerStatus, spinnerPriority;
    private CheckBox cbPrivate;
    private Button btnSaveTask;
    private TaskViewModel taskViewModel;
    private Task existingTask = null;
    private final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_edit_task);

        etTaskTitle = findViewById(R.id.etTaskTitle);
        etTaskDescription = findViewById(R.id.etTaskDescription);
        etAssignedTo = findViewById(R.id.etAssignedTo);
        etDueDate = findViewById(R.id.etTaskDueDate);
        spinnerStatus = findViewById(R.id.spinnerTaskStatus);
        spinnerPriority = findViewById(R.id.spinnerTaskPriority);
        cbPrivate = findViewById(R.id.cbTaskPrivate);
        btnSaveTask = findViewById(R.id.btnSaveTask);

        ArrayAdapter<CharSequence> statusAdapter = ArrayAdapter.createFromResource(
                this, R.array.task_statuses, android.R.layout.simple_spinner_item);
        statusAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerStatus.setAdapter(statusAdapter);

        ArrayAdapter<CharSequence> priorityAdapter = ArrayAdapter.createFromResource(
                this, R.array.task_priorities, android.R.layout.simple_spinner_item);
        priorityAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerPriority.setAdapter(priorityAdapter);

        taskViewModel = new ViewModelProvider(this).get(TaskViewModel.class);

        int taskId = getIntent().getIntExtra(EXTRA_TASK_ID, -1);
        if (taskId != -1) {
            taskViewModel.getById(taskId).observe(this, task -> {
                if (task != null && existingTask == null) {
                    existingTask = task;
                    etTaskTitle.setText(task.getTitle());
                    etTaskDescription.setText(task.getDescription());
                    if (task.getDueDate() > 0) {
                        etDueDate.setText(dateFormat.format(new java.util.Date(task.getDueDate())));
                    }
                    cbPrivate.setChecked(task.isPrivate());
                }
            });
        }

        btnSaveTask.setOnClickListener(v -> saveTask());
    }

    private void saveTask() {
        String title = etTaskTitle.getText().toString().trim();
        String description = etTaskDescription.getText().toString().trim();
        String dueDateStr = etDueDate.getText().toString().trim();
        String status = spinnerStatus.getSelectedItem().toString();
        String priority = spinnerPriority.getSelectedItem().toString();
        boolean isPrivate = cbPrivate.isChecked();
        int createdBy = SessionManager.getInstance().getLoggedInUser() != null
                ? SessionManager.getInstance().getLoggedInUser().getId() : 0;

        if (title.isEmpty()) {
            Toast.makeText(this, getString(R.string.error_fill_all_fields), Toast.LENGTH_SHORT).show();
            return;
        }

        long dueDate = 0;
        if (!dueDateStr.isEmpty()) {
            try {
                dueDate = dateFormat.parse(dueDateStr).getTime();
            } catch (ParseException e) {
                Toast.makeText(this, getString(R.string.error_invalid_date), Toast.LENGTH_SHORT).show();
                return;
            }
        }

        Integer assignedTo = null;
        String assignedStr = etAssignedTo.getText().toString().trim();
        if (!assignedStr.isEmpty()) {
            try { assignedTo = Integer.parseInt(assignedStr); } catch (NumberFormatException ignored) {}
        }

        if (existingTask != null) {
            existingTask.title = title;
            existingTask.description = description;
            existingTask.assignedTo = assignedTo;
            existingTask.status = status;
            existingTask.priority = priority;
            existingTask.isPrivate = isPrivate;
            existingTask.dueDate = dueDate;
            taskViewModel.update(existingTask);
        } else {
            Task task = new Task(title, description, assignedTo, createdBy, status, priority,
                    isPrivate, dueDate, System.currentTimeMillis());
            taskViewModel.insert(task);
        }
        finish();
    }
}
