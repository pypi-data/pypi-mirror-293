class RobotArmController:
    def __init__(self, view, parent_controller=None):
        """ Initialize the Robot Arm Controller

        Parameters
        ----------
        view : object
            The Custom Device View object
        parent_controller : object
            The parent (e.g., main) controller object
        """
        self.view = view
        self.parent_controller = parent_controller

        # Get the variables and buttons from the view
        self.variables = self.view.get_variables()
        self.buttons = self.view.buttons

        self.buttons["zero"].configure(command=self.zero_joints)
        self.buttons["disconnect"].configure(command=self.disconnect)
        self.buttons['opengripper'].configure(command=self.open_gripper)
        self.buttons['closegripper'].configure(command=self.close_gripper)

    def zero_joints(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "zero_joints"
        )

    def move_pose(self, a, b, c, d, e, f):
        self.parent_controller.execute(
            "move_pose", a, b, c, d, e, f
        )

    def move_joints(self, a, b, c, d, e, f):
        self.parent_controller.execute(
            "move_joints", a, b, c, d, e, f
        )
    
    def move_lin(self, a, b, c, d, e, f):
        self.parent_controller.execute(
            "move_lin", a, b, c, d, e, f
        )
        
    def open_gripper(self):
        self.parent_controller.execute(
            "open_gripper"
        )
        
    def close_gripper(self):
        self.parent_controller.execute(
            "close_gripper"
        )

    def disconnect(self):
        self.parent_controller.execute(
            "disconnect"
        )
        
    def move_lin_rel_trf(self,a,b,c,d,e,f):
        self.parent_controller.execute(
            "move_lin_rel_trf", a, b, c, d, e, f
        )

    def delay(self,time):
        self.parent_controller.execute(
            "delay", time
        )
    # def move_joints(self, a, b, c, d, e, f):
    #     self.robot_arm.move_joints(a, b, c, d, e, f)
    #     print("Robot has finished moving [move_joints]")
    #
    # def move_pose(self, a, b, c, d, e, f):
    #     self.robot_arm.move_pose(a, b, c, d, e, f)
    #     print("Robot has finished moving [move_pose]")
    #
    # def move_lin_rel_wrf(self, x, y, z, alpha, beta, gamma):
    #     self.robot_arm.move_lin_rel_wrf(x, y, z, alpha, beta, gamma)
    #     print("Robot has finished moving [lin_rel_wrf]")

