from grasp_ball_in_box import q_init, q_goal, robot, ps, graph
from manipulation import vf, PathPlayer

def generatePath(q_from, edgeName, q=None):
    print('step', edgeName)
    trial = 0
    while True:
        if trial % 10 == 0:
            print('trial {0}'.format(trial))
        trial += 1
        q_ = q if q is not None else robot.shootRandomConfig()
        res, q1, err = graph.generateTargetConfig(edgeName, q_from, q_)
        if not res: continue
        res, msg = robot.isConfigValid(q1)
        if not res: continue
        res, pid, msg = ps.directPath(q_from, q1, True)
        if not res: continue
        return pid, q1

def generatePathTwoEdges(q_from, edgeName1, edgeName2, q):
    print(step, edgeName1, edgeName2)
    trial = 0
    while True:
        if trial % 10 == 0:
            print('trial {0}'.format(trial))
        trial += 1
        q_ = robot.shootRandomConfig()
        res, q1, err = graph.generateTargetConfig(edgeName1, q_from, q_)
        if not res: continue
        res, msg = robot.isConfigValid(q1)
        if not res: continue
        res, pid1, msg = ps.directPath(q_from, q1, True)
        if not res: continue
        res, q2, err = graph.generateTargetConfig(edgeName2, q1, q)
        if not res: continue
        res, msg = robot.isConfigValid(q2)
        if not res: continue
        res, pid2, msg = ps.directPath(q1, q2, True)
        if not res: continue
        return pid1, pid2, q1, q2

v=vf.createViewer()
pp=PathPlayer(v)
paths = []

pid, q1 = generatePath(q_init, 'approach-ball')
# pp(pid)
paths.append(pid)

pid, q2 = generatePath(q1, 'grasp-ball')
# pp(pid)
paths.append(pid)

pid, q3 = generatePath(q2, 'take-ball-up')
# pp(pid)
paths.append(pid)

pid1, pid2, q4, q5 = generatePathTwoEdges(q3, 'take-ball-away', 'approach-ground', q_goal)
# pp(pid1);pp(pid2)
paths.append(pid1), paths.append(pid2)

pid, q6 = generatePath(q5, 'put-ball-down', q_goal)
# pp(pid)
paths.append(pid)

pid, q7 = generatePath(q6, 'move-gripper-up', q_goal)
# pp(pid)
paths.append(pid)

pid, q8 = generatePath(q7, 'move-gripper-away', q_goal)
# pp(pid)
paths.append(pid)

# success = False
# trial = 0
# while not success:
#     paths = list ()
#     print ("trial {0}".format (trial)); trial += 1
#     q = robot.shootRandomConfig ()
#     res, q1, err = graph.generateTargetConfig ('approach-ball', q_init, q)
#     if not res: continue
#     res, msg = robot.isConfigValid (q1)
#     if not res: continue
#     res, pid, msg = ps.directPath (q_init, q1, True)
#     paths.append (pid)
#     if not res: continue
#     success = True

v=vf.createViewer()
pp=PathPlayer(v)
for pid in paths:
    pp(pid)
