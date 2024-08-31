# Standard Imports
import tkinter as tk
from tkinter import ttk
# import logging

# from autonomous_robotic_sample_handling.view.frames.robot_initialization import
# RobotInitialization
from autonomous_robotic_sample_handling.view.frames.move_sequence import MoveSequence
from autonomous_robotic_sample_handling.view.frames.multiposition_frame import MultiPositionTab, MultipositionButtons


class AutonomousRoboticSampleHandlingFrame(ttk.Frame):
    """Plugin Frame: Just an example

    This frame contains the widgets for the plugin.
    """

    def __init__(self, root, *args, **kwargs):
        """Initialization of the  Frame

        Parameters
        ----------
        root : tkinter.ttk.Frame
            The frame that this frame will be placed in.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        ttk.Frame.__init__(self, root, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Dictionary for widgets and buttons
        #: dict: Dictionary of the widgets in the frame
        self.inputs = {}
        self.buttons = {}
        self.variables = {}

        # #################################
        # ######## Example Widgets ########
        # ##### add your widgets here #####
        # #################################

        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # # Robot Initialization Buttons
        # self.robot_init = RobotInitialization(self)
        # self.robot_init.grid(
        #     row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        # )
        # self.buttons.update(RobotInitialization.get_buttons(self.robot_init))

        # Automation Program Buttons
        self.move_sequence = MoveSequence(self)
        self.move_sequence.grid(
            row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        self.buttons.update(MoveSequence.get_buttons(self.move_sequence))

        # Multiposition Table Buttons
        self.MultipositionButtons = MultipositionButtons(self)
        self.MultipositionButtons.grid(
            row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )

        # Multiposition Table
        self.multiposition = MultiPositionTab(self)
        self.multiposition.grid(
            row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )

    # Getters
    def get_variables(self):
        """Returns a dictionary of the variables for the widgets in this frame.

        The key is the widget name, value is the variable associated.

        Returns
        -------
        variables : dict
            Dictionary of the variables for the widgets in this frame.
        """
        return self.variables

    def get_widgets(self):
        """Returns a dictionary of the widgets in this frame.

        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.inputs : dict
            Dictionary of the widgets in this frame.
        """
        return self.inputs
