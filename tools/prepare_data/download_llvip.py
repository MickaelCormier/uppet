import os
import shutil
import zipfile

import gdown


class LLVIPDownloader:
    googledrive_link = (
        "https://drive.google.com/uc?id=1VTlT3Y7e1h-Zsne4zahjx5q0TK2ClMVv"
    )

    def __init__(self, _path="data/llvip/"):
        self.base_dir = _path
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.base_dir, exist_ok=True)

    def download_and_organize_images(self):
        zip_path = self._download_zip()
        if zip_path:
            self._extract_images(zip_path)
            self._cleanup(zip_path)
        else:
            print("Download failed.")

    def _download_zip(self):
        zip_path = os.path.join(self.base_dir, "llvip_data.zip")
        try:
            gdown.download(self.googledrive_link, zip_path, quiet=False)
        except gdown.exceptions.FileURLRetrievalError as e:
            print("Error downloading file:", e)
            return None
        return zip_path

    def _extract_images(self, zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.base_dir)

        # Move contents of the LLVIP directory to the base directory
        llvip_dir = os.path.join(self.base_dir, "LLVIP")
        if os.path.exists(llvip_dir):
            for item in os.listdir(llvip_dir):
                shutil.move(os.path.join(llvip_dir, item), self.base_dir)
            os.rmdir(llvip_dir)  # Remove the LLVIP directory after moving contents

    def _cleanup(self, zip_path):
        # Remove the zip file
        os.remove(zip_path)

        # Remove all items in the base directory except for "infrared"
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            if item != "infrared":  # Skip the "infrared" directory
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directories
                else:
                    os.remove(item_path)  # Remove files


def main():
    downloader = LLVIPDownloader()
    downloader.download_and_organize_images()


if __name__ == "__main__":
    main()
