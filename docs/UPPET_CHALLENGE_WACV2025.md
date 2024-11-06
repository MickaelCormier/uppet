# UPPET - Human Pose Estimation on Thermal Imaging Challenge at WACV 2025 (UPPET@WACV2025)

## Overview
### The Task
In the context of human pose estimation (HPE) using thermal surveillance imagery, generalizing across different sensors is challenged by domain gaps. These gaps stem from variations in sensor specifications, environmental conditions, and calibration inconsistencies, which can affect the thermal characteristics and representations of human figures. This challenge aims to spotlight the problem of domain gaps in a real-world thermal surveillance context and highlight the challenges and limitations of existing methods to provide a direction for future research.

### The Dataset 
The UPPET [1] Dataset combines LLVIP-Pose[2], CAMEL[3], and OpenThermalPose (OTP)[4], providing harmonized pose annotations across 19,333 images with 15 keypoints from various sensors. It facilitates the evaluation of the robustness of pose estimators to domain shifts, thereby highlighting the limitations of existing methodologies in practical surveillance applications.
In the evaluation phase a fourth subset with new data will be added.


### The Tracks

In order to dynamize the fields of HPE in Thermal Imaging for realistic scenarios, we propose specially selected challenging splits for a challenge with three tracks: 
- Track 1: **Generalization of HPE in Thermal Imaging** using cross-validation scheme: The task is to train a pose estimator that accurately predicts persons’ keypoints under domain shifts.
- Track 2: **HPE in Thermal Imaging** using specialization scheme: The task is to train a pose estimator that accurately predicts persons’ keypoints in thermal imaging.
- Track 3: **HPE on Thermal Imaging based on Synthetic Data**: The task is to generate own thermal synthetic data for training.
Explicitly, the participants should use generative networks (stable diffusion..etc.) to generate synthetic thermal training data. Participants must release and opensource their synthetic data. After training only on synthetic data, the pose estimator is evaluated using specialization scheme on real data.

### The Phases


Each track will be composed of two phases, i.e., the development and test phases. During the development phase, public training data will be released, and participants must submit their predictions concerning a validation set. At the test (final) phase, participants will need to submit their results for the test data, which will be released just a few days before the end of the challenge. As we progress into the test phase, validation annotations will become available together with the test images for the final submission. At the end of the challenge, participants will be ranked using the public test data and additional data that is kept private. It is important to note that this competition involves submitting **results and code**. Therefore, participants will be required to share their code and trained models after the end of the challenge (with detailed instructions) so that the organizers can reproduce the results submitted at the test phase in a code verification stage. <u> The organizers will evaluate the top submissions on the public leaderboard on the private test set to determine the 3 top winners of the challenge. At the end of the challenge, top-ranked methods that pass the code verification stage will be considered valid submissions and compete for the final ranking. </u>

We propose the following evaluation protocols for the challenge:

- Track 1
    1. Validation Phase: Three-fold cross-validation cross-domain scheme: Each of the three datasets is used for training once, and evaluation is performed on the others using AP metric.  
    2. Test Phase: Four-fold cross-validation cross-domain scheme: Each of the four datasets is used for training once, and evaluation is performed on the others using AP metric.
- Track 2
    1. Validation Phase: Specialization scheme: All of the three datasets are used for training at once, and evaluation is performed on all three datasets using AP metric.  
    2. Test Phase: : Specialization scheme: All of the four datasets are used for training at once, and evaluation is performed on all four datasets using AP metric.  
- Track 3
    1. Validation Phase: Training only on Thermal Synthetic Data allowed, and evaluation is performed on all three datasets using AP metric.  
    2. Test Phase: Training only on Thermal Synthetic Data allowed, and evaluation is performed on all four datasets using AP metric.


## Important Dates
| Deadlines                                            |         Date |
|------------------------------------------------------------|--------------|
| Start of the Challenge (development phase)                 |      Nov 6   |
| Release of train/validation data                            |      Nov 6   |
| Release of encrypted test data                              |      Nov 27  |
| End of the Development Phase                                |      Nov 28  |
| Start of the Final Phase                                   |      Nov 29  |
| Release of decryption keys                                  |      Nov 29  |
| End of the Competition                                     |      Dec 6   |
| Code and fact sheets submission                             |      Dec 8   |
| Code verification start                                     |      Dec 9   |
| Code verification end                                       |      Dec 12  |
| Paper submission (challenge participants)                  |      Dec 15  |
| Decision notification                                       |      Dec 20  |
| Camera-ready submission                                     |      Jan 7   |


## Dataset
Detailed information about the dataset coming soon.

## Baseline
We will provide a trained HRNet-W48 and VitPose-H as baselines for Track 1 and Track 2.

## How to enter the competition

The competition will be run on the eval.ai platform. First, register on eval.ai in the following links to submit results during the development and test phase of the challenge. Then, pick a track (or all tracks) to follow and train on the respective training splits. The validation and testing data will remain the same across all tracks.

By submitting result files to the eval.ai platform following the format provided in the starting kit and complying with the challenge rules, the submission will be listed on the leaderboard and ranked.

- Track 1: **Generalization of HPE in Thermal Imaging** (competition link coming soon) using cross-validation scheme: The task is to train a pose estimator that accurately predicts persons’ keypoints under domain shifts.
- Track 2: **HPE in Thermal Imaging**  (competition link coming soon)  using specialization scheme: The task is to train a pose estimator that accurately predicts persons’ keypoints in thermal imaging.
- Track 3: **HPE on Thermal Imaging based on Synthetic Data**  (competition link coming soon) : The task is to generate own thermal synthetic data for training.

The participants will need to register through the platform, where they can submit their predictions on the validation and test data (i.e., development and test phases) and obtain real-time feedback on the leaderboard. The development and test phases will open/close automatically based on the defined schedule.

## Starting kit

The starting kit includes a download script that downloads the sub-datasets, the annotations for the development phase, and submission templates for all tracks. You can find it [here](https://github.com/MickaelCormier/uppet/). Please follow the instructions. The submission templates for all tracks include random predictions and show the expected submission format. More details can be found in the following “Making a submission” section. Participants are required to make submissions using the defined templates, by changing the random predictions by the ones obtained by their models. Note, the evaluation script will verify the consistency of submitted files and may refuse the submission in case of any inconsistency.
**Warning**: the **maximum number of submissions per participant <u>at the test stage</u> will be set to 3**. Participants are not allowed to create multiple accounts to make additional submissions. The organizers may disqualify suspicious submissions that do not follow this rule.

### Use GT bboxes for submission

Since the focus of the challenge lies on the generalization abilities of the pose estimation models, we accomodate top-down models by providing GT bboxes for each sub-split. Each keypoints dict is filled with zeroes, which participants should replace with their predictions.

We provide an inference script using these bboxes and formatting the file to the required format.
For instance for CV Split0 test file:

```
python tools/prepare_submission/prepare_submission.py --submission_file data/annotations/CV/split0/test_split0_gtboxes.json  --output_file data/annotations/CV/split0/test_split0_submit.json --image_dir data/ --config_file path-to-your-mmpose-config-file.py --checkpoint_file path-to-your-model-checkpoint.pth
```

## Making a submission
Detailed information about making a submission coming soon.

## Evaluation Metric

We will use AP as our primary evaluation metric. We will also report AP_50, AP_75, AP_medium and AP_large for your reference.

The calculation works as follows for track 1. First, the metrics are computed separately for each of the three splits and then averaged across the splits.
## Basic Rules

1. The participants only use the training data specified in the "train_X.json" files for training their models on the respective splits. Using training data from another split is strictly forbidden. This includes all kinds of training, calibration, etc.
1. Track 1 and Track 2: models cannot be trained on any additional real or synthetic data except ImageNet and COCO (but only for pre-Training). Pre-training with any other dataset is not allowed.
1. Track 3: models cannot be trained on any additional real data except ImageNet and COCO (but only for pre-Training). Pre-training with any other dataset is not allowed. Only synthetic data is allowed for training.
1. Any use of the test images is prohibited and will result in disqualification. The test data may not be used in any way, not even unsupervised, semi-supervised, or for domain adaptation.
1. Validation data and released labels in the testing phase can only be used to validate the method's performance and not for training.
1. Track 1: For each split, participants may train only one model. This model has to be used to compute predictions for the entire validation/test set. The participants are not allowed to use different approaches/models/hyper-parameter sets/etc. for different subsets of the validation/test data. It is allowed to use different training parameters/hyper-parameters for each of the training splits.
1. The maximum number of submissions per participant at the test stage will be set to 3. Participants are not allowed to create multiple accounts to make additional submissions. The organizers may disqualify suspicious submissions that do not follow this rule.
1. In order to win the challenge, top-ranked participants' scores must improve the baseline performance provided by the challenge organizers.
1. The performances on test data will be verified after the end of the challenge during a code verification stage. Only submissions that pass the code verification will be considered in the final list of winning methods.
1. To be part of the final ranking, the participants will be asked to fill out a survey (fact sheet) where detailed and technical information about the developed approach is provided.


## Final Evaluation and Ranking​ (post-challenge)

Important dates regarding code submission and fact sheets are defined in the schedule.

- **Code verification:** After the end of the test phase, participants are required to share with the organizers the source code used to generate the submitted results, with detailed and complete instructions (and requirements) so that the results can be reproduced locally (preferably using docker). **Note that only solutions that pass the code verification stage are eligible to be announced in the final list of winning solutions.** Participants are required to <u>share both training and prediction code with pre-trained models</u>. Participants are requested to share with the organizers <u>a link to a code repository with the required instructions.</u> This information <u>must be detailed inside the fact sheets</u> (detailed next).
Ideally, the instructions to reproduce the code should contain:
    1. how to structure the data (at train and test stage).
    2. how to run any preprocessing script, if needed.
    3. how to extract or load the input features, if needed.
    4. how to run the docker used to run the code and to install any required libraries, if possible/needed.
    5. how to run the script to perform the training.
    6. how to run the script to perform the predictions, that will generate the output format of the challenge. The script must be able to generate predictions for any input images (Task 1) or query input image combinations (Task 2) specified in a text file (formats analogous to those provided for testing).

- **Fact sheets:** In addition to the source code, participants are required to share with the organizers a detailed scientific and technical description of the proposed approach using the template of the fact sheets provided by the organizers. Latex template of the fact sheets can be downloaded [here](#comingsoon).

**Sharing the requested information with the organizers**: Send the compressed project of your fact sheet (in .zip format), i.e., the generated PDF, .tex, .bib, and any additional files to <mickael.cormier@iosb.fraunhofer.de>, and put in the Subject of the E-mail "WACV 2025 UPPET Challenge / Fact Sheets and Code repository"


<u>IMPORTANT NOTE</u>: we encourage participants to provide detailed and complete instructions so that the organizers can easily reproduce the results. If we face any problem during code verification, we may need to contact the authors, and this can take time, and the release of the list of winners may be delayed.


## Challenge Results (test phase)
Coming soon. (after the end of the challenge ;-) 

## Associated Workshop
Check our associated [Real-World Surveillance: Applications and Challenges Workshop](https://vap.aau.dk/rws-wacv2025/)

