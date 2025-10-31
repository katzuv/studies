# Notes Backup and PDF Merger

Automatically collect lecture PDFs for university courses from Google Drive, merge them with clickable table of contents, and upload the results back to Drive.

## Features

- **Automated PDF Collection**: Downloads PDFs from Google Drive course folders
- **Smart Merging**: Combines PDFs with proper ordering (Lecture_01, Lecture_02, etc.)
- **Clickable TOC**: Generates table of contents visible in PDF sidebar
- **TOC Page**: Adds a clickable TOC page at the beginning of merged PDFs
- **Multiple Output Files**: Creates separate files for Lectures, Tirgul, and Full course
- **GitHub Actions Integration**: Runs automatically on schedule or manual trigger
- **Flexible Authentication**: Supports both service accounts and OAuth tokens

## Folder Structure

Each course in Google Drive should follow this structure:

```
Course_Name/
├── Lecture_01.pdf
├── Lecture_02.pdf
├── Tirgul_01.pdf
├── Tirgul_02.pdf
└── ...
```

## Setup

### 1. Install Dependencies

```bash
cd notes-backup
pip install -r requirements.txt
```

### 2. Google Drive Authentication

#### Option A: Service Account (Recommended for GitHub Actions)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create a Service Account
5. Download the JSON credentials file
6. Share your Google Drive folders with the service account email

#### Option B: OAuth Token

1. Create OAuth credentials in Google Cloud Console
2. Generate and save the token JSON file

### 3. Configuration

Create `config.json` based on `config.example.json`:

```json
{
  "merged_folder_name": "Merged_Notes",
  "courses": {
    "Linear_Algebra": "your-folder-id-here",
    "Calculus_1": "your-folder-id-here"
  }
}
```

To find a folder ID:
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the ID after `/folders/`

## Usage

### Run Locally

```bash
python main.py --credentials credentials.json
```

### Options

```bash
python main.py --help

Options:
  --config CONFIG           Path to config file (default: config.json)
  --credentials CREDS       Path to service account credentials
  --token TOKEN            Path to OAuth token (alternative)
  --temp-dir DIR           Temporary directory (default: ./temp)
  --course COURSE          Process only specific course
```

### Process Single Course

```bash
python main.py --credentials credentials.json --course "Linear_Algebra"
```

## GitHub Actions Setup

### 1. Add Secrets

In your GitHub repository, go to Settings → Secrets → Actions and add:

- `GOOGLE_CREDENTIALS`: Content of your service account JSON file
- `DRIVE_CONFIG`: Content of your config.json file

### 2. Workflow Configuration

The workflow is located at `.github/workflows/merge-notes.yml`

**Automatic Schedule**: Runs daily at 2 AM UTC

**Manual Trigger**:
1. Go to Actions tab in GitHub
2. Select "Merge Course Notes" workflow
3. Click "Run workflow"
4. Optionally specify a course name

## Output

The script creates three types of merged PDFs for each course:

1. **`CourseName_Lectures.pdf`**: All lecture PDFs merged
2. **`CourseName_Tirgul.pdf`**: All tirgul PDFs merged
3. **`CourseName_Full.pdf`**: All lectures + tirgul PDFs merged

Each PDF includes:
- Clickable table of contents in the PDF sidebar
- Visual TOC page at the beginning with clickable links
- Properly ordered sections

## Architecture

### Components

- **`main.py`**: Main orchestrator script
- **`drive_handler.py`**: Google Drive API operations
- **`pdf_merger.py`**: PDF merging and TOC generation
- **`config.json`**: Course folder mappings
- **`credentials.json`**: Google service account credentials (not committed)

### Flow

1. Authenticate with Google Drive API
2. For each course in config:
   - Download PDFs from Lectures and Tirgul folders
   - Merge PDFs with TOC generation
   - Upload merged files to "Merged_Notes" folder
3. Generate summary report

## Technologies

- **Python 3.11+**
- **PyMuPDF (fitz)**: PDF manipulation and TOC generation
- **pikepdf**: Additional PDF operations
- **google-api-python-client**: Google Drive API access
- **pathlib**: Modern path handling

## Troubleshooting

### Authentication Errors

- Verify credentials file is valid JSON
- Check that service account has access to folders
- Ensure Google Drive API is enabled in Google Cloud Console

### Download Issues

- Verify folder IDs in config.json are correct
- Check folder structure matches expected format
- Ensure PDFs are actually in the folders

### Merge Failures

- Check that downloaded PDFs are valid
- Verify sufficient disk space for temporary files
- Look for specific error messages in logs

## License

This project is part of the studies repository.

## Contributing

Feel free to open issues or submit pull requests for improvements.
