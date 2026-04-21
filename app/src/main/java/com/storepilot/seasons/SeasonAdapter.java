package com.storepilot.seasons;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.storepilot.R;
import com.storepilot.db.entities.Season;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class SeasonAdapter extends RecyclerView.Adapter<SeasonAdapter.ViewHolder> {

    private List<Season> seasons = new ArrayList<>();

    public void setSeasons(List<Season> seasons) {
        this.seasons = seasons != null ? seasons : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_season, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Season s = seasons.get(position);
        SimpleDateFormat sdf = new SimpleDateFormat("MMM dd, yyyy", Locale.getDefault());
        holder.tvSeasonName.setText(s.getName());
        holder.tvSeasonDates.setText(sdf.format(new Date(s.getStartDate()))
                + " - " + sdf.format(new Date(s.getEndDate())));
        holder.tvSeasonActive.setText(s.isActive() ? "Active" : "Inactive");
    }

    @Override
    public int getItemCount() {
        return seasons.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvSeasonName, tvSeasonDates, tvSeasonActive;

        ViewHolder(View itemView) {
            super(itemView);
            tvSeasonName = itemView.findViewById(R.id.tvSeasonName);
            tvSeasonDates = itemView.findViewById(R.id.tvSeasonDates);
            tvSeasonActive = itemView.findViewById(R.id.tvSeasonActive);
        }
    }
}
