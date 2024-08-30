from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class Hans_E10_L(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
                                                
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          260,        0           ],
                        [   -np.pi/2,   0,          0,          -np.pi/2    ],
                        [   0,          600,        0,          -np.pi/2    ],
                        [   -np.pi/2,   0,          700,        0           ],
                        [   np.pi/2,    0,          0,          0           ],
                        [   -np.pi/2,   0,          168,        np.pi       ]])
         
        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                        
        # Joint limits provided in degrees
        self.jointMax = [360, 135, 153, 360, 180, 360]
        self.jointMin = [-360, -135, -153, -360, -180, -360]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, -1, 1, 1, 1, 1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper