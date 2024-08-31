class MotorController:
    def __init__(self, view, parent_controller=None):
        """ Initialize the Robot Arm Controller

        Parameters
        ----------
        parent_controller : object
            The parent (e.g., main) controller object
        """

        # Initialize attributes
        self.view = view
        self.parent_controller = parent_controller

        # Get the variables and buttons from the view
        self.variables = self.view.get_variables()
        self.buttons = self.view.buttons

        self.buttons["import"].configure(command=self.test_connection)
        self.buttons["movetoloadingzone"].configure(command=self.MoveToLoadingZone)

    def test_connection(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "jog"
        )

    def home(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "home"
        )
        print("Homing Rotary Stage Motor")
        
    def setHomingVelocity(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "setHomingVelocity"
        )
    
    def MoveTo(self, position):
        """

        Parameters
        ----------
        position

        Returns
        -------

        """
        self.parent_controller.execute(
            "moveTo", position
        )
    
    def MoveToLoadingZone(self, position = 302.3):
        """

        Parameters
        ----------
        position

        Returns
        -------

        """
        text_input = self.buttons["input"].get(1.0, "end-1c")
        non_empty_text = text_input == ""
        if not non_empty_text:
            position = text_input
        self.parent_controller.execute(
            "moveTo", float(position)
        )
        
    def getPosition(self):
        """

        Returns
        -------

        """
        
        return self.parent_controller.execute(
            "position"
        )

    def disconnect(self):
        """

        Returns
        -------

        """
        self.parent_controller.execute(
            "disconnect"
        )
        print("Stage has disconnected")

    def MoveJog(self,position):
        """

        Parameters
        ----------
        position

        Returns
        -------

        """
        
        self.parent_controller.execute(
            "moveJog", position
        )
        print("Motor has finished Move Jog")
        

