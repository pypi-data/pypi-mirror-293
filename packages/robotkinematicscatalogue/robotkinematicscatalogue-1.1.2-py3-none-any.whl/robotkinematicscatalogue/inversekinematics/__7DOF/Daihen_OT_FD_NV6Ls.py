from robotkinematicscatalogue.inversekinematics.__6DOF.sixDOF import *

class Daihen_OT_FD_NV6Ls(sixDOF):
    
    def __init__(self, base=np.eye(4), gripper=np.eye(4)):
        
        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          525,        0           ],
                        [   -np.pi/2,   185,        0,          0           ],
                        [   np.pi/2,    0,          760,        0           ],
                        [   -np.pi/2,   0,          0,          np.pi/2     ],
                        [   np.pi/2,    -150,       1038.22,    0           ],
                        [   -np.pi/2,   0,          0,          0           ],
                        [   np.pi/2,    0,          99.5,       np.pi       ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]
                                
        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [170, 190, 360, 450, 180, 140, 360]
        self.jointMin = [-170, -65, -360, -270, -180, -140, -360]

        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1, -1, 1, -1, 1, -1, 1]
                
        # Identify nullified joints - prior joints that cancel out at specified self.null_joint element
        self.null_joint = [0, 0, 0, 0, 0, 0, 0]

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper