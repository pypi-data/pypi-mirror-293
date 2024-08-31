class ConstantVelocityAcquisitionController:
    def __init__(self, view, parent_controller=None):
        self.view = view
        self.parent_controller = parent_controller

        self.variables = self.view.get_variables()
        widgets = self.view.get_widgets()

        if (
            "ConstantVelocity"
            not in self.parent_controller.configuration["experiment"].keys()
        ):
            self.parent_controller.configuration["experiment"]["ConstantVelocity"] = {}
        parameter_config = self.parent_controller.configuration["experiment"][
            "ConstantVelocity"
        ]
        widget_names = ["start_position", "end_position", "step_size"]
        for widget_name in widget_names:
            self.variables[widget_name].trace_add(
                "write", self.update_value(widget_name)
            )
        self.variables["axis"].trace_add("write", self.update_axis)

        widgets["axis"].set(parameter_config.get("axis", "Z"))
        self.axis = self.variables["axis"].get()
        widgets["start_position"].set(parameter_config.get("start_position", 0))
        widgets["end_position"].set(parameter_config.get("end_position", 100))
        widgets["step_size"].set(parameter_config.get("step_size", 1))

        self.view.buttons["start_position"].configure(
            command=self.update_position("start_position")
        )
        self.view.buttons["end_position"].configure(
            command=self.update_position("end_position")
        )

    def update_value(self, widget_name):
        """Example function to move the plugin device"""

        def func(*args):
            try:
                value = float(self.variables[widget_name].get())
                self.parent_controller.configuration["experiment"]["ConstantVelocity"][
                    widget_name
                ] = value
            except (TypeError, ValueError):
                return

            start_position = self.parent_controller.configuration["experiment"][
                "ConstantVelocity"
            ]["start_position"]
            end_position = self.parent_controller.configuration["experiment"][
                "ConstantVelocity"
            ]["end_position"]
            step_size = self.parent_controller.configuration["experiment"][
                "ConstantVelocity"
            ]["step_size"]
            # calculate the estimated number of frames
            try:
                frame_number = abs(end_position - start_position) // step_size
            except:
                frame_number = 1
            self.variables["number_of_frames"].set(frame_number)
            self.parent_controller.configuration["experiment"]["ConstantVelocity"][
                "number_of_frames"
            ] = int(frame_number)

        return func

    def update_position(self, widget_name):
        def func(*args):
            self.variables[widget_name].set(
                self.parent_controller.configuration["experiment"]["StageParameters"][
                    self.axis.lower()
                ]
            )

        return func

    def update_axis(self, *args):
        self.parent_controller.configuration["experiment"]["ConstantVelocity"][
            "axis"
        ] = self.variables["axis"].get()

    def display_frame_number(self, frame_number):
        self.variables["number_of_frames"].set(frame_number)

    @property
    def custom_events(self):
        """dict: Custom events for this controller"""
        return {"ConstantVelocity-UpdateFrameNumber": self.display_frame_number}
