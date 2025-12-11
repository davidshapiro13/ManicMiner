from constants import POTHOLE_STATE, ROCKFALL_STATE, GOAL_STATE, X_LIM, Y_LIM
import numpy as np
from State import State

#Calculate cost of move to desired state
def cost(desired_state):
    if desired_state.type == POTHOLE_STATE:
        return 5
    elif desired_state.type == ROCKFALL_STATE:
        return 10
    elif desired_state.type == GOAL_STATE:
        return 0
    else:
        return 1

#Get states that you can move to and probability of it happening   
def successor_func(state, expected_action, States):
    possible_actions = applicable(state)
    perpedicular_actions = {up_action: (left_action, right_action), down_action: (left_action, right_action),
                        left_action: (up_action, down_action), right_action: (up_action, down_action)}
    
    #Perpendicular Action 1
    perpedicular1 = perpedicular_actions[expected_action][0]
    if perpedicular1 not in possible_actions:
        perpedicular1 = stay_action

    #Perpendicular Action 2
    perpedicular2 = perpedicular_actions[expected_action][1]
    if perpedicular2 not in possible_actions:
        perpedicular2 = stay_action

    #Expected Action
    if expected_action not in possible_actions:
        expected_action = stay_action

    return {expected_action(state, States):0.8, perpedicular1(state, States):0.1, perpedicular2(state, States):0.1}

#All Possible actions
def up_action(state, States):
    new_state = States[state.y -1, state.x]
    return new_state
def down_action(state, States):
    new_state = States[state.y +1, state.x]
    return new_state
def left_action(state, States):
    new_state = States[state.y, state.x-1]
    return new_state
def right_action(state, States):
    new_state = States[state.y, state.x+1]
    return new_state
def stay_action(state, States):
    return state

#Get all applicable actions
def applicable(state):
    applicable_actions = []
    if state.y > 0:
        applicable_actions.append(up_action)
    if state.y < Y_LIM:
        applicable_actions.append(down_action)
    if state.x > 0:
        applicable_actions.append(left_action)
    if state.x < X_LIM:
        applicable_actions.append(right_action)
    return applicable_actions

#Key of dictionary with minimum value
def key_of_min(dictionary):
    minimum_val = min(dictionary.values())
    for key, val in dictionary.items():
        if val == minimum_val:
            return key
    return "ERROR"

#Get the ancestors of a state
def get_ancestors(state, policy, States):
    ancestors = set()
    for possible_state in policy.keys():
        if possible_state != state:
            results = closure(possible_state, policy, States)
            if state in results:
                ancestors.add(possible_state)
    return ancestors

#All states accessible from start state given policy
def closure(state, policy, States):
    unexplored= {state}
    explored = set()
    accessible_states = set()

    while unexplored != set():
        curr_state = unexplored.pop()
        explored.add(curr_state)
        accessible_states.add(curr_state)

        #Find states durectly connected to curr state
        if curr_state in policy.keys():
            action = policy[curr_state]
            new_states = successor_func(curr_state, action, States)

            for new_state in new_states.keys():
                if new_state not in explored:
                    unexplored.add(new_state)
                    
    return accessible_states

#Translation between action and its name
action_to_name = {up_action: "Go Up", down_action: "Go Down", left_action: "Go Left", right_action: "Go Right"}