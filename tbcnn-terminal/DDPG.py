import os, sys, random
import numpy as np
from itertools import count
import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from restore_model import fileString_convert_vector
import pickle
# from tensorboardX import SummaryWriter

# arguments
device = 'cuda' if torch.cuda.is_available() else 'cpu'
capacity=1000000
state_dim = 600
action_dim = 200
max_action = 2.0
min_Val = torch.tensor(1e-7).float().to(device) # min value

tau=0.005
target_update_interval=1
test_iteration=10
learning_ratet=1e-4
gamma=0.99
capacity=1000000
batch_size=100
seed=False
random_seed=9527

max_episode=100000
dict ={}
with open("/home/tangsong/CLionProjects/InvokeDDPGtest/file:vec.pickle",'rb') as f:
    dict = pickle.load(f)


def cal_dis(list1,list2):
    sum =0
    for i in range(len(list1)):
        sum = sum + (list1[i] - list2[i])**2
    return sum

class Replay_buffer():
    '''
    Code based on:
    https://github.com/openai/baselines/blob/master/baselines/deepq/replay_buffer.py
    Expects tuples of (state, next_state, action, reward, done)
    '''
    def __init__(self, max_size=capacity):
        self.storage = []
        self.max_size = max_size
        self.ptr = 0

    def push(self, data):
        if len(self.storage) == self.max_size:
            self.storage[int(self.ptr)] = data
            self.ptr = (self.ptr + 1) % self.max_size
        else:
            self.storage.append(data)

    def sample(self, batch_size):
        ind = np.random.randint(0, len(self.storage), size=batch_size)
        x, y, u, r, d = [], [], [], [], []

        for i in ind:
            X, Y, U, R, D = self.storage[i]
            x.append(np.array(X, copy=False))
            y.append(np.array(Y, copy=False))
            u.append(np.array(U, copy=False))
            r.append(np.array(R, copy=False))
            d.append(np.array(D, copy=False))

        return np.array(x), np.array(y), np.array(u), np.array(r).reshape(-1, 1), np.array(d).reshape(-1, 1)


class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, max_action):
        super(Actor, self).__init__()

        self.l1 = nn.Linear(state_dim, 400)
        self.l2 = nn.Linear(400, 300)
        self.l3 = nn.Linear(300, action_dim)

        self.max_action = max_action

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.max_action * torch.tanh(self.l3(x))
        return x


class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()

        self.l1 = nn.Linear(state_dim + action_dim, 400)
        self.l2 = nn.Linear(400 , 300)
        self.l3 = nn.Linear(300, 1)

    def forward(self, x, u):
        x = F.relu(self.l1(torch.cat([x, u], 1)))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x

class DDPG(object):
    def __init__(self):
        #initialize actor
        self.actor = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_target = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=1e-4)

        #initialize critic
        self.critic = Critic(state_dim, action_dim).to(device)
        self.critic_target = Critic(state_dim, action_dim).to(device)
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=1e-3)
        self.replay_buffer = Replay_buffer()
        # self.writer = SummaryWriter(directory)

        self.num_critic_update_iteration = 0
        self.num_actor_update_iteration = 0
        self.num_training = 0

        #initialize the file_vector
        self.s0 =[]
        self.a0 =[]
        self.s1=[]
        self.reward =0

    def get_s0(self):
        list = fileString_convert_vector("/home/tangsong/CLionProjects/InvokeDDPGtest/test.js")
        self.s0 = list[0][0]
        print("get s0 -----------------------------------------------")

    def match(self):
        print("match-----------------------")
        max =0
        file_path=""
        for key,value in dict.items():
            dis = cal_dis(self.a0.tolist(),value)
            if dis > max:
                max = dis
                file_path = key
        # print(file_path)
        with open("new_file.txt",'w') as f:
            f.write(file_path)
            f.close()

    def get_s1(self):
        list = fileString_convert_vector("/home/tangsong/CLionProjects/InvokeDDPGtest/test.js")
        self.s1 = list[0][0]
        print("get s1 -----------------------------------------------")


    def select_action(self):
        print('------action-------')
        state = torch.FloatTensor(self.s0.reshape(1, -1)).to(device)
        # print(self.actor(state))
        self.a0 = self.actor(state).cpu().data.numpy().flatten()
        return self.actor(state).cpu().data.numpy().flatten()

    def update(self):
        for it in range(args.update_iteration):
            # Sample replay buffer
            x, y, u, r, d = self.replay_buffer.sample(args.batch_size)
            state = torch.FloatTensor(x).to(device)
            action = torch.FloatTensor(u).to(device)
            next_state = torch.FloatTensor(y).to(device)
            done = torch.FloatTensor(1-d).to(device)
            reward = torch.FloatTensor(r).to(device)

            # Compute the target Q value
            target_Q = self.critic_target(next_state, self.actor_target(next_state))
            target_Q = reward + (done * args.gamma * target_Q).detach()

            # Get current Q estimate
            current_Q = self.critic(state, action)

            # Compute critic loss
            critic_loss = F.mse_loss(current_Q, target_Q)
            self.writer.add_scalar('Loss/critic_loss', critic_loss, global_step=self.num_critic_update_iteration)
            # Optimize the critic
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            self.critic_optimizer.step()

            # Compute actor loss
            actor_loss = -self.critic(state, self.actor(state)).mean()
            self.writer.add_scalar('Loss/actor_loss', actor_loss, global_step=self.num_actor_update_iteration)

            # Optimize the actor
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

            # Update the frozen target models
            for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
                target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)

            for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
                target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)

            self.num_actor_update_iteration += 1
            self.num_critic_update_iteration += 1

    def save(self):
        torch.save(self.actor.state_dict(), '/home/tangsong/CLionProjects/InvokeDDPGtest' + 'actor.pth')
        torch.save(self.critic.state_dict(),'/home/tangsong/CLionProjects/InvokeDDPGtest' + 'critic.pth')
        # print("====================================")
        # print("Model has been saved...")
        # print("====================================")

    def load(self):
        self.actor.load_state_dict(torch.load('/home/tangsong/CLionProjects/InvokeDDPGtest' + 'actor.pth'))
        self.critic.load_state_dict(torch.load('/home/tangsong/CLionProjects/InvokeDDPGtest' + 'critic.pth'))
        print("====================================")
        print("model has been loaded...")
        print("====================================")

# agent = DDPG()
# agent.get_s0()
# agent.select_action()
# file_path = agent.match()
# print(file_path)