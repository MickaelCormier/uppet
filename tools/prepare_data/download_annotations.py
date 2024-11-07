import os
import zipfile

import requests
from tqdm import tqdm


class UPPETAnnotationsDownloader:
    github_links = {
        "dev": {
            "link": "https://github.com/MickaelCormier/uppet/releases/download/v0.0.1/annotations.zip",
        },
    }

    def __init__(self, _path="data/"):
        self.base_dir = _path
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.base_dir, exist_ok=True)

    def download_annotations(self):
        url = self.github_links["dev"]["link"]
        zip_path = os.path.join(self.base_dir, "annotations.zip")

        # Download the zip file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        with open(zip_path, "wb") as file, tqdm(
            desc=zip_path,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

        # Unzip the file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.base_dir)

        # Cleanup
        self._cleanup(zip_path)

    def _cleanup(self, zip_path):
        os.remove(zip_path)


def main():
    downloader = UPPETAnnotationsDownloader()  # Fixed the variable name
    downloader.download_annotations()


if __name__ == "__main__":
    main()
