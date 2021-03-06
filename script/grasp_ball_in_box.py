from math import sqrt
from hpp import Transform
from hpp.corbaserver.manipulation import ConstraintGraph, Constraints
from hpp.corbaserver import Client
Client ().problem.resetProblem ()
from manipulation import robot, vf, ps, Ground, Box, Pokeball, PathPlayer, gripperName, ballName

vf.loadEnvironmentModel (Ground, 'ground')
vf.loadEnvironmentModel (Box, 'box')
vf.moveObstacle ('box/base_link_0', [0.3+0.04, 0, 0.04, 0, 0, 0, 1])
vf.moveObstacle ('box/base_link_1', [0.3-0.04, 0, 0.04, 0, 0, 0, 1])
vf.moveObstacle ('box/base_link_2', [0.3, 0.04, 0.04, 0, 0, 0, 1])
vf.moveObstacle ('box/base_link_3', [0.3, -0.04, 0.04, 0, 0, 0, 1])

vf.loadObjectModel (Pokeball, 'pokeball')
robot.setJointBounds ('pokeball/root_joint', [-.4,.4,-.4,.4,-.1,1.,
                                              -1.0001, 1.0001,-1.0001, 1.0001,
                                              -1.0001, 1.0001,-1.0001, 1.0001,])

q1 = [0, -1.57, 1.57, 0, 0, 0, .3, 0, 0.025, 0, 0, 0, 1]

## Create graph
graph = ConstraintGraph (robot, 'graph')

graph.createNode(['grasp-placement', 'gripper-above-ball', 'ball-above-ground',
                  'grasp', 'placement'])

graph.createEdge('placement', 'placement', 'transit', 1, 'placement')
graph.createEdge('placement', 'gripper-above-ball', 'approach-ball', 1, 'placement')
graph.createEdge('gripper-above-ball', 'placement', 'move-gripper-away', 1, 'placement')
graph.createEdge('gripper-above-ball', 'grasp-placement', 'grasp-ball', 1, 'placement')
graph.createEdge('grasp-placement', 'gripper-above-ball', 'move-gripper-up', 1, 'placement')
graph.createEdge('grasp-placement', 'ball-above-ground', 'take-ball-up', 1, 'grasp')
graph.createEdge('ball-above-ground', 'grasp-placement', 'put-ball-down', 1, 'grasp')
graph.createEdge('ball-above-ground', 'grasp', 'take-ball-away', 1, 'grasp')
graph.createEdge('grasp', 'ball-above-ground', 'approach-ground', 1, 'grasp')
graph.createEdge('grasp', 'grasp', 'transfer', 1, 'grasp')

ps.createTransformationConstraint('placement', '', ballName,
                                  [0,0,0.025,0, 0, 0, 1],
                                  [False, False, True, True, True, False])
ps.setConstantRightHandSide('placement', True)
ps.createTransformationConstraint('placement/complement', '', ballName,
                                  [0,0,0.025,0, 0, 0, 1],
                                  [True, True, False, False, False, True,])
ps.setConstantRightHandSide('placement/complement', False)

ballInGripper = [0, .137, 0, 0.5, 0.5, -0.5, 0.5]
ps.createTransformationConstraint('grasp', gripperName, ballName,
                                  ballInGripper, 6*[True,])

ballUnderGripper = [0, .137+.15, 0, 0.5, 0.5, -0.5, 0.5]
ps.createTransformationConstraint('gripper-above-ball', gripperName, ballName,
                                  ballUnderGripper, 6*[True,])
ps.setConstantRightHandSide('gripper-above-ball', True)

ballInGripper = [0, .137, 0, 0.5, 0.5, -0.5, 0.5]
ps.createTransformationConstraint('ball-in-gripper', gripperName, ballName,
                                  ballInGripper, 6*[True,])
#ps.setConstantRightHandSide('ball-in-gripper', True)

ps.createTransformationConstraint('ball-above-ground', '', ballName,
                                  [0,0,.2,0, 0, 0, 1],
                                  [False, False, True, True, True, False])
ps.setConstantRightHandSide('ball-above-ground', True)


ps.createTransformationConstraint('vertical-free', '', gripperName,
                                  [0,0,.15,0,0,0,1],
                                  [True, True, False, False, False, False])
ps.setConstantRightHandSide('vertical-free', False)

graph.addConstraints(node='placement', constraints=Constraints(numConstraints=['placement'],))
graph.addConstraints(node='grasp', constraints=Constraints(numConstraints=['grasp']))
graph.addConstraints(edge='transit', constraints=Constraints(numConstraints=['placement/complement']))
graph.addConstraints(edge='transfer', constraints=Constraints())
graph.addConstraints(node='gripper-above-ball', constraints=Constraints(numConstraints=['placement', 'gripper-above-ball']))
graph.addConstraints(node='ball-above-ground', constraints=Constraints(numConstraints=['ball-in-gripper', 'ball-above-ground']))
graph.addConstraints(edge='move-gripper-away', constraints=Constraints(numConstraints=['placement/complement']))
graph.addConstraints(edge='approach-ball', constraints=Constraints(numConstraints=['placement/complement']))
graph.addConstraints(edge='take-ball-away', constraints=Constraints())
graph.addConstraints(edge='approach-ground', constraints=Constraints())
graph.addConstraints(node='grasp-placement', constraints=Constraints(numConstraints=['placement', 'ball-in-gripper']))
graph.addConstraints(edge='move-gripper-up', constraints=Constraints(numConstraints=['vertical-free']))
graph.addConstraints(edge='grasp-ball', constraints=Constraints(numConstraints=['vertical-free', 'placement/complement']))
graph.addConstraints(edge='take-ball-up', constraints=Constraints(numConstraints=['vertical-free']))
graph.addConstraints(edge='put-ball-down', constraints=Constraints(numConstraints=['vertical-free']))


ps.selectPathValidation ("Discretized", 0.01)
ps.selectPathProjector ("Progressive", 0.1)
graph.initialize ()

res, q_init, error = graph.applyNodeConstraints ('placement', q1)
q2 = q1 [::]
q2 [7] = .2

res, q_goal, error = graph.applyNodeConstraints ('placement', q2)

ps.setInitialConfig (q_init)
ps.addGoalConfig (q_goal)

# pp = PathPlayer (v)
# v (q1)

## Uncomment to solve and see the solution
# ps.solve()
# v = vf.createViewer ()
# pp=PathPlayer(v)
# pp(0)
