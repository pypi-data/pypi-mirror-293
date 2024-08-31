class SyntheticRobotArm:
    """ A synthetic robot arm class """

    def __init__(self, device_connection, *args):
        """ Initialize the Synthetic Device

        Parameters
        ----------
        device_connection : object
            The device connection object
        args : list
            The arguments for the device
        """
        self.device = device_connection  # DummyDeviceConnection is provided here
        pass

    def start_program(self, program_name):
        """ Start offline robot program

        Parameters
        ----------
        program_name : str
            String containing the offline program name

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: Start {program_name} Program")

    def disconnect(self):
        """ Disconnects the Mecademic Robot object from the robot and system

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Disconnect")

    def zero_joints(self):
        """ Zero the joints of the synthetic device

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Zero Joints")

    def move_joints(self, j1, j2, j3, j4, j5, j6):
        """ Move robot arm joints to the specified angles

        Parameters
        ----------
        j1 : float
            Angle of joint 1
        j2 : float
            Angle of joint 2
        j3 : float
            Angle of joint 3
        j4 : float
            Angle of joint 4
        j5 : float
            Angle of joint 5
        j6 : float
            Angle of joint 6

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: MoveJoints({j1}, {j2}, {j3}, {j4}, {j5}, {j6})")

    def move_lin(self, x, y, z, rx, ry, rz):
        """ Move the robot arm along a linear path (in the Cartesian space) to a given pose

        Parameters
        ----------
        x : float
            position in x
        y : float
            position in y
        z : float
            position in z
        rx : float
            angle around x-axis
        ry : float
            angle around y-axis
        rz : float
            angle around z-axis

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: MoveLin({x}, {y}, {z}, {rx}, {ry}, {rz})")

    def move_lin_ref_trf(self, x, y, z, rx, ry, rz):
        """ Move robot arm relative to the tool reference frame

        Parameters
        ----------
        x : float
            distance (mm) in x
        y : float
            distance (mm) in y
        z : float
            distance (mm) in z
        rx : float
            angle around x-axis
        ry : float
            angle around y-axis
        rz : float
            angle around z-axis

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: MoveLinRelTrf({x}, {y}, {z}, {rx}, {ry}, {rz})")

    def move_lin_ref_wrf(self, x, y, z, rx, ry, rz):
        """ Move robot arm relative to the world reference frame

        Parameters
        ----------
        x : float
            distance (mm) in x
        y : float
            distance (mm) in y
        z : float
            distance (mm) in z
        rx : float
            angle around x-axis
        ry : float
            angle around y-axis
        rz : float
            angle around z-axis

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: MoveLinRelWrf({x}, {y}, {z}, {rx}, {ry}, {rz})")

    def move_pose(self, x, y, z, rx, ry, rz):
        """ Move Robot Arm to the given Pose

        Parameters
        ----------
        x : float
            position in x
        y : float
            position in y
        z : float
            position in z
        rx : float
            angle around x-axis
        ry : float
            angle around y-axis
        rz : float
            angle around z-axis

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: MovePose({x}, {y}, {z}, {rx}, {ry}, {rz})")

    def delay(self, wait):
        """ Delays robot operation by a specified time

        Parameters
        ----------
        wait : float
            time in seconds to delay the robot

        Returns
        -------

        """
        print(f"*** Synthetic robot receive command: Delay by {wait} seconds")

    def activate_and_home(self):
        """ Activates and Homes the Robot

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Activate and Home")

    def load_robot_config(self):
        """ Loads robot configuration data

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Load robot config")

    def open_gripper(self):
        """ Open the robot gripper

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Open gripper")

    def close_gripper(self):
        """ Close the robot gripper

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Close gripper")

    def pause_robot_motion(self):
        """ Pause robot motion for synthetic device

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Pause robot motion")

    def resume_robot_motion(self):
        """ Resume robot motion for synthetic device

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Resume robot motion")

    def reset_robot_motion(self):
        """ Reset robot motion for synthetic device

        Returns
        -------

        """
        print("*** Synthetic robot receive command: Reset robot motion")

    def reset_error(self):
        """ Reset robot error for synthetic device

        Returns
        -------

        """
        print("*** Synthetic device received command: Reset error")

    @property
    def commands(self):
        """Return the commands for the synthetic device

        Returns
        -------
        commands : dict
            commands that the device supports
        """
        return {
            "start_program": lambda *args: self.start_program(args[0]),
            "disconnect": lambda *args: self.disconnect(),
            "zero_joints": lambda *args: self.zero_joints(),
            "move_joints": lambda *args: self.move_joints(args[0], args[1], args[2], args[3], args[4], args[5]),
            "move_lin": lambda *args: self.move_joints(args[0], args[1], args[2], args[3],
                                                          args[4], args[5]),
            "move_lin_rel_trf": lambda *args: self.move_joints(args[0], args[1], args[2], args[3],
                                                          args[4], args[5]),
            "move_lin_rel_wrf": lambda *args: self.move_joints(args[0], args[1], args[2], args[3],
                                                          args[4], args[5]),
            "move_pose": lambda *args: self.move_pose(args[0], args[1], args[2], args[3], args[4], args[5]),
            "delay": lambda *args: self.delay(args[0]),
            "activate_and_home": lambda *args: self.activate_and_home(),
            "open_gripper": lambda *args: self.open_gripper(),
            "close_gripper": lambda *args: self.close_gripper(),
            "pause_motion": lambda *args: self.pause_robot_motion(),
            "resume_motion": lambda *args: self.resume_robot_motion(),
            "reset_motion": lambda *args: self.reset_robot_motion(),
            "reset_error": lambda *args: self.reset_error(),
        }
