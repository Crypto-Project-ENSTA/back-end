# ============================================================
# RUN THIS SCRIPT ONLY ONCE LOCALLY TO GET YOUR GMAIL TOKENS
# After running, copy the printed values to your .env file
# Then never run this again — the refresh token doesn't expire
# ============================================================

# from google_auth_oauthlib.flow import InstalledAppFlow

# SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
# creds = flow.run_local_server(port=0)

# print("GMAIL_TOKEN=" + creds.token)
# print("GMAIL_REFRESH_TOKEN=" + creds.refresh_token)
# print("GMAIL_CLIENT_ID=" + creds.client_id)
# print("GMAIL_CLIENT_SECRET=" + creds.client_secret)