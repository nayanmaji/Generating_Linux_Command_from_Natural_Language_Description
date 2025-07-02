package com.example.aiassistant;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.ViewHolder> {

    private List<HistoryItem> historyItems;
    private final DeleteListener deleteListener;
    private final ReplyListener replyListener;

    public interface DeleteListener {
        void onDelete(int position);
    }

    public interface ReplyListener {
        void onReply(int position);
    }

    public HistoryAdapter(List<HistoryItem> historyItems,
                          DeleteListener deleteListener,
                          ReplyListener replyListener) {
        this.historyItems = historyItems;
        this.deleteListener = deleteListener;
        this.replyListener = replyListener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.history_item, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        try {
            HistoryItem item = historyItems.get(position);

            // Clean markdown tags
            String prompt = cleanMarkdown(item.getPrompt());
            String response = cleanMarkdown(item.getResponse());

            // Truncate for display
            if (prompt.length() > 100) {
                prompt = prompt.substring(0, 100) + "...";
            }
            if (response.length() > 150) {
                response = response.substring(0, 150) + "...";
            }

            holder.tvPrompt.setText(prompt);
            holder.tvResponse.setText(response);
            holder.tvModel.setText(item.getModel());

            // Format timestamp
            SimpleDateFormat sdf = new SimpleDateFormat("MMM dd, HH:mm", Locale.getDefault());
            holder.tvTimestamp.setText(sdf.format(new Date(item.getTimestamp())));

            // Set click listeners
            holder.btnDelete.setOnClickListener(v ->
                    deleteListener.onDelete(holder.getAdapterPosition()));

            holder.btnReply.setOnClickListener(v ->
                    replyListener.onReply(holder.getAdapterPosition()));

            holder.itemView.setOnClickListener(v ->
                    replyListener.onReply(holder.getAdapterPosition()));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public int getItemCount() {
        return historyItems.size();
    }

    public void updateData(List<HistoryItem> newItems) {
        historyItems = newItems;
        notifyDataSetChanged();
    }

    private String cleanMarkdown(String text) {
        if (text == null) return "";
        return text.replaceAll("(?m)^```(bash)?\\s*", "")
                   .replaceAll("(?m)^```\\s*", "")
                   .trim();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvPrompt, tvResponse, tvModel, tvTimestamp;
        ImageButton btnDelete, btnReply;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvPrompt = itemView.findViewById(R.id.tv_prompt);
            tvResponse = itemView.findViewById(R.id.tv_response);
            tvModel = itemView.findViewById(R.id.tv_model);
            tvTimestamp = itemView.findViewById(R.id.tv_timestamp);
            btnDelete = itemView.findViewById(R.id.btn_delete);
            btnReply = itemView.findViewById(R.id.btn_reply);
        }
    }
}
