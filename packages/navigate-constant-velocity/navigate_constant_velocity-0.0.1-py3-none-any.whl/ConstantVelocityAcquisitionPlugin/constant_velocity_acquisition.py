# Copyright (c) 2021-2022  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:

#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.

#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.

# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from navigate.tools.decorators import AcquisitionMode
from navigate.model.features.feature_related_functions import ConstantVelocityAcquisition


@AcquisitionMode
class ConstantVelocityAcquisitionMode:
    def __init__(self, name):
        self.acquisition_mode = name
        
        self.feature_list = [{"name": ConstantVelocityAcquisition}]

    def prepare_acquisition_controller(self, controller):
        """Prepare acquisition in controller side
        
        Parameters
        ----------
        controller : object
            navigate controller
        """
        controller.configuration["experiment"]["MicroscopeState"][
            "waveform_template"
        ] = "Constant-Velocity"
        # only supports per stack
        controller.configuration["experiment"]["MicroscopeState"][
            "stack_cycling_mode"
        ] = "per_stack"

    def end_acquisition_controller(self, controller):
        """Cleanup in controller side after acquisition
        
        Parameters
        ----------
        controller : object
            navigate controller
        """
        controller.configuration["experiment"]["MicroscopeState"][
            "waveform_template"
        ] = "Default"

    def update_saving_config(self, model):
        """Update saving configuration (set the shaping metadata)

        Parameters
        ----------
        model : object
            navigate model
        """
        return {
            "z": model.configuration["experiment"]["ConstantVelocity"][
                "number_of_frames"
            ]
        }
    
    def end_acquisition_model(self, model):
        """Model side cleanup after acquisition

        Parameters
        ----------
        model : object
            navigate model
        """
        axis = model.configuration["experiment"]["ConstantVelocity"]["axis"].lower()
        model.active_microscope.stages[axis].stop()
