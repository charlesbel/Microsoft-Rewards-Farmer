import os
from io import BytesIO
from zipfile import ZipFile

import requests


def update(version: str):
    url = "https://github.com/charlesbel/Microsoft-Rewards-Farmer/archive/refs/heads/master.zip"
    folderName = "Microsoft-Rewards-Farmer-master"
    with open(".gitignore", "r") as f:
        exclusions = f.read().splitlines()
        exclusions = [e for e in exclusions if e != "" and not e.startswith("#")] + [
            ".gitignore",
            ".git",
        ]
    print("Removing old files...")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            path = os.path.join(root, name)
            relativePath = path[2:]
            if not relativePath.startswith(tuple(exclusions)):
                os.remove(path)
    print("Downloading...")
    r = requests.get(url)
    data = BytesIO(r.content)
    print("Extracting...")
    with ZipFile(data, "r") as zipObj:
        files = [
            f
            for f in zipObj.namelist()
            if f.startswith(folderName) and not f.endswith("/")
        ]
        for file in files:
            newName = file.replace(f"{folderName}/", "")
            dirName = os.path.dirname(newName)
            if "/" in newName and not os.path.exists(dirName):
                print(f"Creating folder {dirName}...")
                os.makedirs(dirName)
            with zipObj.open(file) as src, open(newName, "wb") as dst:
                dst.write(src.read())
    with open("version.txt", "w") as f:
        f.write(version)
    print("Done !")


def getCurrentVersion():
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            version = f.read()
        return version
    return None


def getLatestVersion():
    r = requests.get(
        "https://api.github.com/repos/charlesbel/Microsoft-Rewards-Farmer/commits/master"
    )
    return r.json()["sha"]


if __name__ == "__main__":
    currentVersion = getCurrentVersion()
    latestVersion = getLatestVersion()
    if currentVersion != latestVersion:
        print("New version available !")
        update(latestVersion)

    print("Starting...")
    from main import main

    main()
