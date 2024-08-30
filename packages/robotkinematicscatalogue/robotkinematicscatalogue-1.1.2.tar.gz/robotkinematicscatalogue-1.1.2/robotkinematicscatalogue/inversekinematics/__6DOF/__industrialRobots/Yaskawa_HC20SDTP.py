from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class Yaskawa_HC20SDTP(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          360,        0           ],
                        [   -np.pi/2,   0,          0,          -np.pi/2    ],
                        [   0,          725,        0,          0           ],
                        [   -np.pi/2,   0,          475,        0           ],
                        [   np.pi/2,    0,          185,        0           ],
                        [   -np.pi/2,   0,          200,        0           ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                        
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [210, 180, 290, 210, 180, 210] # jointMax[2] = 247*
        self.jointMin = [-210, -180, -290, -210, -180, -210]
        
        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, 1, -1, -1, -1, -1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper