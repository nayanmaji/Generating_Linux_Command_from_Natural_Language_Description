package com.example.aiassistant;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private TextInputEditText etPrompt, etResponse;
    private MaterialButton btnGenerate, btnClearHistory;
    private RequestQueue requestQueue;
    private HistoryAdapter historyAdapter;
    private List<HistoryItem> historyItems = new ArrayList<>();
    private static final int MAX_HISTORY = 15;

    private static final String OPENAI_API_KEY = "AIzaSyAkk2Z-tR_FVTo17K7mNsoilbODrmeMTCM";
    private static final String ANTHROPIC_API_KEY = "plsSkwhQ9GCkWsH4KEgtTE26Nk06EVZMyDOS5SRc";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initializeViews();
        setupRecyclerView();
        setupModelSpinner();
        setupRequestQueue();
        loadHistory();
        updateHistoryVisibility();
        setupEventListeners();
    }

    private void initializeViews() {
        etPrompt = findViewById(R.id.et_prompt);
        etResponse = findViewById(R.id.et_response);
        btnGenerate = findViewById(R.id.btn_generate);
        btnClearHistory = findViewById(R.id.btn_clear_history);
    }

    private void setupRecyclerView() {
        RecyclerView rvHistory = findViewById(R.id.rv_history);
        rvHistory.setLayoutManager(new LinearLayoutManager(this));
        historyAdapter = new HistoryAdapter(historyItems, this::deleteHistoryItem, this::replyToHistoryItem);
        rvHistory.setAdapter(historyAdapter);
    }

    private void setupModelSpinner() {
        AutoCompleteTextView modelSpinner = findViewById(R.id.model_spinner);
        String[] models = {"ChatGPT (GPT-4)", "Claude (Anthropic)", "Gemini (Google)"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_dropdown_item_1line, models);
        modelSpinner.setAdapter(adapter);
        modelSpinner.setText(models[0], false);
    }

    private void setupRequestQueue() {
        requestQueue = Volley.newRequestQueue(this);
    }

    private void setupEventListeners() {
        btnGenerate.setOnClickListener(v -> handleGenerate());
        btnClearHistory.setOnClickListener(v -> clearAllHistory());

        ImageButton btnCopy = findViewById(R.id.btn_copy);
        btnCopy.setOnClickListener(v -> copyResponseToClipboard());

        ImageButton btnShare = findViewById(R.id.btn_share);
        btnShare.setOnClickListener(v -> shareResponse());
    }

    private void handleGenerate() {
        String userPrompt = etPrompt.getText().toString().trim();
        String selectedModel = ((AutoCompleteTextView) findViewById(R.id.model_spinner)).getText().toString();

        if (userPrompt.isEmpty()) {
            showError("Please enter a prompt");
            return;
        }

        btnGenerate.setEnabled(false);
        btnGenerate.setText("Generating...");
        etResponse.setText("Thinking...");

        if (selectedModel.contains("ChatGPT")) {
            callOpenAI(userPrompt);
        } else if (selectedModel.contains("Claude")) {
            callAnthropicAPI(userPrompt);
        } else if (selectedModel.contains("Gemini")) {
            callGeminiAPI(userPrompt);
        }
    }

    private void callOpenAI(String prompt) {
        String url = "https://api.openai.com/v1/chat/completions";

        try {
            JSONObject requestBody = new JSONObject();
            requestBody.put("model", "gpt-4");
            requestBody.put("max_tokens", 500);
            requestBody.put("temperature", 0.7);

            JSONArray messages = new JSONArray();
            JSONObject systemMessage = new JSONObject();
            systemMessage.put("role", "system");
            systemMessage.put("content", "You are a helpful AI assistant. Provide clear, concise, and accurate responses.");
            messages.put(systemMessage);

            JSONObject userMessage = new JSONObject();
            userMessage.put("role", "user");
            userMessage.put("content", prompt);
            messages.put(userMessage);

            requestBody.put("messages", messages);

            JsonObjectRequest request = new JsonObjectRequest(
                    Request.Method.POST,
                    url,
                    requestBody,
                    response -> {
                        try {
                            JSONArray choices = response.getJSONArray("choices");
                            String result = choices.getJSONObject(0)
                                    .getJSONObject("message")
                                    .getString("content")
                                    .trim();

                            displayResponse(result);
                            saveToHistory(prompt, result, "ChatGPT");
                        } catch (JSONException e) {
                            handleAPIError("OpenAI response parsing error: " + e.getMessage());
                        }
                    },
                    error -> handleAPIError("OpenAI API error: " + getErrorMessage(error))
            ) {
                @Override
                public Map<String, String> getHeaders() {
                    Map<String, String> headers = new HashMap<>();
                    headers.put("Authorization", "Bearer " + OPENAI_API_KEY);
                    headers.put("Content-Type", "application/json");
                    return headers;
                }
            };

            requestQueue.add(request);
        } catch (JSONException e) {
            handleAPIError("Request creation error: " + e.getMessage());
        }
    }

    private void callAnthropicAPI(String prompt) {
        String url = "https://api.anthropic.com/v1/messages";

        try {
            JSONObject requestBody = new JSONObject();
            requestBody.put("model", "claude-3-sonnet-20240229");
            requestBody.put("max_tokens", 500);

            JSONArray messages = new JSONArray();
            JSONObject userMessage = new JSONObject();
            userMessage.put("role", "user");
            userMessage.put("content", prompt);
            messages.put(userMessage);

            requestBody.put("messages", messages);

            JsonObjectRequest request = new JsonObjectRequest(
                    Request.Method.POST,
                    url,
                    requestBody,
                    response -> {
                        try {
                            JSONArray content = response.getJSONArray("content");
                            String result = content.getJSONObject(0)
                                    .getString("text")
                                    .trim();

                            displayResponse(result);
                            saveToHistory(prompt, result, "Claude");
                        } catch (JSONException e) {
                            handleAPIError("Claude response parsing error: " + e.getMessage());
                        }
                    },
                    error -> handleAPIError("Claude API error: " + getErrorMessage(error))
            ) {
                @Override
                public Map<String, String> getHeaders() {
                    Map<String, String> headers = new HashMap<>();
                    headers.put("x-api-key", ANTHROPIC_API_KEY);
                    headers.put("Content-Type", "application/json");
                    headers.put("anthropic-version", "2023-06-01");
                    return headers;
                }
            };

            requestQueue.add(request);
        } catch (JSONException e) {
            handleAPIError("Request creation error: " + e.getMessage());
        }
    }

    private void callGeminiAPI(String prompt) {
        String url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + BuildConfig.GEMINI_API_KEY;

        String refinedPrompt = "Provide only Linux terminal commands for the following task. Use multiple lines if needed, with each command on a new line. Task: " + prompt;

        try {
            JSONObject requestBody = new JSONObject();
            JSONArray contentsArray = new JSONArray();
            JSONObject contentObject = new JSONObject();
            JSONArray partsArray = new JSONArray();

            JSONObject textPart = new JSONObject();
            textPart.put("text", refinedPrompt);
            partsArray.put(textPart);

            contentObject.put("parts", partsArray);
            contentsArray.put(contentObject);
            requestBody.put("contents", contentsArray);

            JSONObject generationConfig = new JSONObject();
            generationConfig.put("temperature", 0.7);
            generationConfig.put("maxOutputTokens", 500);
            requestBody.put("generationConfig", generationConfig);

            JsonObjectRequest request = new JsonObjectRequest(
                    Request.Method.POST,
                    url,
                    requestBody,
                    response -> {
                        try {
                            JSONArray candidates = response.getJSONArray("candidates");
                            String result = candidates.getJSONObject(0)
                                    .getJSONObject("content")
                                    .getJSONArray("parts")
                                    .getJSONObject(0)
                                    .getString("text")
                                    .trim();

                            displayResponse(result);
                            saveToHistory(prompt, result, "Gemini");
                        } catch (JSONException e) {
                            handleAPIError("Gemini response parsing error: " + e.getMessage());
                        }
                    },
                    error -> handleAPIError("Gemini API error: " + getErrorMessage(error))
            ) {
                @Override
                public Map<String, String> getHeaders() {
                    Map<String, String> headers = new HashMap<>();
                    headers.put("Content-Type", "application/json");
                    return headers;
                }
            };

            requestQueue.add(request);
        } catch (JSONException e) {
            handleAPIError("Request creation error: " + e.getMessage());
        }
    }

    private void displayResponse(String rawResponse) {
    String model = ((AutoCompleteTextView) findViewById(R.id.model_spinner)).getText().toString();
    String cleaned = cleanMarkdownTags(rawResponse);
    String output = model.contains("Gemini") ? extractCommandBlock(cleaned) : cleaned;
    etResponse.setText(output);
    resetGenerateButton();
}

private String cleanMarkdownTags(String response) {
    return response
            .replaceAll("(?m)^```(bash)?\\s*", "") 
            .replaceAll("(?m)^```\\s*", "")        
            .trim();
}


    private String extractCommandBlock(String response) {
        StringBuilder builder = new StringBuilder();
        for (String line : response.split("\n")) {
            line = line.trim();
            if (line.matches("^(touch|mkdir|cat|echo|nano|vim|cp|mv|rm|chmod|chown|sudo|cd|ls|pwd|grep|awk|sed|for|if|while|#|\\$).*")) {
                builder.append(line).append("\n");
            }
        }
        String result = builder.toString().trim();
        return result.isEmpty() ? response.trim() : result;
    }

    private void resetGenerateButton() {
        btnGenerate.setEnabled(true);
        btnGenerate.setText("Generate");
    }

    private void saveToHistory(String prompt, String response, String model) {
        if (historyItems.size() >= MAX_HISTORY) {
            historyItems.remove(historyItems.size() - 1);
        }
        historyItems.add(0, new HistoryItem(prompt, response, model));
        saveHistoryToPrefs();
        updateHistoryVisibility();
    }

    private void loadHistory() {
        String json = getPreferences(Context.MODE_PRIVATE).getString("ai_history", "");
        if (!json.isEmpty()) {
            try {
                historyItems = new Gson().fromJson(json, new TypeToken<ArrayList<HistoryItem>>(){}.getType());
                if (historyItems == null) historyItems = new ArrayList<>();
            } catch (Exception e) {
                Log.e("AI_ASSISTANT", "Error loading history", e);
                historyItems = new ArrayList<>();
            }
        }
        historyAdapter.updateData(historyItems);
    }

    private void saveHistoryToPrefs() {
        String json = new Gson().toJson(historyItems);
        getPreferences(Context.MODE_PRIVATE).edit().putString("ai_history", json).apply();
        historyAdapter.notifyDataSetChanged();
    }

    private void deleteHistoryItem(int position) {
        if (position >= 0 && position < historyItems.size()) {
            historyItems.remove(position);
            saveHistoryToPrefs();
            updateHistoryVisibility();
        }
    }

    private void replyToHistoryItem(int position) {
        if (position >= 0 && position < historyItems.size()) {
            HistoryItem item = historyItems.get(position);
            etPrompt.setText(item.getPrompt());
            etResponse.setText(item.getResponse());
        }
    }

    private void clearAllHistory() {
        historyItems.clear();
        saveHistoryToPrefs();
        updateHistoryVisibility();
        Toast.makeText(this, "History cleared", Toast.LENGTH_SHORT).show();
    }

    private void updateHistoryVisibility() {
        findViewById(R.id.rv_history).setVisibility(historyItems.isEmpty() ? View.GONE : View.VISIBLE);
        findViewById(R.id.tv_empty_history).setVisibility(historyItems.isEmpty() ? View.VISIBLE : View.GONE);
    }

    private void copyResponseToClipboard() {
        String response = etResponse.getText().toString();
        if (!response.isEmpty()) {
            ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            ClipData clip = ClipData.newPlainText("AI Response", response);
            clipboard.setPrimaryClip(clip);
            Toast.makeText(this, "Response copied to clipboard", Toast.LENGTH_SHORT).show();
        }
    }

    private void shareResponse() {
        String response = etResponse.getText().toString();
        if (!response.isEmpty()) {
            Intent shareIntent = new Intent(Intent.ACTION_SEND);
            shareIntent.setType("text/plain");
            shareIntent.putExtra(Intent.EXTRA_TEXT, response);
            startActivity(Intent.createChooser(shareIntent, "Share AI Response"));
        }
    }

    private void handleAPIError(String message) {
        Log.e("AI_ASSISTANT", message);
        showError(message);
        etResponse.setText("Error: " + message);
        resetGenerateButton();
    }

    private void showError(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    private String getErrorMessage(com.android.volley.VolleyError error) {
        if (error.networkResponse != null && error.networkResponse.data != null) {
            try {
                return "Status: " + error.networkResponse.statusCode +
                        ", Body: " + new String(error.networkResponse.data, "utf-8");
            } catch (UnsupportedEncodingException e) {
                return "Failed to parse error response";
            }
        }
        return error.getMessage() != null ? error.getMessage() : "Unknown network error";
    }
}
