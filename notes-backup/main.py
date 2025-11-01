"""
Main script for Notes Backup and PDF Merger.
Orchestrates downloading from Google Drive, merging PDFs, and uploading results.
"""

import argparse
import collections
import json
from datetime import datetime
from pathlib import Path

from drive_handler import DriveHandler, download_course_files
from pdf_merger import merge_course_pdfs


def process_course(
    drive: DriveHandler,
    course_name: str,
    course_folder_id: str,
    temp_dir: Path,
    semester_folder_id: str,
) -> dict:
    """
    Process a single course: download, merge, and upload.

    @param drive: DriveHandler instance.
    @param course_name: Name of the course.
    @param course_folder_id: Google Drive folder ID for the course.
    @param temp_dir: Temporary directory for downloads.
    @param parent_merged_folder_id: Google Drive folder ID for parent merged PDFs folder.
    @return: Dictionary with processing results.
    """
    temp_dir = Path(temp_dir)
    print(f"\n{'=' * 60}")
    print(f"Processing: {course_name}")
    print(f"{'=' * 60}")

    results = {
        "course": course_name,
        "status": "success",
        "files_created": [],
        "errors": [],
    }

    try:
        # Download course files
        print(f"\n[1/3] Downloading files for {course_name}...")
        file_lists = download_course_files(
            drive, course_name, course_folder_id, temp_dir
        )

        if not file_lists["lectures"] and not file_lists["tirgul"]:
            results["status"] = "skipped"
            results["errors"].append("No files found to download")
            return results

        # Merge PDFs
        print(f"\n[2/3] Merging PDFs for {course_name}...")
        course_output_dir = temp_dir / f"{course_name}_merged"
        parent_output_dir = temp_dir / "all_courses_merged"

        merged_files = merge_course_pdfs(
            file_lists["lectures"],
            file_lists["tirgul"],
            course_output_dir,
            parent_output_dir,
            course_name,
        )

        # Upload merged files
        print(f"\n[3/3] Uploading merged files for {course_name}...")

        # Upload course-specific files to the course folder
        course_merged_folder_id = drive.get_or_create_folder("Merged", course_folder_id)
        for file_path in merged_files["course"]:
            if file_path.exists():
                try:
                    file_id = drive.upload_file(file_path, course_merged_folder_id)
                    results["files_created"].append(
                        {"location": "course", "name": file_path.name, "id": file_id}
                    )
                except Exception as e:
                    error_msg = (
                        f"Failed to upload {file_path.name} to course folder: {e}"
                    )
                    print(f"Error: {error_msg}")
                    results["errors"].append(error_msg)

        # Upload parent files to the parent merged folder
        for file_path in merged_files["parent"]:
            if file_path.exists():
                try:
                    file_id = drive.upload_file(file_path, semester_folder_id)
                    results["files_created"].append(
                        {"location": "parent", "name": file_path.name, "id": file_id}
                    )
                except Exception as e:
                    error_msg = (
                        f"Failed to upload {file_path.name} to parent folder: {e}"
                    )
                    print(f"Error: {error_msg}")
                    results["errors"].append(error_msg)

        if results["errors"]:
            results["status"] = "partial"

    except Exception as e:
        results["status"] = "failed"
        results["errors"].append(str(e))
        print(f"Error processing {course_name}: {e}")

    return results


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Notes Backup and PDF Merger")
    parser.add_argument(
        "--config", default="config.json", help="Path to configuration file"
    )
    parser.add_argument(
        "--credentials",
        default="credentials.json",
        help="Path to Google service account credentials",
    )
    parser.add_argument(
        "--token", help="Path to OAuth token file (alternative to credentials)"
    )
    parser.add_argument(
        "--temp-dir", default="./temp", help="Temporary directory for downloads"
    )
    parser.add_argument("--course", help="Process only specific course (optional)")

    args = parser.parse_args()

    # Convert paths to Path objects
    config_path = Path(args.config)
    credentials_path = Path(args.credentials)
    token_path = Path(args.token) if args.token else None
    temp_dir = Path(args.temp_dir)

    # Load configuration
    try:
        config = json.loads(config_path.read_text())
    except FileNotFoundError as e:
        e.strerror = f"Config file not found, see config.example.json"
        raise e

    # Initialize Drive handler
    drive = DriveHandler(
        credentials_path=credentials_path if credentials_path.exists() else None,
        token_path=token_path,
    )

    # Get or create merged folder
    semester_folder_id = config["semester_folder_id"]

    # Process courses
    courses = config["courses"]

    if args.course:
        # Process single course
        try:
            courses = {args.course: courses[args.course]}
        except KeyError as e:
            e.strerror = f"Error: Course '{args.course}' not found in config"
            raise e

    print(f"\nProcessing {len(courses)} course(s)...")
    print(f"Timestamp: {datetime.now()}")

    results = [
        process_course(
            drive, course_name, course_folder_id, temp_dir, semester_folder_id
        )
        for course_name, course_folder_id in courses.items()
    ]

    # Print summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total courses: {len(results)}")

    result_statuses = (result["status"] for result in results)
    statuses_counter = collections.Counter(result_statuses)
    for key, count in statuses_counter.items():
        print(f"{key.capitalize()}: {count}")

    total_files = sum(len(r["files_created"]) for r in results)
    print(f"\nTotal files created: {total_files}")

    # Print detailed results
    for result in results:
        if result["status"] == "success":
            print(f"\n✓ {result['course']}: {len(result['files_created'])} files")
        elif result["status"] == "partial":
            print(
                f"\n⚠ {result['course']}: {len(result['files_created'])} files, {len(result['errors'])} errors"
            )
        elif result["status"] == "failed":
            print(f"\n✗ {result['course']}: Failed")
            for error in result["errors"]:
                print(f"  - {error}")
        else:
            print(f"\n○ {result['course']}: Skipped")

    print(f"\nSemester folder ID: {semester_folder_id}")
    print(
        f"Semester folder URL: https://drive.google.com/drive/folders/{semester_folder_id}"
    )

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
