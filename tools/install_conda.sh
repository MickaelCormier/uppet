export CONDA_ENV_NAME=mmpose_uppet
echo $CONDA_ENV_NAME

conda create -n $CONDA_ENV_NAME python=3.8 -y

eval "$(conda shell.bash hook)"
conda activate $CONDA_ENV_NAME

which python
which pip

conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia

pip install -U openmim
mim install "mmengine==0.10.4"
mim install "mmcv==2.1.0"
mim install "mmdet==3.2.0"
mim install "mmpose==1.3.1"

pip install -r requirements.txt

mim install 'mmpretrain==1.2.0'
