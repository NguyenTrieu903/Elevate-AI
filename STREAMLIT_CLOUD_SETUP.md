# Streamlit Cloud Setup Guide

## Configuring Secrets for Streamlit Cloud

Since Streamlit Cloud doesn't use `.env` files, you need to configure your Azure OpenAI credentials through Streamlit Cloud Secrets.

### Steps:

1. **Go to Streamlit Cloud Dashboard**
   - Navigate to https://share.streamlit.io/
   - Select your app

2. **Open Settings → Secrets**
   - Click on the three dots (⋮) next to your app
   - Select "Settings"
   - Click on "Secrets" in the left sidebar

3. **Add Your Secrets**
   - Paste the following TOML format configuration:

```toml
AZURE_OPENAI_LLM_ENDPOINT = "https://aiportalapi.stu-platform.live/jpe"
AZURE_OPENAI_LLM_API_KEY = "sk-SbfZQ8AZaO4VZBTT_Sev6A"
AZURE_OPENAI_LLM_MODEL = "GPT-4o-mini"
AZURE_OPENAI_LLM_API_VERSION = "2024-02-15-preview"

AZURE_OPENAI_EMBEDDING_ENDPOINT = "https://aiportalapi.stu-platform.live/jpe"
AZURE_OPENAI_EMBEDDING_API_KEY = "sk-I-qXbNTFH5Q2RA8dSnIOpQ"
AZURE_OPENAI_EMBED_MODEL = "text-embedding-3-small"
AZURE_OPENAI_EMBEDDING_API_VERSION = "2024-02-15-preview"
```

4. **Save and Redeploy**
   - Click "Save"
   - Your app will automatically redeploy with the new secrets

### Important Notes:

- **Never commit your API keys to Git** - They are securely stored in Streamlit Cloud Secrets
- The `.env` file is for local development only
- Secrets are encrypted and only accessible to your app
- After saving secrets, Streamlit Cloud will automatically restart your app

### Troubleshooting:

If you still see credential errors:
1. Verify all secrets are correctly pasted (no extra spaces or quotes)
2. Check that the API keys are valid and active
3. Ensure the endpoint URLs are correct
4. Try manually restarting the app from the Streamlit Cloud dashboard

