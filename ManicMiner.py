#AO* Algorithm Dec 10, 2025
#David Shapiro

from State import State
from constants import BLANK_STATE, START_STATE, GOAL_STATE, POTHOLE_STATE, ROCKFALL_STATE
from functions import *
import numpy as np
from collections import defaultdict
from typing import Callable
import random

state_objs = [[State(x=x_val, y=y_val, type=BLANK_STATE) for x_val in range(0, 4)] for y_val in range(0,4)]

#Set special states (using 0-3 for indices) y index, x index
state_objs[3][1].set_stateType(START_STATE)
state_objs[0][3].set_stateType(GOAL_STATE)
state_objs[1][2].set_stateType(POTHOLE_STATE)
state_objs[2][1].set_stateType(POTHOLE_STATE)
state_objs[2][3].set_stateType(ROCKFALL_STATE)

States = np.asarray(state_objs)
goal_state = States[0, 3]
start_state = States[3, 1]
actions = {up_action, down_action, left_action, right_action}
discount = 1 #Not used

#MDP DEFINED
MDP = (States, actions, successor_func, cost, discount)

initial_vals = np.zeros((4, 4))
for y in range(States.shape[0]):
    for x in range(States.shape[1]):
        initial_vals[y][x] = np.abs(States[y, x].y - goal_state.y) + np.abs(States[y, x].x - goal_state.x)

#AO Update for AO*
def AOUpdate(state, values, policy, States):
    Z = {state}
    already_seen = set()
    while Z != set():
        curr_state = Z.pop()
        values, policy = BellmanUpdate(curr_state, values, policy, States)
        ancestors = get_ancestors(curr_state, policy, States)
        Z = Z | (ancestors - already_seen)
        already_seen |= ancestors
    return values, policy

#Updates the policy and values
def BellmanUpdate(state, values, policy, States):
    Q = defaultdict(float)
    for action in actions:
        sum = 0
        for desired_state, prob in successor_func(state, action, States).items():
            #Calculate val of possibilities at state
            new_val = prob * (cost(desired_state) + values[desired_state.y, desired_state.x])
            sum += new_val

        Q[action] = sum
    values[state.y, state.x] = min(Q.values())

    #Policy should not have action in Goal State
    if state.type != GOAL_STATE:
        policy[state] = key_of_min(Q)
    return values, policy

def AOStar(States, actions, successor_func, discount, initial_state, initial_values):
    policy = dict()
    fringe = {initial_state}
    interior = set()
    values = np.zeros((4, 4))
    values[initial_state.y, initial_state.x] = initial_values[initial_state.y, initial_state.x]

    while closure(initial_state, policy, States) & fringe != set():
        state = (closure(initial_state, policy, States) & fringe).pop()
        fringe.remove(state)
        interior.add(state)

        #Loading new states
        for action in actions:
            new_states = successor_func(state, action, States).keys()
            for new_state in new_states:
                
                #State has not been seen before
                if new_state not in fringe and new_state not in interior:
                    fringe.add(new_state)
                    values[new_state.y, new_state.x] = initial_values[new_state.y, new_state.x]

        values, policy = AOUpdate(state, values, policy, States)
    return policy

pol = AOStar(States, actions, successor_func, discount, start_state, initial_vals)

#Display Policy Results
print("Policy")
results = sorted([(item.y, item.x) for item in pol.keys()])
for y, x in results:
    print("X: ", x + 1, ", Y: ", y + 1, ", Action: ", action_to_name[pol[States[y, x]]])