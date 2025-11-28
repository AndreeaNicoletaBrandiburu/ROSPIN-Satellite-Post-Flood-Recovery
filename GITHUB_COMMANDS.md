# Git Commands for GitHub Push

## Initial Setup (if not already done)

If you haven't connected your local repo to GitHub yet:

```powershell
# Check current remote
git remote -v

# If no remote exists, add it (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Standard Workflow

### 1. Check Status

```powershell
git status
```

### 2. Add All Changes

```powershell
git add .
```

Or add specific files:
```powershell
git add README.md
git add data_processing/
git add backend/
git add frontend/
```

### 3. Commit Changes

```powershell
git commit -m "Add full-stack application: data processing V2, Flask backend, React frontend"
```

Or more detailed:
```powershell
git commit -m "Complete HW4 and HW5 deliverables

- Add data processing module V2 (Sentinel-1/2, NDVI, NDWI, radar)
- Add Flask backend API with REST endpoints
- Add React frontend dashboard with interactive map
- Add comprehensive documentation
- Translate all documentation to English"
```

### 4. Push to GitHub

```powershell
git push origin main
```

Or if your default branch is `master`:
```powershell
git push origin master
```

## Complete Sequence

```powershell
# Navigate to project directory
cd C:\Users\ANDREEA\Desktop\ROSPIN-Satellite-Post-Flood-Recovery

# Check what changed
git status

# Add all files
git add .

# Commit with message
git commit -m "Complete HW4 and HW5: Full-stack application with data processing, backend API, and React dashboard"

# Push to GitHub
git push origin main
```

## If You Need to Pull First (if repo has changes)

```powershell
# Pull latest changes
git pull origin main

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge remote changes"
git push origin main
```

## If You Get Authentication Errors

If GitHub asks for authentication:

1. **Use Personal Access Token:**
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with `repo` permissions
   - Use token as password when prompted

2. **Or use SSH:**
   ```powershell
   # Change remote to SSH
   git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

## Verify Push

After pushing, check on GitHub:
- All files should be visible
- README.md should display correctly
- Folder structure should be preserved

