# Standard Library Imports
import logging
import tkinter as tk

# Third Party Imports

# Local Imports
from navigate.view.custom_widgets.popup import PopUp

# Logging Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


class InHouseToolsPopup(tk.Frame):
    """Popup for in house tools

    Parameters
    ----------
    root : object
        GUI root
    *args : object
        Arguments
    **kwargs : object
        Keyword arguments

    Attributes
    ----------
    popup : object
        Popup window
    inputs : dict
        Dictionary of inputs
    buttons : dict
        Dictionary of buttons

    Methods
    -------
    get_variables()
        Returns the variables
    get_buttons()
        Returns the buttons
    get_widgets()
        Returns the widgets

    """

    def __init__(self, root, *args, **kwargs):
        self.popup = PopUp(
            root,
            "In House Tools",
            "630x420+330+330",
            top=False,
            transient=False,
        )
        # Storing the content frame of the popup, this will be the parent of the widgets
        content_frame = self.popup.get_frame()

        # Formatting
        tk.Grid.columnconfigure(content_frame, "all", weight=1)
        tk.Grid.rowconfigure(content_frame, "all", weight=1)

        # Initializing Button
        self.buttons = {
            "input": tk.Text(content_frame, height=1, width=5),
            "height": tk.Text(content_frame, height=1, width=5),
            "connect": tk.Button(content_frame, text="Connect Robot"),
            "disconnect": tk.Button(content_frame, text="Disconnect Robot"),
            "home": tk.Button(content_frame, text='Home Robot and Motor'),
            "zero": tk.Button(content_frame, text="Zero Joints"),
            "opengripper": tk.Button(content_frame, text="Open Gripper"),
            "closegripper": tk.Button(content_frame, text="Close Gripper"),
            "movetoloadingzone": tk.Button(content_frame, text="Move Stage to Initial Loading Zone"),
        }

        counter = 0
        for key, button in self.buttons.items():
            if counter == 0:
                row, column = 0, 0
            elif counter == 1:
                row, column = 0, 1
            elif counter == 3:
                row, column = 0, 2
            elif counter == 4:
                row, column = 1, 0
            elif counter == 5:
                row, column = 1, 1
            elif counter == 6:
                row, column = 1, 2
            elif counter == 7:
                row, column = 2, 0
            elif counter == 8:
                row, column = 2, 1
            elif counter == 9:
                row, column = 2, 2

            button.grid(
                row=row, column=column, sticky=tk.NSEW, padx=(4, 1), pady=(4, 6)
            )
            counter += 1

    def get_buttons(self):
        return self.buttons