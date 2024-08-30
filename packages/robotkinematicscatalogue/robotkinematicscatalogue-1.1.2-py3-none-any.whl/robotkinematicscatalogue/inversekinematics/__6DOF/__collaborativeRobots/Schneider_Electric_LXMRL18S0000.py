from robotkinematicscatalogue.inversekinematics.__6DOF.collaborativeRobot import *

class Schneider_Electric_LXMRL18S0000(collaborativeRobot):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
                        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          142.65,     0           ],
                        [   np.pi/2,    0,          0,          0           ],
                        [   0,          510,        0,          0           ],
                        [   0,          400,        -154,       np.pi       ],
                        [   -np.pi/2,   0,          115,        0           ],
                        [   np.pi/2,    0,          103.5,      np.pi       ]])
 
        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [360, 265, 175, 265, 360, 360]
        self.jointMin = [-360, -85, -175, -85, -360, -360]
                
        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1] * 6
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper