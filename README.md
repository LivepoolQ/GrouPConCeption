# Code of GrouPConCeption

This is the official code of manuscript *Who Walks With You Matters: Perceiving Social Interactions with Groups for Pedestrian Trajectory Prediction*. The paper is available at [arxiv](http://arxiv.org/abs/2412.02395).

## Environment Configuration

We recommend creating a virtual environment with packages in `requirements.txt` to test our code.

```bash
conda create -n your_env_name python==3.10
```

```bash
pip install -r requirements.txt
```

## Dataset Configuration

The datasets (**ETH-UCY, SDD, NBA, nuScenes**) are preprocessed and provided in this code implementation.

### Pre-trained Model Weights

The pre-trained model weights of different datasets (**ETH-UCY, SDD, NBA, nuScenes**) are available [here](https://github.com/LivepoolQ/GrouPConCeption/releases/tag/v1.1).

Run the following command to evaluate these pre-trained weights:

```bash
python main.py --load ./weights/group_{dataset}
```

## Training

Run the following command to train the typical `gp` model from the beginning:

```bash
python main.py --model gp --split SPLIT 
```

`SPLIT` is a train-test-val split of the dataset.
Arg `--split` accepts {`eth`, `hotel`, `univ13`, `zara1`, `zara2`} (ETH-UCY), {`sdd`} (SDD), {`nba50k`} (NBA), {`nuScenes_ov_v1.0`} (nuScenes).
Add args to train variational (corresponding to the ablation study in the paper) GPCC model.

### Args

- `--split` (short for `-s`): type=`str`, argtype=`static`.
 The dataset split that used to train and evaluate.
 The default value is `zara1`.
- `--gpu`: type=`str`, argtype=`temporary`.
Speed up training or test if you have at least one NVidia GPU. If you have no GPUs or want to run the code on your CPU, please set it to `-1`. NOTE: It only supports training or testing on one GPU.
The default value is `0`.
- `--epochs`: type=`int`, argtype=`static`.
 Maximum training epochs. 
 The default value is `500`.
- `--batch_size` (short for `-bs`): type=`int`, argtype=`dynamic`.
 Batch size when implementation.
 The default value is `5000`.
- `--lr` (short for `-lr`): type=`float`, argtype=`static`.
 Learning rate.
 The default value is `0.001`.
- `--use_group`: type=`int`, argtype=`STATIC`.
 Choose whether to use pedestrian groups when calculating Conception.
 The default value is `1`.
- `--view_angle`: type=`float`, argtype=`STATIC`.
 Value of conception field of view (FOV).
 The default value is `np.pi`.
- `--use_view_angle`: type=`int`, argtype=`STATIC`.
 Choose whether to use view angle in calculating Conception.
 The default value is `1`.
- `--use_pooling`: type=`int`, argtype=`STATIC`.
 Choose whether to use pooling in calculating conception value.
 Only choose one between pooling and max.
 The default value is `1`.
- `--use_max`: type=`int`, argtype=`STATIC`.
 Choose whether to use max in calculating conception value.
 Only choose one between pooling and max.
 The default value is `0`.
- `--output_units`: type=`int`, argtype=`STATIC`.
 Set the number of the output units of trajectory encoding.
 The default value is `32`.
- `--use_velocity`: type=`int`, argtype=`STATIC`.
Choose whether to use the velocity factor in the Conception.
The default value is `1`.
- `--use_distance`: type=`int`, argtype=`STATIC`.
Choose whether to use the distance factor in the Conception.
The default value is `1`.
- `--use_move_dir`: type=`int`, argtype=`STATIC`.
Choose whether to use the move direction factor in the Conception.
The default value is `1`.
- `--disable_conception`: type=`int`, argtype=`STATIC`.
Choose whether to disable conception layer in the GroupModel.
The default value is `0`.
- `--generation_num`: type=`int`, argtype=`STATIC`.
Number of multi-style generation.
The default value is `20`.

Add args above to train specific GPCC model as the following command:

```bash
python main.py --model gp --split {dataset} --batchsize {batchsize} --lr {lr} --{Arg} arg --{Arg} arg ... --{Arg} arg
```

If no arg is detected, the model will use the default settings:

```bash
python main.py --model gp
```

Continue to train from checkpoints or pre-trained weights using this command:

```bash
python main.py --restore_args {checkpoint/weight_file}
```

## Visualization

Run the following command to run a visualization demo:

```bash
python playground/main.py
```

Reload model weights in the demo and visualize them.
The output file is stored in `temp_files/playground`.
Uncomment visualization codes commented out in `gp.py` and `conception.py` to see results of attention value and contribution ratio demonstrated in the paper.
The output file is stored in `temp_files/gp`.
