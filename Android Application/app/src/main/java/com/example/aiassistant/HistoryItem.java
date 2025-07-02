package com.example.aiassistant;

public class HistoryItem {
    private String prompt;
    private String response;
    private String model;
    private long timestamp;

    public HistoryItem(String prompt, String response, String model) {
        this.prompt = prompt;
        this.response = response;
        this.model = model;
        this.timestamp = System.currentTimeMillis();
    }

    // Constructor with timestamp (for loading from storage)
    public HistoryItem(String prompt, String response, String model, long timestamp) {
        this.prompt = prompt;
        this.response = response;
        this.model = model;
        this.timestamp = timestamp;
    }

    // Getters
    public String getPrompt() { 
        return prompt; 
    }
    
    public String getResponse() { 
        return response; 
    }
    
    public String getModel() { 
        return model; 
    }
    
    public long getTimestamp() { 
        return timestamp; 
    }

    // Setters (if needed)
    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }

    public void setResponse(String response) {
        this.response = response;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "HistoryItem{" +
                "prompt='" + prompt + '\'' +
                ", response='" + response + '\'' +
                ", model='" + model + '\'' +
                ", timestamp=" + timestamp +
                '}';
    }
}