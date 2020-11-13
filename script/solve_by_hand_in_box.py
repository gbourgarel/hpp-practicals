from grasp_ball_in_box import q_init, q_goal, robot, ps, graph
from manipulation import vf, PathPlayer

def generatePath(q_from, edgeName):
    trial = 0
    while True:
        print('trial {0}'.format(trial))
        trial += 1
        q = robot.shootRandomConfig()
        res, q1, err = graph.generateTargetConfig(edgeName, q_from, q)
        if not res: continue
        res, msg = robot.isConfigValid(q1)
        if not res: continue
        res, pid, msg = ps.directPath(q_from, q1, True)
        if not res: continue
        return pid, q1

paths = []
pid, q1 = generatePath(q_init, 'approach-ball')
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
