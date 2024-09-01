import os
import json
import yaml
import argparse
import requests
import subprocess
import tarfile
import shutil

# Download the latest version of Positron
def init():
    # Fetch the latest release
    with requests.get("https://api.github.com/repos/kaangiray26/positron/releases/latest") as r:
        if r.status_code != 200:
            raise Exception("Failed to fetch the latest release!")

        url = r.json()["assets"][0]["browser_download_url"]

    # Download the release
    with requests.get(url) as r:
        with open("positron.tar.gz", "wb") as f:
            f.write(r.content)

    # Open the tar archive
    with tarfile.open("positron.tar.gz", "r:gz") as tar:
        tar.extractall()

    # Remove the tar archive
    os.remove("positron.tar.gz")
    print("Positron has been installed.")

# Run the development server
def dev():
    subprocess.run(["env/bin/python3", "-m", "hypercorn", "app:app", "--reload"])

# Build the flatpak package
def build():
    # Check if the manifest file exists
    files = [f for f in os.listdir(".") if f.startswith("manifest.")]
    if not len(files):
        raise Exception("Manifest file not found!")

    # Read the manifest file
    if files[0].endswith(".yaml"):
        with open(files[0], "r") as f:
            manifest = yaml.safe_load(f)
    elif files[0].endswith(".json"):
        with open(files[0], "r") as f:
            manifest = json.load(f)
    else:
        raise Exception("Invalid manifest file format!")

    # Clean up
    shutil.rmtree(".flatpak-builder", ignore_errors=True)
    shutil.rmtree("build-dir", ignore_errors=True)

    # Get the latest firefox build if it doesn't exist
    if not os.path.exists("firefox.tar.bz2"):
        with requests.get("https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US", stream=True) as r:
            r.raise_for_status()
            with open("firefox.tar.bz2", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    # Create wheels if they don't exist
    if not os.path.exists("wheels"):
        subprocess.run(["docker", "build", "-t", "flatpak-wheels", ".", "--no-cache"])
        subprocess.run(["docker", "run", "--name", "flatpak-wheels", "flatpak-wheels"])
        os.makedirs("wheels", exist_ok=True)
        subprocess.run(["docker", "cp", "flatpak-wheels:/app/wheels/.", "wheels"])
        subprocess.run(["docker", "rm", "flatpak-wheels"])

    # Remove old flatpak
    subprocess.run(["flatpak", "uninstall", "-y", manifest["id"]])

    # Build the flatpak
    result = subprocess.run(["flatpak-builder", "--force-clean", "--install", "--user", "build-dir", files[0]], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception("Flatpak build failed!")

    # Run the flatpak
    subprocess.run(["flatpak", "run", manifest["id"]])

def main():
    parser = argparse.ArgumentParser(description='Positron CLI tool')
    parser.add_argument('command', type=str, help='Command to run', choices=['init', 'dev', 'build', 'serve', 'deploy'])
    args = parser.parse_args()

    match args.command:
        case "init":
            init()

        case "dev":
            dev()

        case "build":
            build()

if __name__ == "__main__":
    main()