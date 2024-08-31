<h1 align="center">
<img src="https://github.com/TheDeanLab/navigate-plugin-template/blob/main/plugin-icon.jpg" width="200" height="200"/>

navigate-constant-velocity-acquisition
	
<h2 align="center">
	A navigate plugin for imaging in a constant velocity format.
</h2>
</h1>

### Background

When acquiring large z-stacks, the time it takes to move the stage between slices can 
be a significant bottleneck. Often, stage movement is initiated with a serial command,
the stages accelerates, moves, and decelerates before sending a return serial 
command to notify the software that the stage has reached the desired position. 
Altogether, this can add a significant amount of time to each image acquisition, 
which accumulates over the course of a large z-stack.

### Approach

The **navigate-constant-velocity-acquisition** is a plugin for **navigate** which 
improves the image acquisition rate for large z-stacks by using a constant velocity
approach.  The plugin is designed to operate with Applied Scientific Instrumentation 
scan-optimized stages which maintain a constant velocity during long-range movements.
The [SCAN](https://asiimaging.com/docs/scan_module?s[]=sync) module is necessary.

The plugin will move the stages to a position before the start of the z-stack and 
trigger constant velocity movement. When the stage reaches the desired start 
position and is operating at the correct velocity, the stage triggers the operation 
of the software. The software then acquires images at the desired z-slice intervals
according to the stage velocity, camera integration and readout time, etc.
