import tkinter as tk
from tkinter import filedialog, messagebox

class AutomationController:
    """ """

    def __init__(self, view, parent_controller=None):
        """

        Parameters
        ----------
        view
        parent_controller
        """
        self.parent_controller = parent_controller
        self.view = view

        self.widgets = self.view.get_widgets()
        self.buttons = self.view.buttons
        self.variables = self.view.variables

        # #################################
        # ##### Example Widget Events #####
        # #################################

        self.widgets['num_samples'].set("1")
        #TODO: Configure all widgets to be loaded using configuration file data

        self.reset_automation_variables()

    def pause_motion(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "pause_motion"
        )

    def resume_motion(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "resume_motion"
        )

    def get_num_samples(self):
        """

        Returns
        -------

        """
        return self.widgets['num_samples'].get()

    def reset_automation_variables(self):
        """

        Returns
        -------

        """
        self.variables['current_sample_id'].set(0)
        self.variables['progress_bar_style'].configure('text.Horizontal.TProgressbar', text=f'0/{self.get_num_samples()}')
        self.widgets['automation_progress']['maximum'] = self.get_num_samples()

    def update_progress_bar(self, current_sample_id):
        """

        Parameters
        ----------
        current_sample_id

        Returns
        -------

        """
        progress_bar = self.widgets['automation_progress']
        self.variables['current_sample_id'].set(current_sample_id)
        self.variables['progress_bar_style'].configure('text.Horizontal.TProgressbar',
                                                       text=f'{progress_bar["value"]}/{self.get_num_samples()}')
        self.view.update()
