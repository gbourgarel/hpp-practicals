class MotionPlanner:
  def __init__ (self, robot, ps):
    self.robot = robot
    self.ps = ps

  def solveBiRRT (self, maxIter = float("inf")):
    self.ps.prepareSolveStepByStep ()
    finished = False
    # In the framework of the course, we restrict ourselves to 2 connected components.
    nbCC = self.ps.numberConnectedComponents ()
    if nbCC != 2:
      raise Exception ("There should be 2 connected components.")

    iter = 0
    while True:
      #### RRT begin
      newConfigs = list ()
      config = self.robot.shootRandomConfig()
      for i in range(self.ps.numberConnectedComponents()):
        nearestConfig, _ = self.ps.getNearestConfig(config, i)
        _, pathId, _ = self.ps.directPath(nearestConfig, config, True)
        q = self.ps.configAtParam(pathId, self.ps.pathLength(pathId))
        newConfigs.append(q)
        self.ps.addConfigToRoadmap(q)
        self.ps.addEdgeToRoadmap(nearestConfig, q, pathId, True)
      ## Try connecting the new nodes together
      for i in range (len(newConfigs)):
        if self.ps.numberConnectedComponents()!=2:
          break
        q_list = self.ps.nodesConnectedComponent(1-i)
        for q in q_list:
          if self.ps.directPath(newConfigs[i], q, True)[0]:
            self.ps.addEdgeToRoadmap(newConfigs[i], q, self.ps.directPath(newConfigs[i], q, True)[1], True)
        pass
      #### RRT end
      ## Check if the problem is solved.
      nbCC = self.ps.numberConnectedComponents ()
      if nbCC == 1:
        # Problem solved
        finished = True
        break
      iter = iter + 1
      if iter > maxIter:
        break
    if finished:
        self.ps.finishSolveStepByStep ()
        return self.ps.numberPaths () - 1

  def solvePRM (self):
    self.ps.prepareSolveStepByStep ()
    #### PRM begin
    #### PRM end
    self.ps.finishSolveStepByStep ()
