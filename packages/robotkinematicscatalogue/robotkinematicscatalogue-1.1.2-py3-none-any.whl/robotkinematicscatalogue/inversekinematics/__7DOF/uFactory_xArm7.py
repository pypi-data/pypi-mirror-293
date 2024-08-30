from robotkinematicscatalogue.inversekinematics.__6DOF.sixDOF import *

class uFactory_xArm7(sixDOF):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          267,        0           ],
                        [   -np.pi/2,   0,          0,          0           ],
                        [   np.pi/2,    0,          293,        0           ],
                        [   -np.pi/2,   52.2,       0,          np.pi       ],
                        [   np.pi/2,    -77.5,      342.5,      0           ],
                        [   -np.pi/2,   0,          0,          0           ],
                        [   np.pi/2,    -76,        97,         np.pi       ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [360, 120, 360, 225, 360, 180, 360]
        self.jointMin = [-360, -118, -360, -11, -360, -97, -360]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, 1, 1, -1, 1, 1, 1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper