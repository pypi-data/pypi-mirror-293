import tkinter as tk
from tkinter import filedialog, messagebox

class PausePlayController:
    """"""

    def __init__(self, view, parent_controller=None):
        """

        Parameters
        ----------
        view
        parent_controller
        """
        self.parent_controller = parent_controller
        self.view = view

        # self.variables = self.view.get_variables()
        self.buttons = self.view.buttons

        # #################################
        # ##### Example Widget Events #####
        # #################################

        self.buttons['pause'].configure(command=self.pause_motion)
        self.buttons['play'].configure(command=self.resume_motion)

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