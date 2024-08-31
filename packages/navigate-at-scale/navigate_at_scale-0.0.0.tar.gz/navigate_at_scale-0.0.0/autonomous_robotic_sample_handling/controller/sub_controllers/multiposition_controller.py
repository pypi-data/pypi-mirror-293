import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from pandastable import TableModel

class MultipositionController:
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
        self.table = self.view.multiposition.multipoint_list.pt

        self.table.loadCSV = self.load_positions
        self.table.exportCSV = self.export_positions
        self.table.insertRow = self.insert_row_func
        self.table.addStagePosition = self.add_stage_position

        
        self.variables = self.view.get_variables()
        self.buttons = self.view.buttons

        # #################################
        # ##### Example Widget Events #####
        # #################################

        self.view.MultipositionButtons.buttons['import'].config(
            command=self.load_positions    
        )
        self.view.MultipositionButtons.buttons['export'].config(
            command=self.export_positions
        )
        self.view.MultipositionButtons.buttons['add row'].config(
            command=self.insert_row_func
        )
        self.view.MultipositionButtons.buttons['add stage'].config(
            command=self.add_stage_position
        )

    def load_positions(self):       
        """Load a csv file.

        The valid csv file should contain the line of headers ['X', 'Y', 'Z', '1', '2', '3']

        Example
        -------
        >>> load_positions()
        """
        filename = filedialog.askopenfilenames(
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt")),
        )
        if not filename:
            return
        df = pd.read_csv(filename[0])
        print(df)
        # validate the csv file
        df.columns = map(lambda v: v.upper(), df.columns)
        cmp_header = df.columns == ["X", "Y", "Z", "1", "2", "3"]
        print(cmp_header)
        if not cmp_header.all():
            messagebox.showwarning(
                title="Warning",
                message="The csv file isn't right, it should contain [X, Y, Z, 1, 2,3]"
            )
            #logger.info("The csv file isn't right, it should contain [X, Y, Z, 1, 2, 3]")
            return
        model = TableModel(dataframe=df)
        self.table.updateModel(model)
        try:
            self.table.redraw()
        except KeyError:
            pass
        self.show_verbose_info("loaded csv file", filename)
    
    def export_positions(self):
        """Export the positions in the Multi-Position Acquisition Interface to a
        csv file.

        This function opens a dialog that let the user input a filename
        Then, it will export positions to that csv file

        Example
        -------
        >>> export_positions()
        """
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=(("CSV file", "*.csv"), ("Text file", "*.txt")),
        )
        if not filename:
            return
        self.table.model.df.to_csv(filename, index=False)
        self.show_verbose_info("exporting csv file", filename)  

    def insert_row_func(self):
        """Insert a row in the Multi-Position Acquisition Interface.

        Example
        -------
        >>> insert_row_func()
        """
        self.table.model.addRow(self.table.currentrow)
        self.table.update_rowcolors()
        self.table.redraw()
        self.table.tableChanged()
        self.show_verbose_info("insert a row before current row")

    def add_stage_position(self):
        """Add the current stage position to the Multi-Position Acquisition Interface.

        This function will get the stage's current position,
        Then add it to position list

        Example
        -------
        >>> add_stage_position()
        """
        position = self.parent_controller.execute("get_stage_position")
        self.append_position(position)