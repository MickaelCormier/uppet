from download_annotations import UPPETAnnotationsDownloader
from download_camel import CamelDownloader
from download_llvip import LLVIPDownloader
from download_otp import OpenThermalPoseDownloader


def prepare_datasets():

    # Download & extract datasets
    camel = CamelDownloader()
    camel.download_and_organize_images()

    llvip = LLVIPDownloader()
    llvip.download_and_organize_images()

    otp = OpenThermalPoseDownloader()
    otp.download_and_organize_images()

    # Download & extract annotations
    annotations = UPPETAnnotationsDownloader()
    annotations.download_annotations()

if __name__ == "__main__":
    prepare_datasets()
