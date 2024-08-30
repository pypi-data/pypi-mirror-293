from robotkinematicscatalogue.inversekinematics.__4DOF.SCARARobot import *

class ABB_IRB_920T_6_055(SCARARobot):

    def __init__(self, base=np.eye(4), gripper=np.eye(4)):

        # Modified Denavit-Hartenberg parameters (DHM)
        DHM = np.array([[   0,          0,          0,          0           ],
                        [   0,          290,        0,          0           ],
                        [   0,          260,        180,        0           ],
                        [   np.pi,      0,          0,          0           ]])

        self.alpha = DHM[:,0]
        self.a = DHM[:,1]
        self.d = DHM[:,2]
        self.theta = DHM[:,3]

        # Joint limits provided in degrees and/or millimeters (mm)
        self.jointMax = [140, 150, 0.1, 400]
        self.jointMin = [-140, -150, -180.1, -400]
        self.translationalJoint = 3 # The joint using translational movement
                                
        # Identify inverted joints - joints that rotate counterclockwise in local z-axis frame
        self.inv_joint = [1] * 6

        # The base and gripper/end-effector of the robot
        self.TB0 = base
        self.T6W = gripper