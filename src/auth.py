import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

# Define the scopes required for the application
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = "client_secrets.json"
CREDENTIALS_FILE = "youtube_credentials.json"

def get_authenticated_service(scopes=SCOPES):
    credentials = None
    # Check if credentials file exists
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as token:
            credentials = Credentials.from_authorized_user_info(json.load(token), scopes)

    # If there are no valid credentials, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(credentials.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)