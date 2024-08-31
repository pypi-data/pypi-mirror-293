class SyntheticRobotArm:
    """ A synthetic robot arm for testing purposes """
    def __init__(self, device_connection, *args):
        """ Initialize the Synthetic Device

        Parameters
        ----------
        device_connection : object
            The device connection object
        args : list
            The arguments for the device
        """
        pass

    def jog(self):
        """ Zero the joints of the synthetic device """
        print("*** Synthetic motor receive command: jog")

    def disconnect(self):
        """ Disconnects the Mecademic Robot object from the robot and system"""
        print("*** Synthetic robot receive command: disconnect")

    def move_joints(self, a, b, c, d, e, f):
        """ Move Robot Joints.

        Parameters
        ----------
        a
        b
        c
        d
        e
        f
        """
        print("*** Synthetic robot receive command: move_joints")

    def move_pose(self, a, b, c, d, e, f):
        """ Move Robot Linearly """
        print("*** Synthetic robot receive command: disconnect")

    def delay(self, wait):
        """ Makes the Robot wait """
        print("*** Synthetic robot receive command: disconnect")

    def activate_and_home(self):
        """ Activates and Homes the Robot """
        print("*** Synthetic robot receive command: disconnect")

    @property
    def commands(self):
        """Return the commands for the synthetic device

        Returns
        -------
        commands : dict
            commands that the device supports
        """
        return {
            "jog": lambda *args: self.jog(),
        }
