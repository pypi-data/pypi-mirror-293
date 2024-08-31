import tkinter as tk
from tkinter import ttk

from navigate.view.custom_widgets.LabelInputWidgetFactory import LabelInput
from navigate.view.custom_widgets.validation import ValidatedSpinbox, ValidatedEntry

from autonomous_robotic_sample_handling.view.popups.inhouse_tools_popup import InHouseToolsPopup

class MoveSequence(tk.Frame):
    """MoveSequence

    MoveSequence is a frame that contains the widgets for initializing
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
        text_label = 'Move Sequence'
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Initializing Buttons
        self.buttons = {
            "offline_program": ttk.Button(self, text="Start program"),
            "automation_sequence": ttk.Button(self, text="Start automation sequence"),
            "process_sample": ttk.Button(self, text="Process a sample"),
            "in_house": ttk.Button(self, text="In House Tools"),
            "import": ttk.Button(self, text="Load Positions from Disk"),
        }
        counter = 0
        for key, button in self.buttons.items():
            if counter == 0:
                row, column = 0, 0
            elif counter == 1:
                row, column = 0, 1
            elif counter == 2:
                row, column = 0, 2
            elif counter == 3:
                row, column = 1, 1
            elif counter == 4:
                row, column = 1, 2

            button.grid(
                row=row, column=column, sticky=tk.NSEW, padx=(4, 1), pady=(4, 6)
            )
            counter += 1

        # Initialize Variables
        self.variables = {
            "current_sample_id": tk.IntVar(
                self,
                0
            ),
            "progress_bar_style": ttk.Style(),
            # TODO: Consider benefits of specifying a number_of_samples variable for the num_samples LabelInput
        }

        self.InHouseTools = InHouseToolsPopup(self)
        self.buttons.update(InHouseToolsPopup.get_buttons(self.InHouseTools))

        # Define styles for widgets
        self.variables['progress_bar_style'].layout('text.Horizontal.TProgressbar',
                                                    [('Horizontal.Progressbar.trough',
                                                      {'children': [('Horizontal.Progressbar.pbar',
                                                                     {'side': 'left', 'sticky': 'ns'})],
                                                       'sticky': 'nswe'}),
                                                     ('Horizontal.Progressbar.label', {'sticky': ''})])

        # Initialize Widgets
        self.inputs = {
            "num_samples": LabelInput(
                parent=self,
                label="Number of samples",
                input_class=ValidatedSpinbox,
                input_var=tk.IntVar(),
                input_args={"from_": 1, "to": 24, "increment": 1, "width": 5},
            ),
            "automation_progress": ttk.Progressbar(
                self,
                orient=tk.HORIZONTAL,
                mode="determinate",
                length=200,
                variable=self.variables['current_sample_id'],
                maximum=24,
                style='text.Horizontal.TProgressbar'
            )
        }
        self.inputs['num_samples'].grid(row=1, column=0, padx=(4, 1), pady=(4, 6))
        self.inputs['automation_progress'].grid(row=2, column=0, padx=(4, 1), pady=(4, 6))

    def get_buttons(self):
        return self.buttons

    def get_widgets(self):
        """Get Widgets.

        This function returns the dictionary that holds the widgets.

        The key is the widget name, value is the LabelInput class that has all the data.

        Parameters
        ----------
        self.inputs : dict
            Dictionary of all the widgets in the frame.
        """
        return self.inputs

    def get_variables(self):
        return self.variables
