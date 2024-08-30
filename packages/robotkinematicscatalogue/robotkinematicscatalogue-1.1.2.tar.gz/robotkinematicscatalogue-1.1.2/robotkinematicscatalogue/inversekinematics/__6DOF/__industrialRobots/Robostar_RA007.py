from robotkinematicscatalogue.inversekinematics.__6DOF.industrialRobot import *

class Robostar_RA007(industrialRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
                
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          383,        0           ],
                        [   -np.pi/2,   50,         0,          -np.pi/2    ],
                        [   0,          440,        0,          0           ],
                        [   -np.pi/2,   20,         440,        0           ],
                        [   np.pi/2,    0,          0,          0           ],
                        [   -np.pi/2,   0,          83,         np.pi       ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [170, 140, 67, 190, 125, 360]
        self.jointMin = [-170, -90, -205, -190, -125, -360]
        
        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1] * 6
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper