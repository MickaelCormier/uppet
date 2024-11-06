import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from mmpose.apis import inference_topdown, init_model
from mmpose.structures import PoseDataSample, merge_data_samples
from tqdm import tqdm


def get_bboxes_from_dict(img_id: int, ann_dict: Dict[str, Any]) -> List[List[float]]:
    """Get all bounding box annotations for the given image ID."""
    img_id = int(img_id)
    bboxes = [
        ann["bbox"] + [img_id, i]
        for i, ann in enumerate(ann_dict["annotations"])
        if img_id == int(ann["image_id"])
    ]

    return bboxes


def process_image_topdown(
    img: str, bboxes: List[List[float]], pose_estimator
) -> PoseDataSample:
    """Get predicted keypoints (and heatmaps) of one image."""
    bboxes_xyxy = [
        [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]] for bbox in bboxes
    ]

    pose_results = inference_topdown(pose_estimator, img, bboxes_xyxy)
    data_samples = merge_data_samples(pose_results)

    return data_samples


def run_pose_estimator_on_submission_file(
    submission_file_path: str,
    output_file_path: str,
    image_dir: str,
    config_file: str,
    checkpoint_file: str,
    device: str,
    limit: Optional[int] = None,
) -> None:
    pose_model = init_model(config_file, checkpoint_file, device=device)

    with open(submission_file_path, "r") as f:
        submission_data = json.load(f)

    annotations = submission_data["annotations"]
    for i, img in tqdm(
        enumerate(submission_data["images"]), total=len(submission_data["images"])
    ):
        if limit and i >= limit:
            break

        image_id = img["id"]
        image_path = os.path.join(image_dir, img["file_name"])

        if not os.path.exists(image_path):
            print(f"Warning: Image {image_path} not found. Skipping...")
            continue

        bboxes = get_bboxes_from_dict(image_id, submission_data)

        pred_instances = process_image_topdown(
            image_path, bboxes, pose_model
        ).pred_instances

        for j, bbox in enumerate(bboxes):
            if j < len(pred_instances.keypoints):
                keypoints = pred_instances.keypoints[j]
                keypoints_scores = pred_instances.keypoint_scores[j]
                keypoints = np.array(
                    [
                        [float(keypoint[0]), float(keypoint[1]), float(keypoint_score)]
                        for keypoint, keypoint_score in zip(keypoints, keypoints_scores)
                    ]
                )
                keypoints = keypoints.flatten().tolist()

                annotations[bbox[-1]]["keypoints"] = keypoints

            else:
                print(
                    f"Warning: No keypoints found for bbox index {j} in image_id {image_id}. Skipping..."
                )

    output_file = Path(output_file_path).with_suffix(".json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(annotations, f, indent=4)

    print(f"Submission file created at: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pose estimator on submission file."
    )
    parser.add_argument(
        "--submission_file",
        "-s",
        type=str,
        required=True,
        help="Path to the submission file with bounding boxes.",
    )
    parser.add_argument(
        "--output_file",
        "-o",
        type=str,
        required=True,
        help="Path to save the extended submission file.",
    )
    parser.add_argument(
        "--image_dir",
        "-img",
        type=str,
        required=True,
        help="Directory containing images.",
    )
    parser.add_argument(
        "--config_file",
        "-cfg",
        type=str,
        required=True,
        help="Path to the model configuration file.",
    )
    parser.add_argument(
        "--checkpoint_file",
        "-ckpt",
        type=str,
        required=True,
        help="Path to the model checkpoint file.",
    )
    parser.add_argument(
        "--device",
        "-d",
        type=str,
        default="cuda:0",
        help="Device to run the model on (e.g., cuda:0 or cpu).",
    )
    parser.add_argument(
        "--limit", "-l", type=int, help="Limit the number of images to process."
    )

    args = parser.parse_args()

    run_pose_estimator_on_submission_file(
        args.submission_file,
        args.output_file,
        args.image_dir,
        args.config_file,
        args.checkpoint_file,
        args.device,
        args.limit,
    )
