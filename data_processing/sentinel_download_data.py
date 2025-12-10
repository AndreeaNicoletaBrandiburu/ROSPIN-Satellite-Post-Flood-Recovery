"""
Sentinel-2 Data Downloader (CDSE Version)
Automates fetching satellite imagery for the 'Healing Map' project
using the new Copernicus Data Space Ecosystem.
"""

import os
import requests
import zipfile
import shutil
import json
from datetime import date
from glob import glob
from pystac_client import Client

# --- CONFIGURATION ---
USER = 'richgailosuwe@gmail.com'
PASSWORD = 'ROSPIND@T@Processing25'

# CDSE API Endpoints
STAC_API_URL = "https://catalogue.dataspace.copernicus.eu/stac"
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# Search Parameters
START_DATE = "2023-05-01"  # ISO Format YYYY-MM-DD
END_DATE = "2023-08-01"
CLOUD_COVER_LIMIT = 20

# Files and Folders
GEOJSON_PATH = 'map.geojson'
DOWNLOAD_FOLDER = 'real_satellite_data'


def get_access_token(username, password):
    """
    Authenticates with the new Copernicus Identity system to get a download token.
    """
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Authentication Failed: {e}")
        return None


def download_file(url, session, save_path, filename):
    """
    Downloads a file using the authenticated session.
    """
    print(f"⬇️ Downloading {filename}...")
    try:
        with session.get(url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("✅ Download complete.")
        return True
    except Exception as e:
        print(f"⚠️ Download failed: {e}")
        return False


def organize_sentinel_data(zip_path, extract_path):
    """
    Helper: Unzips the raw .SAFE file and extracts ONLY Band 4 and Band 8.
    """
    print(f"📦 Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        print("⚠️ Error: Downloaded file is not a valid zip.")
        return

    # Find the unzipped .SAFE folder
    safe_folders = glob(os.path.join(extract_path, "*.SAFE"))
    if not safe_folders:
        print(f"⚠️ No .SAFE folder found in {zip_path}")
        return

    safe_folder = safe_folders[0]
    folder_name = os.path.basename(safe_folder)

    # Parse date from folder name
    try:
        date_str = folder_name.split('_')[2][:8]  # YYYYMMDD
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    except IndexError:
        print(f"⚠️ Could not parse date from {folder_name}")
        return

    # Create destination folder
    dest_dir = os.path.join(DOWNLOAD_FOLDER, formatted_date)
    os.makedirs(dest_dir, exist_ok=True)

    # Find Bands
    b4_path = glob(os.path.join(safe_folder, "**", "*B04_10m.jp2"), recursive=True)
    b8_path = glob(os.path.join(safe_folder, "**", "*B08_10m.jp2"), recursive=True)

    if b4_path and b8_path:
        shutil.copy(b4_path[0], os.path.join(dest_dir, "B04.jp2"))
        shutil.copy(b8_path[0], os.path.join(dest_dir, "B08.jp2"))
        print(f"✅ Organized data for {formatted_date}")
    else:
        print(f"⚠️ Could not find bands in {safe_folder}")

    # Cleanup
    try:
        shutil.rmtree(safe_folder)
    except OSError as e:
        print(f"⚠️ Error cleaning up {safe_folder}: {e}")


def main():
    # 1. Load GeoJSON
    if not os.path.exists(GEOJSON_PATH):
        print(f"❌ Error: {GEOJSON_PATH} not found.")
        return

    with open(GEOJSON_PATH) as f:
        geojson_data = json.load(f)
        # Assuming the GeoJSON contains a FeatureCollection, we take the first feature's geometry
        geometry = geojson_data['features'][0]['geometry']

    # 2. Search using STAC API
    print(f"🔍 Searching Sentinel-2 images ({START_DATE} to {END_DATE})...")

    client = Client.open(STAC_API_URL)
    search = client.search(
        collections=["SENTINEL-2"],
        intersects=geometry,
        datetime=f"{START_DATE}/{END_DATE}",
        query={"eo:cloud_cover": {"lt": CLOUD_COVER_LIMIT}}
    )

    items = list(search.items())
    print(f"Found {len(items)} images.")

    if not items:
        return

    # 3. Authenticate for Download
    token = get_access_token(USER, PASSWORD)
    if not token:
        return

    # Create a session with the token
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    # 4. Download and Process
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    for item in items:
        # Get the download link for the full product (application/zip)
        # Note: CDSE STAC usually provides an 'assets' dictionary.
        # For the full zip, we often look for the 'download' link or 'zipper' endpoint.
        # Alternatively, we construct the OData download URL using the Product ID.

        product_id = item.id
        print(f"\nProcessing Product ID: {product_id}")

        # CDSE OData Download URL
        download_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"

        zip_filename = f"{product_id}.zip"
        zip_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)

        success = download_file(download_url, session, zip_path, zip_filename)

        if success:
            organize_sentinel_data(zip_path, DOWNLOAD_FOLDER)
            # Delete zip
            if os.path.exists(zip_path):
                os.remove(zip_path)

if __name__ == "__main__":
    main()