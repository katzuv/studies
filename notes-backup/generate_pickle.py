"""
Generate token.pickle from credentials.json.

This script creates a pickle file from OAuth credentials for use with Google Drive API.
Run this once to set up authentication.
"""

import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes define what access the app has
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def generate_pickle_from_credentials(credentials_path: Path = Path('credentials.json'),
                                     output_path: Path = Path('token.pickle')):
    """
    Generate token.pickle from credentials.json.
    
    @param credentials_path: Path to the downloaded credentials.json file.
    @param output_path: Path where token.pickle will be saved.
    """
    if not credentials_path.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
    
    # Start the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials for future use
    output_path.write_bytes(pickle.dumps(creds))
    print(f"✓ Successfully created {output_path}")
    print(f"✓ You can now use this token.pickle file for authentication")


if __name__ == '__main__':
    generate_pickle_from_credentials()
