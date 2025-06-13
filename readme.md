python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="clean the " \
  --control.repo_id=data/double_so100_clothes \
  --control.tags='["so100","tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=180 \
  --control.reset_time_s=180 \
  --control.num_episodes=50\
  --control.push_to_hub=false \
  --control.display_data=true \
  --control.resume=false 

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --robot.cameras='{}' \
  --control.type=teleoperate \
  --control.display_data=true

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --robot.cameras='{}' \
  --control.type=calibrate \
  --control.arms='["left_follower"]'

python lerobot/scripts/visualize_dataset_html.py --repo-id data/so100_mark

python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_cameras

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=replay \
--control.fps=30 \
--control.repo_id=${HF_USER}/so100_duck \
--control.episode=0

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --robot.cameras='{}' \
  --control.type=calibrate \
  --control.arms='["left_follower"]'

# Chenlu

## train
python lerobot/scripts/train.py \
  --steps=200000 \
  --dataset.repo_id=data/so100_mark1 \
  --policy.type=act \
  --output_dir=outputs/train/act_so100_mark1 \
  --policy.device=cuda \
  --job_name=act_so100_mark1 \
  --wandb.enable=false

### train double so100 grasp
python lerobot/scripts/train.py \
  --steps=200000 \
  --dataset.repo_id=data/double_so100_cube \
  --policy.type=act \
  --output_dir=outputs/train/double_so100_cube \
  --policy.device=cuda \
  --job_name=act_so100_cube \
  --wandb.enable=false

python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=replay \
  --control.fps=30 \
  --control.repo_id=data/double_so100_cube5 \
  --control.episode=0

## eval

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_diffusion_dso100_classify  \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/train/diffusion/double_so100_classify/checkpoints/100000/pretrained_model


python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_act_dso100_clean  \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/train/double_so100_clean/checkpoints/200000/pretrained_model

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_act_dso100_cube  \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/train/double_so100_cube/checkpoints/200000/pretrained_model

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=yingf/eval_act_so100_duck_merge  \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/act_so100_duck_chenlu/080000/pretrained_model

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=yingf/eval_act_so100_duck_merged \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/diffusion_so100_duck_chenlu/500000/pretrained_model

python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Pick up the yellow cube into black square, and then put the red cube on the yellow cube." \
--control.repo_id=yingf/eval_act_so100_cube \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=20 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/train/act_so100_cube/checkpoints/500000/pretrained_model


# Zengyingfu

## duck
python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_act_so100_duck \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/train/act_so100_duck/checkpoints/200000/pretrained_model


## mark
python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_act_so100_mark \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/act_so100_mark_500k/checkpoints/400000/pretrained_model


## maojin
python lerobot/scripts/control_robot.py \
--robot.type=so100 \
--control.type=record \
--control.fps=30 \
--control.single_task="Grasp a duck and put it in the bin." \
--control.repo_id=data/eval_act_so100_towel1 \
--control.tags='["tutorial"]' \
--control.warmup_time_s=5 \
--control.episode_time_s=400 \
--control.reset_time_s=10 \
--control.num_episodes=5 \
--control.push_to_hub=false \
--control.policy.path=outputs/act_so100_towel/checkpoints/200000/pretrained_model

  python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Grasp a duck and put it in the bin." \
  --control.repo_id=yingf/eval_diffusion_so100_duck7 \
  --control.tags='["tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=400 \
  --control.reset_time_s=10 \
  --control.num_episodes=5 \
  --control.push_to_hub=false \
  --control.policy.path=outputs/so100_duck7/diffusion_pretrained_model


  python lerobot/scripts/configure_motor.py \
  --port /dev/ttyACM2 \
  --brand feetech \
  --model sts3215 \
  --baudrate 1000000 \
  --ID 6