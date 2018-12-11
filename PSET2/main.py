import numpy as np
from visuals import gridWorld
from pset2 import gridWorlds
from time import clock

'''Creates trajectories and plots, also determines values for a trajectory'''

# Pe is the probability for error
Pe = .1

# to only have the heading point downwards in the goal state, input 'not all'
# this will not work with the initial policy, I didn't design it with that capability

example = gridWorlds(6, 6, 12, Pe, 'all')

possible_goal_states = example.goal('all')

# make reward matrix
REWARD_MATRIX = np.zeros((6, 6))
REWARD_MATRIX[:, 0] = -100
REWARD_MATRIX[:, -1] = -100
REWARD_MATRIX[0, :] = -100
REWARD_MATRIX[-1, :] = -100
REWARD_MATRIX[2:5, 2] = -10
REWARD_MATRIX[2:5, 4] = -10
REWARD_MATRIX[4, 3] = 1

# create grid world object
grid_world = gridWorld('6x6 grid', REWARD_MATRIX, possible_goal_states)

# generate and plot a trajectory, initial policy
state = (1, 4, 6)
trajectory = [state]
actionMatrix = example.policy_matrix()
valuePi0 = example.policy_evaluation(actionMatrix)
value = valuePi0[1][4][6]
trajectory_value = [value]
grid_world.updateState(state)
grid_world.updateValue(value)
while state not in possible_goal_states:
    action = actionMatrix[state]
    transition = example.transition_function(Pe, state, action) # with Pe = 0, it should get there in min moves
    state = tuple(transition)
    grid_world.updateState(state)
    trajectory.append(state)
    x = state[0]
    y = state[1]
    h = state[2]
    value = valuePi0[x][y][h]
    grid_world.updateValue(value)
    trajectory_value.append(value)
grid_world.plotTrajectoryGradient()
grid_world.saveFigure('trajectory', 'Initial Policy Trajectory', '.pdf')
grid_world.saveFigure('value', 'Iniital Policy Value', '.pdf')
print trajectory
print trajectory_value

# generate and plot a trajectory, policy iteration
state = (1, 4, 6)
trajectory = [state]
actionMatrix0 = example.policy_matrix()
optPolicyMatrix = example.policy_iteration(actionMatrix0)
valuePiStar = example.policy_evaluation(optPolicyMatrix)
value = valuePiStar[1][4][6]
trajectory_value = [value]
grid_world.updateState(state)
grid_world.updateValue(value)
while state not in possible_goal_states:
    prev_value = value
    action = optPolicyMatrix[state]
    transition = example.transition_function(Pe, state, action)
    state = tuple(transition)
    grid_world.updateState(state)
    trajectory.append(state)
    x = state[0]
    y = state[1]
    h = state[2]
    value = valuePiStar[x][y][h]
    grid_world.updateValue(value)
    trajectory_value.append(value)
    if prev_value == value:
        break
grid_world.plotTrajectoryGradient()
grid_world.saveFigure('trajectory', 'PolicyOptimalTrajectoryGoals', '.pdf')
grid_world.saveFigure('value', 'PolicyOptimalSelectGoals', '.pdf')
print trajectory
print trajectory_value

# generate and plot a trajectory, value iteration
state = (1, 4, 6)
trajectory = [state]
optPolicyMatrix, valuePiStar = example.value_iteration()
value = valuePiStar[1][4][6]
trajectory_value = [value]
grid_world.updateState(state)
grid_world.updateValue(value)
while state not in possible_goal_states:
    prev_value = value
    action = optPolicyMatrix[state]
    transition = example.transition_function(Pe, state, action)
    state = tuple(transition)
    grid_world.updateState(state)
    trajectory.append(state)
    x = state[0]
    y = state[1]
    h = state[2]
    value = valuePiStar[x][y][h]
    grid_world.updateValue(value)
    trajectory_value.append(value)
    if prev_value == value:
        break
grid_world.plotTrajectoryGradient()
grid_world.saveFigure('trajectory', 'ValueIterationTrajectoryGoals', '.pdf')
grid_world.saveFigure('value', 'ValueIterationGoals', '.pdf')
print trajectory
print trajectory_value

raw_input('Press Enter when finished')