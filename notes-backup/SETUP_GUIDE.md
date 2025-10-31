# Quick Setup Guide

## 🎯 What This Does

Automatically downloads PDFs from your Google Drive course folders, merges them into organized files with clickable bookmarks, and uploads them back to Drive.

## 📁 Required Folder Structure in Google Drive

```
Your Drive/
├── Course1/
│   ├── Lectures/
│   │   ├── Lecture_01.pdf
│   │   ├── Lecture_02.pdf
│   │   └── ...
│   └── Tirgul/
│       ├── Tirgul_01.pdf
│       └── ...
├── Course2/
│   ├── Lectures/
│   └── Tirgul/
└── Merged_Notes/  ← Auto-created, will contain merged PDFs
```

## 🚀 Quick Start (5 minutes)

### Step 1: Get Google Drive Access

1. Go to https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Enable "Google Drive API"
4. Create credentials → Service Account
5. Download the JSON key file → save as `credentials.json`
6. **Important**: Share your Drive folders with the service account email
   - The email looks like: `your-service@your-project.iam.gserviceaccount.com`
   - Give it "Editor" access

### Step 2: Create config.json

```json
{
  "merged_folder_name": "Merged_Notes",
  "courses": {
    "Linear_Algebra": "FOLDER_ID_HERE",
    "Calculus": "FOLDER_ID_HERE"
  }
}
```

**How to get folder ID:**
1. Open folder in Google Drive
2. URL looks like: `drive.google.com/drive/folders/1AbC...XyZ`
3. Copy everything after `/folders/` → that's your folder ID

### Step 3: Add GitHub Secrets

Go to your repo → Settings → Secrets → Actions → New secret

**Secret 1: `GOOGLE_CREDENTIALS`**
- Copy entire content of `credentials.json`
- Paste as-is

**Secret 2: `DRIVE_CONFIG`**
- Copy entire content of `config.json`
- Paste as-is

### Step 4: Run It!

**Option A: Automatic (scheduled)**
- Workflow runs daily at 2 AM UTC automatically
- No action needed

**Option B: Manual trigger**
1. Go to "Actions" tab in GitHub
2. Click "Merge Course Notes"
3. Click "Run workflow"
4. (Optional) Enter specific course name
5. Click green "Run workflow" button

## 📦 Output Files

For each course, creates 3 merged PDFs:

1. **`CourseName_Lectures.pdf`** - All lectures merged
2. **`CourseName_Tirgul.pdf`** - All tutorials merged
3. **`CourseName_Full.pdf`** - Everything together

Each PDF includes:
- ✅ Clickable bookmarks in sidebar
- ✅ Visual table of contents page
- ✅ Proper page ordering

## 🔧 Local Testing

Want to test before setting up GitHub Actions?

```bash
cd notes-backup
pip install -r requirements.txt
python main.py --credentials credentials.json
```

Process just one course:
```bash
python main.py --credentials credentials.json --course "Linear_Algebra"
```

## ❓ Troubleshooting

### "Permission denied" or "File not found"
- **Solution**: Make sure you shared the folders with your service account email

### "Invalid credentials"
- **Solution**: Check that `credentials.json` is valid JSON
- **Solution**: Verify Google Drive API is enabled in Cloud Console

### "No files found"
- **Solution**: Check folder IDs in config.json are correct
- **Solution**: Verify folder structure matches (Lectures/ and Tirgul/ subfolders)

### GitHub Actions failing
- **Solution**: Check that secrets are set correctly (no extra quotes or spaces)
- **Solution**: Look at the Actions logs for specific error messages

## 📊 What Gets Uploaded Where?

All merged PDFs go to the `Merged_Notes` folder (or whatever you named it) in your Google Drive root.

Example result:
```
Your Drive/
└── Merged_Notes/
    ├── Linear_Algebra_Lectures.pdf
    ├── Linear_Algebra_Tirgul.pdf
    ├── Linear_Algebra_Full.pdf
    ├── Calculus_Lectures.pdf
    ├── Calculus_Tirgul.pdf
    └── Calculus_Full.pdf
```

## 🎨 Features

- ✅ Automatically handles sequential numbering (Lecture_01, Lecture_02, etc.)
- ✅ Works with any naming that sorts alphabetically
- ✅ Creates professional TOC with bookmarks
- ✅ Handles courses with only lectures OR only tirgul
- ✅ Runs automatically on schedule
- ✅ Can be triggered manually for specific courses
- ✅ Error handling and detailed logs

## 🔐 Security Notes

- ✅ Never commit `credentials.json` or `config.json` (they're in .gitignore)
- ✅ Use GitHub Secrets for automation
- ✅ Service account only has access to folders you explicitly share
- ✅ Tokens are never exposed in logs

## 💡 Pro Tips

1. **Naming convention**: Keep PDF names consistent (Lecture_01, Lecture_02) for best results
2. **Testing**: Run manually first to verify everything works before relying on schedule
3. **Updates**: If you add new PDFs, just trigger the workflow again
4. **Multiple semesters**: Create separate config.json files or use different merged folder names

## 📞 Need Help?

Check the detailed README.md for more information, or open an issue in the repository.

---

**Time to set up**: ~5 minutes  
**Time saved per semester**: Hours!  
**Coolness factor**: 🚀🚀🚀
