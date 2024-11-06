import os
import shutil
import zipfile

import requests
from tqdm import tqdm


class CamelDownloader:
    dropbox_links = {
        "03": {
            "link": "https://www.dropbox.com/sh/0ifacwigawam2tj/AADXN7sRqckMXVKPoxS2f3cXa?dl=0",
            "train_range": (1, 699),
            "test_range": (700, 952),
            "train_folder": "03_030001_030952",
            "test_folder": "03_030001_030952",
        },
        "04": {
            "link": "https://www.dropbox.com/sh/mh7lofqlx8t7r9f/AACUurWBPWaHXKSXJm_UdIs5a?dl=0",
            "train_range": (1, 680),
            "test_range": (681, 900),
            "train_folder": "04_040001_040900",
            "test_folder": "04_040001_040900",
        },
        "26": {
            "link": "https://www.dropbox.com/sh/j16q1unx04s4ngd/AAApkmgz1ls9umNL0-RAVy_va?dl=0",
            "train_range": (1, 121),
            "test_range": (122, 197),
            "train_folder": "26_260001_260197",
            "test_folder": "26_260001_260197",
        },
        "29": {
            "link": "https://www.dropbox.com/sh/q5aoloxvcqkpb4f/AADKa9MOcr8BVris0Y85rQ-ua?dl=0",
            "train_range": (1, 651),
            "test_range": (652, 877),
            "train_folder": "29_290001_290877",
            "test_folder": "29_290001_290877",
        },
    }

    def __init__(self, _path="data/camel/"):
        self.base_dir = _path
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "images/train"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "images/test"), exist_ok=True)

    def download_and_organize_images(self):
        for sequence, details in self.dropbox_links.items():
            zip_path = self._download_zip(sequence, details["link"])
            self._extract_images(sequence, zip_path, details)
            self._cleanup(zip_path)

    def _download_zip(self, sequence, link):
        download_link = link.replace("?dl=0", "?dl=1")
        response = requests.get(download_link, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        zip_path = os.path.join(self.base_dir, f"{sequence}.zip")
        with open(zip_path, "wb") as f, tqdm(
            desc=sequence,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]",
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                bar.update(len(data))

        return zip_path

    def _extract_images(self, sequence, zip_path, details):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extracted_folder = os.path.join(self.base_dir, sequence)
            zip_ref.extractall(extracted_folder)

        for root, dirs, files in os.walk(extracted_folder):
            for file in files:
                if file.endswith(".jpg"):
                    img_num = int(file.split(".")[0])
                    dest_dir = self._get_destination_directory(img_num, details)
                    if dest_dir:
                        os.makedirs(dest_dir, exist_ok=True)
                        shutil.move(
                            os.path.join(root, file), os.path.join(dest_dir, file)
                        )

    def _get_destination_directory(self, img_num, details):
        if details["train_range"][0] <= img_num <= details["train_range"][1]:
            return os.path.join(self.base_dir, "images/train", details["train_folder"])
        elif details["test_range"][0] <= img_num <= details["test_range"][1]:
            return os.path.join(self.base_dir, "images/test", details["test_folder"])
        return None

    def _cleanup(self, zip_path):
        os.remove(zip_path)
        shutil.rmtree(
            os.path.join(self.base_dir, os.path.basename(zip_path).split(".")[0])
        )


def main():
    downloader = CamelDownloader()
    downloader.download_and_organize_images()


if __name__ == "__main__":
    main()
