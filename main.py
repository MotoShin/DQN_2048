import numpy as np
import random
import math
import os
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.font_manager as fm

from dqn import DQN
from task_2048 import Task_2048

def main():
    # 出力画像を保存するディレクトリの作成
    if not os.path.exists('png'):
        os.mkdir('png')
    
    NUM_SIMS = 5
    EPISODE = 100

    env = GridWorld(4, 4)

    fig_reward = plt.figure()
    ax_reward = fig_reward.add_subplot(111)

    agents = {}
    agents.update({"DQN": DQN(env)})
    agents.update({"Q-Learning": Qlerning(env)})

    steps = {}
    for i in agents.keys():
        results = agents[i].run(env, NUM_SIMS, EPISODE)
        ax_reward.plot(results[1] / NUM_SIMS, label=i)
        steps.update({i: results[2]})

    ax_reward.set_xlabel("Episode")
    ax_reward.set_ylabel("Reward")
    ax_reward.legend(loc="upper right")
    plt.legend(ncol=3, frameon=False, fontsize=16) # 各凡例が横に並ぶ数（default: 1）

    fig_reward.savefig("png/Reward.png")
    plt.close()

    fig_steps = plt.figure()
    ax_steps = fig_steps.add_subplot(111)
    for i in agents.keys():
        ax_steps.plot(steps[i] / NUM_SIMS, label=i)
    ax_steps.set_xlabel("Episode", fontsize=20)
    ax_steps.set_ylabel("Steps", fontsize=20)
    # plt.ylim([0, 80])
    ax_steps.legend(loc="upper right")
    plt.legend(ncol=1, frameon=False, fontsize=18) # 各凡例が横に並ぶ数（default: 1）
    font = fm.FontProperties(size=20)
    for label in ax_steps.get_yticklabels():
        label.set_fontproperties(font)
    fig_steps.savefig("png/Steps.png")
    plt.close()

main()
