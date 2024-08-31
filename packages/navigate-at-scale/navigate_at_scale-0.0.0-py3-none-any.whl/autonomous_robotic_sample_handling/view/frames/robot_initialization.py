import tkinter as tk
from tkinter import ttk


class RobotInitialization(tk.Frame):
    """RobotInitialization

    RobotInitialization is a frame that contains the widgets for initializing
    robot movement.

    Parameters
    ----------
    settings_tab : tk.Frame
        The frame that contains the settings tab.
    *args : tuple
        Variable length argument list.
    **kwargs : dict
        Arbitrary keyword arguments.

    Attributes
    ----------
    buttons : dict
        A dictionary of all the buttons that are tied to each widget name.
        The key is the widget name, value is the button associated.

    Methods
    -------
    """

    def __init__(self, settings_tab, *args, **kwargs):
        text_label = 'Robot Initialization'
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Initializing Button
        self.buttons = {
            "import": ttk.Button(self, text="Load Positions from Disk"),
            "connect": ttk.Button(self, text="Connect Robot"),
            "disconnect": ttk.Button(self, text="Disconnect Robot"),
            "move": ttk.Button(self, text='Move Robot'),
            "zero": ttk.Button(self, text="Zero Joints"),
            "opengripper": ttk.Button(self, text="Open Gripper"),
            "closegripper": ttk.Button(self, text="Close Gripper"),
            "movetoloadingzone": ttk.Button(self, text="Move Stage to Initial Loading Zone")
        }
        counter = 0
        for key, button in self.buttons.items():
            if counter == 0:
                row, column = 0, 0
            elif counter == 1:
                row, column = 0, 1
            elif counter == 2:
                row, column = 0, 2
                row, column = 1, 0
            elif counter == 3:
                row, column = 1, 1
            elif counter == 4:
                row, column = 2, 0
            elif counter == 5:
                row, column = 2, 1
            elif counter == 6:
                row, column = 3, 0
            elif counter == 7:
                row, column = 3, 1

            button.grid(
                row=row, column=column, sticky=tk.NSEW, padx=(4, 1), pady=(4, 6)
            )
            counter += 1

    def get_buttons(self):
        return self.buttons
