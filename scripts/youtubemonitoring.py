# youtube api v3 api key: AIzaSyACF-RzZH4ZXsQw8GhT29sErYZZt7fYCXs
# pip install --upgrade google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2

# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google.auth.transport.requests import Request
# from google.oauth2.service_account import Credentials

# # replace these with your actual credentials
# KEY_FILE_PATH = 'path/to/your/service-account-file.json'
# DEVELOPER_KEY = 'YOUR_DEVELOPER_KEY'
# YOUTUBE_API_SERVICE_NAME = 'youtube'
# YOUTUBE_API_VERSION = 'v3'

# def get_stream_health(youtube, broadcast_id):
#     """
#     Function to fetch stream health from YouTube API.
#     """
#     broadcast_status = youtube.liveBroadcasts().list(
#         part='status',
#         id=broadcast_id
#     ).execute()

#     return broadcast_status['items'][0]['status']['lifeCycleStatus']

# def youtube_stream_health():
#     """
#     Function to build the service and fetch stream health.
#     """
#     credentials = Credentials.from_service_account_file(
#         KEY_FILE_PATH, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
#     )

#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

#     try:
#         broadcast_id = 'YOUR_BROADCAST_ID'
#         print("Stream Health: %s" % get_stream_health(youtube, broadcast_id))
#     except HttpError as e:
#         print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

# if __name__ == "__main__":
#     youtube_stream_health()


# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveStreams.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/home/pi/Desktop/ColinsLivestreamRewriteStarted062623/client_secret_993425110504-nr8fhtpievmrld10kv5bfj7dnu36j1op.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.liveStreams().list(
        part="snippet,cdn,contentDetails,status",
        mine=True
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()