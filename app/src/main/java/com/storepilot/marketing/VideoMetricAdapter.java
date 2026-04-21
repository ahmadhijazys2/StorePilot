package com.storepilot.marketing;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.VideoMetric;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class VideoMetricAdapter extends RecyclerView.Adapter<VideoMetricAdapter.ViewHolder> {

    private List<VideoMetric> metrics = new ArrayList<>();

    public void setMetrics(List<VideoMetric> metrics) {
        this.metrics = metrics != null ? metrics : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_video_metric, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        VideoMetric m = metrics.get(position);
        holder.tvTitle.setText(m.getTitle());
        holder.tvPlatform.setText(m.getPlatform());
        holder.tvViews.setText(NumberFormat.getNumberInstance(Locale.US).format(m.getViews()));
        holder.tvLikes.setText(NumberFormat.getNumberInstance(Locale.US).format(m.getLikes()));
    }

    @Override
    public int getItemCount() {
        return metrics.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvTitle, tvPlatform, tvViews, tvLikes;

        ViewHolder(View itemView) {
            super(itemView);
            tvTitle = itemView.findViewById(R.id.tvMetricTitle);
            tvPlatform = itemView.findViewById(R.id.tvMetricPlatform);
            tvViews = itemView.findViewById(R.id.tvMetricViews);
            tvLikes = itemView.findViewById(R.id.tvMetricLikes);
        }
    }
}
