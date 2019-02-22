import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count
from PIL import Image
from progressbar import ProgressBar
import time
import copy

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from torch.autograd import Variable

class Net(nn.Module):

    def __init__(self, n_state, n_action):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(n_state, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 100)
        self.head = nn.Linear(100, n_action)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.head(x)
        return x

class DQN():

    def __init__(self, env):
        self.state_num = env.state_num
        self.action_num = env.n_actions
        self.curr_state = 0
        self.next_state = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        ### DQN 用の変数 ###
        self.policy_net = Net(self.state_num, self.action_num)
        self.temp_net = Net(self.state_num, self.action_num)
        self.target_net = Net(self.state_num, self.action_num)
        self.temp_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.RMSprop(self.policy_net.parameters(), lr=0.00015, alpha=0.95, eps=0.01)
        self.GAMMA = 0.999
        
        self.EPS_START = 1
        self.EPS_END = 0
        self.EPS_DECAY = 0.02
        self.BATCH_SIZE = 64
        self.TARGET_UPDATE = 10

        # リプレイバッファ
        self.memory = []
        self.memory_size = 1000

    def initialize(self):
        self.policy_net.load_state_dict(self.temp_net.state_dict())
        self.target_net.load_state_dict(self.temp_net.state_dict())
        self.steps_done = 0

    def init_agent(self):
        self.curr_state = 0
        self.next_state = 0
    
    def select_action(self, state, epi):
        device = self.device
        sample = random.random()
        eps_threshold = max(self.EPS_START - epi * self.EPS_DECAY, self.EPS_END)
        # print(eps_threshold)
        if sample > eps_threshold:
            with torch.no_grad():
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(4)]], device=device, dtype=torch.long)

    def optimize_model(self):
        # print("memory_length: {}".format(len(self.memory)))
        if len(self.memory) < self.BATCH_SIZE:
            return
        r_memory = random.sample(self.memory, len(self.memory))
        memory_idx = range(len(r_memory))
        for idx in memory_idx[::self.BATCH_SIZE]:
            batch = r_memory[idx:idx+self.BATCH_SIZE]
            curr_states, actions, rewards, next_states = [], [], [], []
            for b in batch:
                curr_states.append(b[0][0].numpy())
                actions.append(b[1][0].numpy())
                rewards.append(b[2][0].numpy())
                next_states.append(b[3][0].numpy())
            
            curr_states = np.array(curr_states, dtype=np.float)
            actions = np.array(actions, dtype=np.int32)
            rewards = np.array(rewards, dtype=np.float)
            next_states = np.array(next_states, dtype=np.float)

            curr_states = torch.from_numpy(curr_states)
            actions = torch.from_numpy(actions)
            rewards = torch.from_numpy(rewards)
            next_states = torch.from_numpy(next_states)

            curr_states = curr_states.float()
            Q = self.policy_net(curr_states)
            next_states = next_states.float()
            tmp = self.target_net(next_states)
            # print("tmp: {}".format(tmp.data))
            tmp_data = tmp.data.numpy()
            # print("tmp_max: {}".format(tmp_data.max(axis=1)))
            tmp = tmp_data.max(axis=1)

            max_Q_dash = np.asanyarray(tmp, dtype=np.float)
            target = np.asanyarray(copy.deepcopy(Q.data), dtype=np.float)
            for i in range(len(target)):
                target[i, actions[i]] = rewards[i]+self.GAMMA*max_Q_dash[i]
            
            # self.policy_net.zero_grad()

            target = torch.from_numpy(target)
            target = target.float()
            loss = F.smooth_l1_loss(Q, Variable(target))
            self.optimizer.zero_grad()
            loss.backward()
            for param in self.policy_net.parameters():
                param.grad.data.clamp_(-1, 1)
            self.optimizer.step()

    def run(self, env, num_sims, episode):
        times = np.zeros(num_sims * episode)
        sum_rewards = np.zeros(episode)
        sum_steps = np.zeros(episode)
        device = self.device

        p = ProgressBar(num_sims)  # 最大値100

        for sim in range(num_sims):
            self.initialize()
            p.update(sim+1)  # ProgressBarの表示に合わせて+1
            time.sleep(0.01)
            
            for t in range(episode):
                index = sim * episode + t
                times[index] = t + 1

                self.init_agent()
                sum_reward = 0
                sum_step = 0
                env.reset()
                print("start")

                while True:
                    state = torch.tensor([env.feature_vector()], dtype=torch.float32, device=device)
                    chosen_action = self.select_action(state, t)
                    reward = env.give_reward(self.curr_state, chosen_action.item())
                    # print(reward)
                    # print("{}, {}, {}".format(self.curr_state, chosen_action.item(), sum_reward))
                    self.next_state, done = env.change_state(self.curr_state, chosen_action.item())
                    reward = torch.tensor([reward], device=device)
                    action = torch.tensor([chosen_action], device=device)
                    next_state = torch.tensor([np.eye(env.state_num)[self.next_state]], dtype=torch.float32, device=device)

                    self.memory.append([state, action, reward, next_state])
                    if len(self.memory) > self.memory_size:
                        self.memory.pop(0)

                    self.curr_state = self.next_state
                    # print(self.curr_state)
                    sum_reward += reward.item()
                    sum_step += 1

                    self.optimize_model()
                    if done:
                        print("end, {}, {}".format(sim, t))
                        print()
                        for i in range(self.state_num):
                            feature_vector = np.eye(self.state_num)[i]
                            state = torch.tensor([feature_vector], dtype=torch.float32, device=device)
                            print("{:02}: {}".format(i, self.policy_net(state).data))
                        print()
                        break
                if t % self.TARGET_UPDATE == 0:
                    self.target_net.load_state_dict(self.policy_net.state_dict())
                
                sum_rewards[t] += sum_reward
                sum_steps[t] += sum_step

        return times, sum_rewards, sum_steps


