#!/usr/bin/env python3
"""
SO100关节读取器 - UDP发送版本
运行在lerobot的conda环境中 (Python 3.10)
"""

import argparse
import json
import socket
import struct
import time

import numpy as np
import torch

from lerobot.common.robot_devices.robots.configs import So100RobotConfig
from lerobot.common.robot_devices.robots.utils import make_simple_robot


class SO100UDPSender:
    def __init__(self, robot, target_host='127.0.0.1', target_port=12345, rate=100):
        self.robot = robot
        self.target_host = target_host
        self.target_port = target_port
        self.rate = rate
        
        # 创建UDP套接字
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 获取关节名称
        self.joint_names = []
        for arm_name in self.robot.leader_arms:
            arm = self.robot.leader_arms[arm_name]
            for motor_name in arm.motor_names:
                self.joint_names.append(f"{arm_name}_{motor_name}")
        
        print(f"UDP Sender initialized: {len(self.joint_names)} joints")
        print(f"Joints: {self.joint_names}")
        print(f"Target: {target_host}:{target_port}")
        print(f"Rate: {rate} Hz")
    
    def read_leader_positions(self):
        """读取leader位置（仿照teleop_step）"""
        if not self.robot.is_connected:
            print("Robot not connected!")
            return None
            
        try:
            leader_positions = []
            
            for arm_name in self.robot.leader_arms:
                before_read_t = time.perf_counter()
                arm_positions = self.robot.leader_arms[arm_name].read("Present_Position")
                arm_positions = torch.from_numpy(arm_positions)
                leader_positions.append(arm_positions)
                
                read_time = time.perf_counter() - before_read_t
                self.robot.logs[f"read_leader_{arm_name}_pos_dt_s"] = read_time
            
            if leader_positions:
                return torch.cat(leader_positions)
            return None
        except Exception as e:
            print(f"Error reading positions: {e}")
            return None
    
    def pack_joint_data_binary(self, positions):
        """打包关节数据为二进制格式（高效）"""
        # 转换为弧度
        positions_package = positions.numpy() / 4096.0
        
        # 二进制格式：时间戳(8字节) + 关节数量(4字节) + 位置数据(每个8字节)
        timestamp = time.time()
        num_joints = len(positions_package)
        
        # 使用struct打包为二进制
        header = struct.pack('dI', timestamp, num_joints)
        positions_packed = struct.pack(f'{num_joints}d', *positions_package)
        
        return header + positions_packed
    
    def pack_joint_data_json(self, positions):
        """打包关节数据为JSON格式（易读）"""
        positions_package = positions.numpy() / 4096.0
        
        data = {
            'timestamp': time.time(),
            'joint_names': self.joint_names,
            'positions': positions_package.tolist(),
            'seq': getattr(self, 'seq', 0)
        }
        
        self.seq = getattr(self, 'seq', 0) + 1
        return json.dumps(data).encode('utf-8')
    
    def run(self, use_binary=True):
        """运行发送循环"""
        print(f"Starting UDP sender... (binary format: {use_binary})")
        print("Press Ctrl+C to stop")
        
        try:
            loop_count = 0
            start_time = time.time()
            
            while True:
                loop_start = time.perf_counter()
                
                # 读取关节位置
                positions = self.read_leader_positions()
                if positions is not None:
                    # 打包数据
                    if use_binary:
                        data = self.pack_joint_data_binary(positions)
                    else:
                        data = self.pack_joint_data_json(positions)
                    
                    # 发送UDP数据
                    try:
                        self.sock.sendto(data, (self.target_host, self.target_port))
                    except Exception as e:
                        print(f"UDP send error: {e}")
                
                loop_count += 1
                
                # 控制发送频率
                elapsed = time.perf_counter() - loop_start
                sleep_time = (1.0 / self.rate) - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                # # 性能统计 - 每2秒输出一次
                # if loop_count % (self.rate * 2) == 0:
                #     total_time = time.time() - start_time
                #     avg_freq = loop_count / total_time
                #     actual_dt = time.perf_counter() - loop_start
                #     actual_freq = 1.0 / actual_dt if actual_dt > 0 else 0
                #     print(f"Stats: avg {avg_freq:.1f} Hz, current {actual_freq:.1f} Hz, sent {loop_count} packets")
                    
        except KeyboardInterrupt:
            print("\nStopping UDP sender...")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.sock.close()


def create_simple_robot_config(robot_type="so100"):
    """创建简单的机器人配置"""
    if robot_type == "so100":
        return {
            "type": "so100"
        }
    else:
        raise ValueError(f"Unsupported robot type: {robot_type}")


def main():
    """主函数"""
    # 简单的参数解析
    parser = argparse.ArgumentParser(description='SO100 UDP Joint Sender')
    parser.add_argument('--robot.type', dest='robot_type', default='so100', 
                       help='Robot type (default: so100)')
    parser.add_argument('--rate', type=int, default=100,
                       help='Send rate in Hz (default: 100)')
    parser.add_argument('--port', type=int, default=12345,
                       help='UDP port (default: 12345)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Target host (default: 127.0.0.1)')
    parser.add_argument('--format', choices=['binary', 'json'], default='binary',
                       help='Data format (default: binary)')
    
    args = parser.parse_args()
    
    try:
        print("="*50)
        print("SO100 UDP Joint Sender")
        print("="*50)
        
        # 创建机器人配置
        robot_config = So100RobotConfig()
        print(f"Robot type: {args.robot_type}")
        print(f"Robot config: {robot_config}")
        
        # 创建并连接机器人
        print("Creating robot...")
        robot = make_simple_robot(robot_config)
        
        print("Connecting to robot...")
        if not robot.is_connected:
            robot.connect()
        print("Robot connected successfully!")
        
        # 检查leader臂
        if not robot.leader_arms:
            raise ValueError("No leader arms found!")
        
        print(f"Found {len(robot.leader_arms)} leader arm(s):")
        for arm_name in robot.leader_arms:
            motors = robot.leader_arms[arm_name].motor_names
            print(f"  - {arm_name}: {len(motors)} motors ({motors})")
        
        # 创建UDP发送器
        sender = SO100UDPSender(
            robot, 
            target_host=args.host,
            target_port=args.port,
            rate=args.rate
        )
        
        # 运行发送器
        sender.run(use_binary=(args.format == 'binary'))
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理
        if 'robot' in locals() and robot.is_connected:
            print("Disconnecting robot...")
            robot.disconnect()
            print("Robot disconnected.")


if __name__ == "__main__":
    main() 