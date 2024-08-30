from robotkinematicscatalogue.forwardKinematics import *

class Reis_RL130P_CNC(forwardKinematics):
    
    def __init__(self, base=angleSetConventions.transformMatrix([0, 0, 0, 0, -90, 0], "ZYX"), 
                 gripper=angleSetConventions.transformMatrix([0, -186.5, 0, 0, 0, 90], "ZYX")):

        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          -20,        0           ],
                        [   np.pi/2,    0,          -2084.5,    np.pi/2     ],
                        [   np.pi/2,    0,          -1214,      0           ],
                        [   0,          0,          0,          np.pi/2     ],
                        [   np.pi/2,    0,          -295,       0           ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [8000.1, 3000.1, 1500.1, 180, 180]
        self.jointMin = [-0.1, -0.1, -0.1, 180, -180]
                
        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1] * 5
        
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 1, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper