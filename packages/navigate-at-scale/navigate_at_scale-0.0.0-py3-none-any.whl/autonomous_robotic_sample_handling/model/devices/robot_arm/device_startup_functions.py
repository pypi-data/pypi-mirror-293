# Standard Imports
import os
from pathlib import Path

# Third party imports

# Local application imports
from navigate.tools.common_functions import load_module_from_file
from navigate.model.device_startup_functions import (
    device_not_found,
    DummyDeviceConnection,
    auto_redial
)

DEVICE_TYPE_NAME = "robot_arm"  # Same as in configuraion.yaml, for example "stage", "filter_wheel", "remote_focus_device"...
DEVICE_REF_LIST = ["type"]  # the reference value from configuration.yaml


def build_robot_arm_connection(configuration, mdr):
    """ Builds and returns a connection to the robot device

    Parameters
    ----------
    configuration : yaml
        Configuration data for the devices from .navigate/config/config.yaml
    mdr : mecademicpy.Robot
        Meca500 Robot object type

    Returns
    -------
    Robot object with corresponding device connection
    """
    # TODO: Set up import statement to occur within initial load_device.
    #  Avoid re-importing package
    robot_ip_address = configuration["ip_address"]
    enable_synchronous_mode = configuration["enable_synchronous_mode"]
    robot = mdr.Robot()
    robot.Connect(address=robot_ip_address,
                  enable_synchronous_mode=enable_synchronous_mode)
    return robot


def load_device(configuration, is_synthetic=False):
    """ Load the Robot Arm

    Parameters
    ----------
    configuration : dict
        The configuration for the Robot Arm
    is_synthetic : bool
        Whether the device is synthetic or not. Default is False.

    Returns
    -------
    object
        The device connection object corresponding to the Meca500 robot arm
    """
    if is_synthetic:
        device_type = "synthetic"
    else:
        # configuration["configuration"]["hardware"]
        device_type = configuration.get("type", "Meca500")

    if device_type == "Meca500":
        import mecademicpy.robot as mdr
        return auto_redial(
            build_robot_arm_connection,
            (configuration, mdr,),
            exception=Exception
        )

    elif device_type.lower() == "syntheticrobot" or device_type.lower() == "synthetic":
        return DummyDeviceConnection()


def start_device(microscope_name, device_connection, configuration, is_synthetic=False):
    """ Start the Robot Arm

    Parameters
    ----------
    microscope_name : str
        The name of the microscope
    device_connection : object
        The device connection object
    configuration : dict
        The configuration for the Robot Arm
    is_synthetic : bool
        Whether the device is synthetic or not. Default is False.

    Returns
    -------
    object
        The Robot Arm object
    """
    if is_synthetic:
        device_type = "synthetic"
    else:
        device_type = configuration["configuration"]["microscopes"][microscope_name]["robot_arm"]["hardware"]["type"]

    if device_type == "Meca500":
        robot_arm = load_module_from_file(
            "robot_arm",
            os.path.join(Path(__file__).resolve().parent, "robot_arm.py"),
        )
        return robot_arm.RobotArm(device_connection=device_connection)
    elif device_type == "synthetic":
        synthetic_device = load_module_from_file(
            "synthetic_device",
            os.path.join(Path(__file__).resolve().parent, "synthetic_device.py"),
        )
        return synthetic_device.SyntheticRobotArm(device_connection=device_connection)
    else:
        return device_not_found(microscope_name, device_type)
