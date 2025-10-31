"""
Main script for Notes Backup and PDF Merger
Orchestrates downloading from Google Drive, merging PDFs, and uploading results
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from drive_handler import DriveHandler, download_course_files
from pdf_merger import merge_course_pdfs


def load_config(config_path: Path) -> dict:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def process_course(drive: DriveHandler, course_name: str, 
                  course_folder_id: str, temp_dir: Path, 
                  merged_folder_id: str) -> dict:
    """
    Process a single course: download, merge, and upload
    
    Args:
        drive: DriveHandler instance
        course_name: Name of the course
        course_folder_id: Google Drive folder ID for the course
        temp_dir: Temporary directory for downloads
        merged_folder_id: Google Drive folder ID for merged PDFs
        
    Returns:
        Dictionary with processing results
    """
    temp_dir = Path(temp_dir)
    print(f"\n{'='*60}")
    print(f"Processing: {course_name}")
    print(f"{'='*60}")
    
    results = {
        'course': course_name,
        'status': 'success',
        'files_created': [],
        'errors': []
    }
    
    try:
        # Download course files
        print(f"\n[1/3] Downloading files for {course_name}...")
        download_paths = download_course_files(
            drive, course_name, course_folder_id, temp_dir
        )
        
        if not download_paths:
            results['status'] = 'skipped'
            results['errors'].append('No files found to download')
            return results
        
        # Merge PDFs
        print(f"\n[2/3] Merging PDFs for {course_name}...")
        merged_dir = temp_dir / f"{course_name}_merged"
        merged_dir.mkdir(parents=True, exist_ok=True)
        
        lectures_folder = download_paths.get('lectures', Path())
        tirgul_folder = download_paths.get('tirgul', Path())
        
        merged_files = merge_course_pdfs(
            lectures_folder, tirgul_folder, merged_dir, course_name
        )
        
        # Upload merged files
        print(f"\n[3/3] Uploading merged files for {course_name}...")
        for file_type, file_path in merged_files.items():
            if file_path.exists():
                try:
                    file_id = drive.upload_file(file_path, merged_folder_id)
                    results['files_created'].append({
                        'type': file_type,
                        'name': file_path.name,
                        'id': file_id
                    })
                except Exception as e:
                    error_msg = f"Failed to upload {file_type}: {e}"
                    print(f"Error: {error_msg}")
                    results['errors'].append(error_msg)
        
        if results['errors']:
            results['status'] = 'partial'
        
    except Exception as e:
        results['status'] = 'failed'
        results['errors'].append(str(e))
        print(f"Error processing {course_name}: {e}")
    
    return results


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Notes Backup and PDF Merger'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--credentials',
        default='credentials.json',
        help='Path to Google service account credentials'
    )
    parser.add_argument(
        '--token',
        help='Path to OAuth token file (alternative to credentials)'
    )
    parser.add_argument(
        '--temp-dir',
        default='./temp',
        help='Temporary directory for downloads'
    )
    parser.add_argument(
        '--course',
        help='Process only specific course (optional)'
    )
    
    args = parser.parse_args()
    
    # Convert paths to Path objects
    config_path = Path(args.config)
    credentials_path = Path(args.credentials)
    token_path = Path(args.token) if args.token else None
    temp_dir = Path(args.temp_dir)
    
    # Load configuration
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        print("Please create a config.json file. See config.example.json")
        return 1
    
    config = load_config(config_path)
    
    # Initialize Drive handler
    try:
        drive = DriveHandler(
            credentials_path=credentials_path if credentials_path.exists() else None,
            token_path=token_path
        )
    except Exception as e:
        print(f"Error: Failed to authenticate with Google Drive: {e}")
        return 1
    
    # Get or create merged folder
    merged_folder_name = config.get('merged_folder_name', 'Merged_Notes')
    merged_folder_id = drive.get_or_create_folder(merged_folder_name)
    
    # Process courses
    courses = config.get('courses', {})
    
    if args.course:
        # Process single course
        if args.course not in courses:
            print(f"Error: Course '{args.course}' not found in config")
            return 1
        courses = {args.course: courses[args.course]}
    
    all_results = []
    
    print(f"\nProcessing {len(courses)} course(s)...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    for course_name, course_folder_id in courses.items():
        result = process_course(
            drive, course_name, course_folder_id, 
            temp_dir, merged_folder_id
        )
        all_results.append(result)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for r in all_results if r['status'] == 'success')
    partial = sum(1 for r in all_results if r['status'] == 'partial')
    failed = sum(1 for r in all_results if r['status'] == 'failed')
    skipped = sum(1 for r in all_results if r['status'] == 'skipped')
    
    print(f"Total courses: {len(all_results)}")
    print(f"Successful: {successful}")
    print(f"Partial: {partial}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    
    total_files = sum(len(r['files_created']) for r in all_results)
    print(f"\nTotal files created: {total_files}")
    
    # Print detailed results
    for result in all_results:
        if result['status'] == 'success':
            print(f"\n✓ {result['course']}: {len(result['files_created'])} files")
        elif result['status'] == 'partial':
            print(f"\n⚠ {result['course']}: {len(result['files_created'])} files, {len(result['errors'])} errors")
        elif result['status'] == 'failed':
            print(f"\n✗ {result['course']}: Failed")
            for error in result['errors']:
                print(f"  - {error}")
        else:
            print(f"\n○ {result['course']}: Skipped")
    
    print(f"\nMerged folder ID: {merged_folder_id}")
    print(f"Merged folder URL: https://drive.google.com/drive/folders/{merged_folder_id}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
