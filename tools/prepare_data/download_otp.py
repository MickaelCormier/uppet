import os
import shutil
import zipfile

import gdown


class OpenThermalPoseDownloader:
    googledrive_link = (
        "https://drive.google.com/uc?id=1C5ThcFZm1twYtEta8GWUe1SENc9ER_0t"
    )

    def __init__(self, _path="data/otp/"):
        self.base_dir = _path
        self._create_directories()

    def _create_directories(self):
        os.makedirs(os.path.join(self.base_dir, "images"), exist_ok=True)

    def download_and_organize_images(self):
        zip_path = self._download_zip()
        if zip_path:
            self._extract_images(zip_path)
            self._cleanup(zip_path)
        else:
            print("Download failed.")

    def _download_zip(self):
        zip_path = os.path.join(self.base_dir, "otp_data.zip")
        try:
            gdown.download(self.googledrive_link, zip_path, quiet=False)
        except gdown.exceptions.FileURLRetrievalError as e:
            print("Error downloading file:", e)
            return None
        return zip_path

    def _extract_images(self, zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.base_dir)

        open_thermal_pose_dir = os.path.join(self.base_dir, "OpenThermalPose")
        for sub_dir in ["train", "val", "test"]:
            src_images_dir = os.path.join(open_thermal_pose_dir, sub_dir, "images")
            dst_images_dir = os.path.join(self.base_dir, "images", sub_dir)

            os.makedirs(dst_images_dir, exist_ok=True)
            # Move images to the new directory
            for image_file in os.listdir(src_images_dir):
                shutil.move(os.path.join(src_images_dir, image_file), dst_images_dir)

    def _cleanup(self, zip_path):
        open_thermal_pose_dir = os.path.join(self.base_dir, "OpenThermalPose")
        # Remove the OpenThermalPose directory
        shutil.rmtree(open_thermal_pose_dir)
        # Remove the zip file
        os.remove(zip_path)


def main():
    downloader = OpenThermalPoseDownloader()
    downloader.download_and_organize_images()


if __name__ == "__main__":
    main()
