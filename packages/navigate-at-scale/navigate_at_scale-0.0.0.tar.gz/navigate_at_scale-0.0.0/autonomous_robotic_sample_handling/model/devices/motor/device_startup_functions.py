# Standard Imports
import os
from pathlib import Path
import time
import clr

# Third party imports

# Local application imports
from navigate.tools.common_functions import load_module_from_file
from navigate.tools.file_functions import load_yaml_file
from navigate.config.config import get_navigate_path
from navigate.model.device_startup_functions import (
    device_not_found,
    DummyDeviceConnection,
    auto_redial,
)

DEVICE_TYPE_NAME = "motor"  # Same as in configuration.yaml, for example "stage", "filter_wheel", "remote_focus_device"...
DEVICE_REF_LIST = ["type"]  # the reference value from configuration.yaml


def build_motor_connection(configuration, motor, motor_serial_no):
    motor.Connect(motor_serial_no)
    return motor


def load_device(configuration, is_synthetic=False):
    """ Load the Stepper Motor

    Parameters
    ----------
    configuration : dict
        The configuration for the Robot Arm
    is_synthetic : bool
        Whether the device is synthetic or not. Default is False.

    Returns
    -------
    object
        The device connection object
    """
    
    import os
    plugins_config_path = os.path.join(
        get_navigate_path(), "config", "plugins_config.yml"
    )
    
    plugins_config = load_yaml_file(plugins_config_path)
    plugin_path = plugins_config["Autonomous Robotic Sample Handling"]
    
    if is_synthetic:
        motor_type = "SyntheticMotor"
    else:
        # Can be Meca500, SyntheticRobot, syntheticrobot, Synthetic, synthetic
        motor_type = configuration.get("type", "HDR50")

    if motor_type == "HDR50":
        # TODO: Consider auto_redial function.
        motor_serial_no = configuration["serial_no"]

        dll_dir = os.path.join(plugin_path, 'API')

        ref_DeviceManagerCLI = os.path.join(dll_dir, "Thorlabs.MotionControl.DeviceManagerCLI.dll")
        ref_StepperMotorCLI = os.path.join(dll_dir, "Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")

        clr.AddReference(ref_DeviceManagerCLI)
        clr.AddReference(ref_StepperMotorCLI)
        
        from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
        from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor
        
        DeviceManagerCLI.BuildDeviceList()
        motor = BenchtopStepperMotor.CreateBenchtopStepperMotor(motor_serial_no)

        return auto_redial(
            build_motor_connection, (configuration, motor, motor_serial_no, ), exception=Exception
        )

    elif motor_type.lower() == "SyntheticMotor" or motor_type.lower() == "synthetic":
        return DummyDeviceConnection()


def start_device(microscope_name, device_connection, configuration, is_synthetic=False):
    """ Start the Robot ARm

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
        device_type = configuration["configuration"]["microscopes"][microscope_name]["motor"]["hardware"]["type"]

    if device_type == "HDR50":
        motor = load_module_from_file(
            "motor",
            os.path.join(Path(__file__).resolve().parent, "motor.py"),
        )
        return motor.Motor(device_connection, configuration["configuration"]["microscopes"][microscope_name]["motor"])
    elif device_type == "synthetic":
        synthetic_device = load_module_from_file(
            "synthetic_device",
            os.path.join(Path(__file__).resolve().parent, "synthetic_device.py"),
        )
        return synthetic_device.SyntheticRobotArm(device_connection, configuration["configuration"]["microscopes"][microscope_name]["motor"])
    else:
        return device_not_found(microscope_name, device_type)
