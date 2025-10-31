"""
Google Drive Handler
Handles authentication and file operations with Google Drive API
"""

import io
import json
from pathlib import Path
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.auth.transport.requests import Request


class DriveHandler:
    """Handles Google Drive API operations"""
    
    def __init__(self, credentials_path: Path = None, token_path: Path = None):
        """
        Initialize Drive Handler
        
        Args:
            credentials_path: Path to service account credentials JSON
            token_path: Path to OAuth token JSON (alternative to service account)
        """
        self.service = None
        self.credentials_path = Path(credentials_path) if credentials_path else None
        self.token_path = Path(token_path) if token_path else None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Try service account first
        if self.credentials_path and self.credentials_path.exists():
            creds = service_account.Credentials.from_service_account_file(
                str(self.credentials_path),
                scopes=['https://www.googleapis.com/auth/drive']
            )
        # Try OAuth token
        elif self.token_path and self.token_path.exists():
            with open(self.token_path, 'r') as token:
                token_data = json.load(token)
                creds = Credentials.from_authorized_user_info(token_data)
            
            # Refresh if expired
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
        if not creds:
            raise ValueError(
                "No valid credentials found. Please provide either "
                "credentials_path or token_path"
            )
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def find_folder(self, folder_name: str, parent_id: str = None) -> Optional[str]:
        """
        Find a folder by name
        
        Args:
            folder_name: Name of the folder to find
            parent_id: ID of parent folder (optional)
            
        Returns:
            Folder ID if found, None otherwise
        """
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        items = results.get('files', [])
        return items[0]['id'] if items else None
    
    def list_pdfs_in_folder(self, folder_id: str) -> List[Dict[str, str]]:
        """
        List all PDF files in a folder
        
        Args:
            folder_id: ID of the folder
            
        Returns:
            List of dictionaries with file info (id, name)
        """
        query = f"'{folder_id}' in parents and mimeType='application/pdf'"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, modifiedTime)',
            orderBy='name'
        ).execute()
        
        return results.get('files', [])
    
    def download_file(self, file_id: str, destination: Path) -> Path:
        """
        Download a file from Google Drive
        
        Args:
            file_id: ID of the file to download
            destination: Local path to save the file
            
        Returns:
            Path to the downloaded file
        """
        destination = Path(destination)
        request = self.service.files().get_media(fileId=file_id)
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        with io.FileIO(str(destination), 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download progress: {int(status.progress() * 100)}%")
        
        return destination
    
    def download_folder_pdfs(self, folder_id: str, destination_folder: Path) -> List[Path]:
        """
        Download all PDFs from a folder
        
        Args:
            folder_id: ID of the Google Drive folder
            destination_folder: Local folder to save files
            
        Returns:
            List of paths to downloaded files
        """
        destination_folder = Path(destination_folder)
        pdfs = self.list_pdfs_in_folder(folder_id)
        downloaded = []
        
        for pdf in pdfs:
            local_path = destination_folder / pdf['name']
            try:
                self.download_file(pdf['id'], local_path)
                downloaded.append(local_path)
                print(f"Downloaded: {pdf['name']}")
            except Exception as e:
                print(f"Error downloading {pdf['name']}: {e}")
        
        return downloaded
    
    def upload_file(self, file_path: Path, folder_id: str = None, 
                   file_name: str = None) -> str:
        """
        Upload a file to Google Drive
        
        Args:
            file_path: Local path of file to upload
            folder_id: ID of destination folder (optional)
            file_name: Name for the file in Drive (optional, uses local name)
            
        Returns:
            ID of the uploaded file
        """
        file_path = Path(file_path)
        if not file_name:
            file_name = file_path.name
        
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(str(file_path), resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"Uploaded: {file_name} (ID: {file.get('id')})")
        return file.get('id')
    
    def create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """
        Create a folder in Google Drive
        
        Args:
            folder_name: Name of the folder to create
            parent_id: ID of parent folder (optional)
            
        Returns:
            ID of the created folder
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        print(f"Created folder: {folder_name} (ID: {folder.get('id')})")
        return folder.get('id')
    
    def get_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """
        Get folder ID or create if it doesn't exist
        
        Args:
            folder_name: Name of the folder
            parent_id: ID of parent folder (optional)
            
        Returns:
            Folder ID
        """
        folder_id = self.find_folder(folder_name, parent_id)
        if not folder_id:
            folder_id = self.create_folder(folder_name, parent_id)
        return folder_id


def download_course_files(drive: DriveHandler, course_name: str, 
                         course_folder_id: str, local_base: Path) -> Dict[str, Path]:
    """
    Download all course files (lectures and tirgul)
    
    Args:
        drive: DriveHandler instance
        course_name: Name of the course
        course_folder_id: ID of the course folder in Drive
        local_base: Base local directory for downloads
        
    Returns:
        Dictionary with paths to downloaded folders
    """
    local_base = Path(local_base)
    results = {}
    
    # Create local course folder
    course_local = local_base / course_name
    course_local.mkdir(parents=True, exist_ok=True)
    
    # Download Lectures
    lectures_id = drive.find_folder("Lectures", course_folder_id)
    if lectures_id:
        lectures_local = course_local / "Lectures"
        lectures_local.mkdir(parents=True, exist_ok=True)
        drive.download_folder_pdfs(lectures_id, lectures_local)
        results['lectures'] = lectures_local
    
    # Download Tirgul
    tirgul_id = drive.find_folder("Tirgul", course_folder_id)
    if tirgul_id:
        tirgul_local = course_local / "Tirgul"
        tirgul_local.mkdir(parents=True, exist_ok=True)
        drive.download_folder_pdfs(tirgul_id, tirgul_local)
        results['tirgul'] = tirgul_local
    
    return results


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python drive_handler.py <credentials_path> <folder_id> [output_dir]")
        sys.exit(1)
    
    creds_path = sys.argv[1]
    folder_id = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./downloads"
    
    drive = DriveHandler(credentials_path=creds_path)
    pdfs = drive.download_folder_pdfs(folder_id, output_dir)
    print(f"\nDownloaded {len(pdfs)} files to {output_dir}")
