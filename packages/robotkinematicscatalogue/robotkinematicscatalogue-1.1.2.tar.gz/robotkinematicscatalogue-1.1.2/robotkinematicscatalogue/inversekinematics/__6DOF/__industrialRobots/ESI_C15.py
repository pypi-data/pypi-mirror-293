from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class ESI_C15(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
                                                
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          345-345,    -np.pi/2    ],
                        [   -np.pi/2,   0,          0,          -np.pi/2    ],
                        [   0,          550,        0,          -np.pi/2    ],
                        [   -np.pi/2,   0,          601.5,      0           ],
                        [   np.pi/2,    0,          155,        0           ],
                        [   -np.pi/2,   0,          172.6,      -np.pi/2    ]])
         
        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                        
        # Joint limits provided in degrees
        self.jointMax = [160, 150, 160, 180, 180, 180]
        self.jointMin = [-160, -150, -160, -180, -180, -180]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1] * 6
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper