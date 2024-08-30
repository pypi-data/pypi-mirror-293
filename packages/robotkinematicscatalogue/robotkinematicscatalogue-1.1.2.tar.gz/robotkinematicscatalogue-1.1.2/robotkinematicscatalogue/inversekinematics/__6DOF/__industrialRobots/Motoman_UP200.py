from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class Motoman_UP200(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          730-730,    0           ],
                        [   -np.pi/2,   285,        0,          -np.pi/2    ],
                        [   0,          1150,       0,          0           ],
                        [   -np.pi/2,   0,          1050,       0           ],
                        [   np.pi/2,    0,          0,          0           ],
                        [   -np.pi/2,   0,          255,        0           ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [180, 75, 240, 360, 125, 360]
        self.jointMin = [-180, -60, -60, -360, -125, -360]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, 1, -1, -1, -1, -1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper