import os
from io import BytesIO
from zipfile import ZipFile

import requests

if __name__ == "__main__":
    url = "https://github.com/charlesbel/Microsoft-Rewards-Farmer/archive/refs/heads/master.zip"
    folderName = "Microsoft-Rewards-Farmer-master"
    exclusions = ["sessions", "accounts.json"]
    print("Removing old files...")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name not in exclusions:
                os.remove(os.path.join(root, name))
        for name in dirs:
            if name not in exclusions:
                os.rmdir(os.path.join(root, name))
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
    print("Done !")
