# Standard Imports
import tkinter as tk
from tkinter import ttk

from navigate.view.custom_widgets.validation import ValidatedSpinbox
from navigate.view.custom_widgets.LabelInputWidgetFactory import LabelInput


class ConstantVelocityAcquisitionFrame(ttk.Frame):
    """Plugin Frame: Just an example

    This frame contains the widgets for the plugin.
    """

    def __init__(self, root, *args, **kwargs):
        """Initilization of the  Frame

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

        label = ttk.Label(self, text="Stage Axis :")
        label.grid(row=0, column=0, sticky=tk.NW, padx=(20, 5), pady=10)

        self.variables["axis"] = tk.StringVar()
        self.inputs["axis"] = ttk.Combobox(self, textvariable=self.variables["axis"])
        self.inputs["axis"]["values"] = ("X", "Y", "Z", "F", "Theta")
        self.inputs["axis"].state(["readonly"])
        self.inputs["axis"].grid(row=0, column=1, sticky="N", padx=5, pady=10)

        labels = ["Start Position", "End Position", "Step Size", "Number of Frames"]
        input_names = [
            "start_position",
            "end_position",
            "step_size",
            "number_of_frames",
        ]
        for i in range(len(labels)):
            label = ttk.Label(self, text=labels[i] + " :")
            label.grid(row=i + 1, column=0, padx=(20, 5), pady=10, sticky=tk.NW)

            self.variables[input_names[i]] = tk.StringVar()
            self.inputs[input_names[i]] = ValidatedSpinbox(
                self, textvariable=self.variables[input_names[i]]
            )
            self.inputs[input_names[i]].grid(
                row=i + 1, column=1, sticky="N", padx=5, pady=10
            )
            self.inputs[input_names[i]].config(from_=-1000, to=1000, increment=1)
        self.inputs["step_size"].config(from_=0, to=1000, increment=0.1)
        self.inputs["number_of_frames"]["state"] = "disabled"

        self.buttons["start_position"] = ttk.Button(
            self, text="Set Position", padding=(10, 0)
        )
        self.buttons["end_position"] = ttk.Button(
            self, text="Set Position", padding=(10, 0)
        )
        self.buttons["start_position"].grid(row=1, column=2, padx=(5, 20))
        self.buttons["end_position"].grid(row=2, column=2, padx=(5, 20))

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
