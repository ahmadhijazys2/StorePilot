package com.storepilot.tasks;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Task;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class TaskAdapter extends RecyclerView.Adapter<TaskAdapter.ViewHolder> {

    private List<Task> tasks = new ArrayList<>();

    public void setTasks(List<Task> tasks) {
        this.tasks = tasks != null ? tasks : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_task, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Task t = tasks.get(position);
        holder.tvTaskTitle.setText(t.getTitle());
        holder.tvTaskStatus.setText(t.getStatus());
        holder.tvTaskPriority.setText(t.getPriority());
        holder.tvTaskDue.setText(t.getDueDate() > 0
                ? new SimpleDateFormat("MMM dd, yyyy", Locale.getDefault()).format(new Date(t.getDueDate()))
                : "No due date");
    }

    @Override
    public int getItemCount() {
        return tasks.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvTaskTitle, tvTaskStatus, tvTaskPriority, tvTaskDue;

        ViewHolder(View itemView) {
            super(itemView);
            tvTaskTitle = itemView.findViewById(R.id.tvTaskTitle);
            tvTaskStatus = itemView.findViewById(R.id.tvTaskStatus);
            tvTaskPriority = itemView.findViewById(R.id.tvTaskPriority);
            tvTaskDue = itemView.findViewById(R.id.tvTaskDue);
        }
    }
}
