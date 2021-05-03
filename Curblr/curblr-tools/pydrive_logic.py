from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
#https://pypi.org/project/PyDrive/

class GdriveManagement:
    def __init__(self):
        self.get_google_drive_auth()
    def get_google_drive_auth(self):
        """Initilaizes the Google drive 'drive' object. """
        gauth = GoogleAuth()

        # Try to load saved client credentials
        gauth.LoadCredentialsFile("/client_secrets.json")

        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.GetFlow()
            gauth.flow.params.update({'access_type': 'offline'})
            gauth.flow.params.update({'approval_prompt': 'force'})
            gauth.LocalWebserverAuth()

        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()

        # Save the current credentials to a file
        gauth.SaveCredentialsFile("path/to/your/credentials/file")  

        self.drive = GoogleDrive(gauth)
        
    def upload_file_to_drive(self, file_id, local_path):
        """Overwrites the existing Google drive file."""
        update_file = self.drive.CreateFile({'id': file_id})
        update_file.SetContentFile(local_path)
        update_file.Upload()
        
    def download_drive_file(self,file_id, save_path):
        """Downloads an existing Google drive file."""
        download_file = self.drive.CreateFile({'id': file_id})
        download_file.GetContentFile(save_path)  # Save Drive file as a local file
    
    def UploadMapFile(self, content):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        drive = GoogleDrive(gauth)

        
        file1 = drive.CreateFile({'id': "last_map_filtred", 'title': 'last_map_filtred.geojson', 'mimeType':'application/json'})
        file1.SetContentString(json.dumps(content))
        file1.Upload() # Files.insert()
        
        # file1['title'] = 'HelloWorld.txt'  # Change title of the file
        # file1.Upload() # Files.patch()

        # content = file1.GetContentString()  # 'Hello'
        # file1.SetContentString(content+' World!')  # 'Hello World!'
        # file1.Upload() # Files.update()

        # file2 = drive.CreateFile()
        # file2.SetContentFile('hello.png')
        # file2.Upload()
        # print('Created file %s with mimeType %s' % (file2['title'],
        # file2['mimeType']))
        # Created file hello.png with mimeType image/png

        # file3 = drive.CreateFile({'id': file2['id']})
        # print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
        # file3.GetContentFile('world.png')  # Save Drive file as a local file

        # or download Google Docs files in an export format provided.
        # downloading a docs document as an html file:
        # docsfile.GetContentFile('test.html', mimetype='text/html')
def UploadMapFile(content):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)
    
    # file0 = drive.CreateFile({'title': 'last_map_filtred.geojson', 'mimeType':'application/json'})
    # file0.SetContentString(json.dumps(content))
    # file0.Upload()

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    
    if len(file_list)>0:
        for file_t in file_list:
            print('title: %s, id: %s' % (file_t['title'], file_t['id']))
            if file_t['title'] == "last_map_filtred.geojson":
                print("ok")
                file1 = drive.CreateFile({'id': file_t['id']})
                file1.SetContentString(json.dumps(content))
                file1.Upload() # Files.insert()
                break
            else:
                file1 = drive.CreateFile({'title': 'last_map_filtred.geojson', 'mimeType':'application/json'})
                file1.SetContentString(json.dumps(content))
                file1.Upload()
    else:
        file1 = drive.CreateFile({'title': 'last_map_filtred.geojson', 'mimeType':'application/json'})
        file1.SetContentString(json.dumps(content))
        file1.Upload()