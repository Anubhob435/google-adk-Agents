import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE = 'token.pickle'

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files(service, page_size=10):
    results = service.files().list(pageSize=page_size, fields="files(id, name)").execute()
    items = results.get('files', [])
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")
    return items

def upload_file(service, file_path, mime_type):
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID:', file.get('id'))
    return file.get('id')

def download_file(service, file_id, destination):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    print('Downloaded to', destination)

def create_folder(service, folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print('Folder ID:', file.get('id'))
    return file.get('id')

def delete_file(service, file_id):
    service.files().delete(fileId=file_id).execute()
    print('Deleted file:', file_id)

def main():
    service = get_drive_service()
    print('Google Drive API Operations:')
    list_files(service)
    # Upload the drive-api-documentaion.json file
    doc_path = 'drive-api-documentaion.json'
    if os.path.exists(doc_path):
        file_id = upload_file(service, doc_path, 'application/json')
        print(f'Uploaded drive-api-documentaion.json with file ID: {file_id}')
    else:
        print('drive-api-documentaion.json not found!')
    # Example usage:
    folder_id = create_folder(service, 'TestFolder')
    # file_id = upload_file(service, 'test.txt', 'text/plain')
    # download_file(service, file_id, 'downloaded_test.txt')
    # delete_file(service, file_id)

if __name__ == "__main__":
    main()
