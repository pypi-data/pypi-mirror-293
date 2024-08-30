from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class Motoman_MH12(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          450-450,    0           ],
                        [   -np.pi/2,   155,        0,          -np.pi/2    ],
                        [   0,          614,        0,          0           ],
                        [   -np.pi/2,   200,        640,        0           ],
                        [   np.pi/2,    0,          0,          0           ],
                        [   -np.pi/2,   0,          100,        0           ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [170, 155, 175, 180, 135, 360]
        self.jointMin = [-170, -90, -175, -180, -135, -360]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, 1, -1, -1, -1, -1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper