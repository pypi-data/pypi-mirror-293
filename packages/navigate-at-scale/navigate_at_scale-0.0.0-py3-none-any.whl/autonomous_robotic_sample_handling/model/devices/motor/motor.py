# Standard Imports
import os
import time
from pathlib import Path

# Third party imports
import clr

# Local application imports
from navigate.tools.file_functions import load_yaml_file
from navigate.config.config import get_navigate_path

plugins_config_path = os.path.join(
        get_navigate_path(), "config", "plugins_config.yml"
    )
    
plugins_config = load_yaml_file(plugins_config_path)
plugin_path = plugins_config["Autonomous Robotic Sample Handling"]
    
dll_dir = os.path.join(plugin_path, 'API')

ref_DeviceManagerCLI = os.path.join(dll_dir, "Thorlabs.MotionControl.DeviceManagerCLI")
ref_GenericMotorCLI = os.path.join(dll_dir, "Thorlabs.MotionControl.GenericMotorCLI")
ref_StepperMotorCLI = os.path.join(dll_dir, "Thorlabs.MotionControl.Benchtop.StepperMotorCLI")

clr.AddReference(ref_DeviceManagerCLI)
clr.AddReference(ref_GenericMotorCLI)
clr.AddReference(ref_StepperMotorCLI)

# from Thorlabs.MotionControl.DeviceManagerCLI import BuildDeviceList
# from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import MotorDirection as MD
# from ThorLabs.MotionControl.GenericMotorCLI import Settings
# from ThorLabs.MotionControl.GenericMotorCLI import RotationDirections as RD
# from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor
from System import Decimal

class Motor:
    """Motor Class"""
    def __init__(self, device_connection, *args):
        """Initialize Motor

        Parameters
        ----------
        device_connection : object
            device connection object
        args : list
            arguments for the device
        """
        # DeviceManagerCLI.BuildDeviceList()
        motor_configuration = args[0]

        #: object: The device connection object
        self.device = device_connection

        # self.MotorDirection = MD
        self.MotorDirection = MD
        # self.RotationDirections = Settings.RotationSettings.RotationDirections
        # self.RotationMode = RD

        #: int: The timeout value in milliseconds
        self.timeoutVal = 100000

        #: str: The serial number
        self.serial_no = motor_configuration['hardware']['serial_no']

        #: object: The device channel
        self.channel = self.device.GetChannel(1)

        # Check if Controller Initializes Rotary Stage
        if not self.channel.IsSettingsInitialized():
            self.channel.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert self.channel.IsSettingsInitialized() is True

        # Start polling and enable
        self.channel.StartPolling(250)  # 250ms polling rate
        time.sleep(5)
        self.channel.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        #: object: The device information
        self.device_info = self.channel.GetDeviceInfo()
        print(self.device_info)
        print(self.device_info.Description)

        # Load any configuration settings needed by the controller/stage
        #: object: The channel configuration
        self.channel_config = self.channel.LoadMotorConfiguration(
            self.serial_no)  # If using BSC203, change serial_no to channel.DeviceID.

        #: object: The channel settings
        self.chan_settings = self.channel.MotorDeviceSettings

        self.channel.GetSettings(self.chan_settings)
        self.channel_config.DeviceSettingsName = 'HDR50'
        self.channel_config.UpdateCurrentConfiguration()
        self.channel.SetSettings(self.chan_settings, True, False)
        
        self.setHomingVelocity(20)
        
        self.home()

    def home(self):
        """Home the motor"""
        print("Homing Motor")
        # self.channel.SetRotationModes(self.RotationMode.RotationalRange,self.RotationDirection.Quickest)
        self.channel.Home(self.timeoutVal)
        print("finish homing")
        self.channel.ResetRotationModes()

    def MoveJog(self, MotorDirection):
        """Move the motor in the specified direction.

        Parameters
        ----------
        MotorDirection : str
            The direction to move the motor in
        """
         #Pass string or initialize MotorDirection.Forward/Backward outside?
         
        if MotorDirection == "Forward":
            self.channel.MoveJog(self.MotorDirection.Forward,self.timeoutVal)
        else:
            self.channel.MoveJog(self.MotorDirection.Backward,self.timeoutVal)
            
    def setHomingVelocity(self, velocity):
        self.channel.SetHomingVelocity(Decimal(velocity))

    def MoveTo(self, Position):
        """Move the motor to the specified position.

        Parameters
        ----------
        Position : int
            The position to move the motor to
        """
        print("moving")
        self.channel.MoveTo(Decimal(Position),self.timeoutVal)
        print("Moving success")

    def disconnect(self):
        """Disconnect the motor"""
        self.channel.StopPolling()
        self.device.Disconnect()
        
    def getPosition(self):
        """Get the motor position.

        Returns
        -------
        int
            The motor position
        """
        return self.channel.Position
    
    def SetJogStepSize(self, JogStepSize):
        """Set the jog step size.

        Parameters
        ----------
        JogStepSize : int
            The jog step size
        """
        self.channel.SetJogStepSize(Decimal(JogStepSize))
        
    def SetJogVelocityParams(self, JogVelocity,JogAccel):
        """Set the jog velocity parameters.

        Parameters
        ----------
        JogVelocity : int
            The jog velocity
        """
        self.SetJogVelocityParams(Decimal(JogVelocity),Decimal(JogAccel))
    
    @property
    def commands(self):
        """Return commands dictionary

        Returns
        -------
        commands : dict
            commands that the device supports
        """
        return {
            "home": lambda *args: self.home(),
            "disconnect": lambda *args: self.disconnect(),
            "moveJog": lambda *args: self.MoveJog(args[0]),
            "position": lambda *args: self.getPosition(),
            "moveTo": lambda *args: self.MoveTo(args[0]),
            "setHomingVelocity": lambda *args: self.setHomingVelocity(args[0])
        }