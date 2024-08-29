import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
import dropbox as dbox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv(override=True)


def get_calendar_service():

    # Setup the Calendar API
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("tokenCALENDARSHIFT.json")
    creds = store.get()
    if not creds or creds.invalid:
        # if you want to put cred json in a different directory you have to include the whole address here
        flow = client.flow_from_clientsecrets(
            r"C:\RC Dropbox\Rivers Cuomo\Apps\credentials\credentialsCALENDARSHIFT.json",
            SCOPES,
        )
        creds = tools.run_flow(flow, store)
    service = build("calendar", "v3", http=creds.authorize(Http()))
    
    # Recurring Events calendar
    calendarId = "hre6is7vlqbig9hrhceo8esg44@group.calendar.google.com"

    return service, calendarId


def get_dropbox_service():
    print("get_dropbox_service...")
    dropbox_access_token = os.environ['DROPBOX_ACCESS_TOKEN']
    dropbox = dbox.Dropbox(dropbox_access_token)
    print(dropbox)
    try:
        dropbox.users_get_current_account()

    except dbox.exceptions.AuthError as e:
        # throw an error if the access token is invalid
        print("ERROR: Invalid access token for dropbox api; try re-generating an "
        "access token from the app console on the web.")
        raise e
    return dropbox


def get_firestore_client(credential_path, project_id):

    current_clients = firebase_admin._apps

    # get all the project_ids from current_clients
    current_project_ids = [x.project_id for x in current_clients.values()]

    # Initialize the Firebase app once
    if project_id not in current_project_ids:

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

        # Use the application default credentials
        cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(
            cred,
            {
                "projectId": project_id,
            },
            name=project_id,
        )

        firestore_client = firestore.client( app=firebase_admin.get_app(project_id) )

        print(f'firestore_client {firestore_client}')
        return firestore_client


def get_google_docs_service(credpath=rF"{os.environ['DROPBOX_HOME']}\Apps\credentials\gtoken.json"):
    print("get_google_docs_service...", end="")
    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/drive"
    store = file.Storage(
        credpath)
    creds = store.get()
    service = build("docs", "v1", http=creds.authorize(Http()))
    print("success!")

    return service


def get_google_drive_service(GOOGLE_DRIVE_CREDS_PATH):
    print("get_google_drive_service...", end="")
    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/drive"
    # GOOGLE_DRIVE_CREDS_PATH = os.getenv("GOOGLE_DRIVE_CREDS_PATH")
    print(GOOGLE_DRIVE_CREDS_PATH)
    try:
        store = file.Storage(GOOGLE_DRIVE_CREDS_PATH)
        creds = store.get()
        # creds = None
        # if not creds or creds.invalid:
        #     print('creds not valid')
        #     # exit()
        #     flow = client.flow_from_clientsecrets(
        #         r'C:\RC Dropbox\Rivers Cuomo\Apps\credentials\client_secret_980949712356-egfklf3potcuv1l7cg3tos91pdfo075g.apps.googleusercontent.com.json', SCOPES)
        #     creds = tools.run_flow(flow, store)

        drive_service = build("drive", "v3", http=creds.authorize(Http()))
        print("success!")
        return drive_service

    except Exception as e:
        print("ERROR: ", e)
        print(GOOGLE_DRIVE_CREDS_PATH)
        print(GOOGLE_DRIVE_CREDS_PATH=="C:\RC Dropbox\Rivers Cuomo\Apps\credentials\gtoken.json")


    return drive_service


def get_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # redirect_uri must exactly match the redirect uri in the Spotify Developer Dashboard
    # https://developer.spotify.com/dashboard/347f6f6f7ac74e6d976002ca8a81375a/settings
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI") or 'http://localhost:8080'
    scope = 'playlist-modify-public playlist-modify-private'
    
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     scope=scope))

def main():
    # get_google_docs_service()
    # get_google_drive_service()
    # get_calendar_service()
    # client = get_spotify_client()
    # PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

    credential_path = os.environ["FIRESTORE_CREDENTIALS_PATH"]
    project_id = os.environ["FIRESTORE_PROJECT_ID"]
    get_firestore_client(credential_path, project_id)

    credential_path = (
    rf"{os.environ['BOXIFY_HOME']}\secrets\rivers-private-f88a05678815.json"    )
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
    project_id = "rivers-private"
    get_firestore_client(os.environ["FIRESTORE_CREDENTIALS_PATH"], project_id)

    credential_path = os.environ["FIRESTORE_CREDENTIALS_PATH"]
    project_id = os.environ["FIRESTORE_PROJECT_ID"]
    get_firestore_client(credential_path, project_id)

    print('alsdkfj')



if __name__ == "__main__":
    main()