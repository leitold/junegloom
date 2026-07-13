# June Gloom: pretty pictures from the Potts model

A simple script to produce some nice illustrations, based on an underlying Potts
model. Inspired by the work of [Bridget Riley](https://en.wikipedia.org/wiki/Bridget_Riley).

![Example picture](one.png)

Python dependencies:

* matplotlib
* numpy
* palettable (for nice color scales)
* pyaudio (for optionally reacting to live audio from the microphone)

In practice, I strongly suggest to use `uv`. It will take care of all the
dependencies.

## Run the simulation: static result images

Run the simulation with the settings defined inside the script. Three result
images will be generated: the random initial configuration and the final
configuration of the two separate simulation runs.

`uv run run_sim.py`

## Run the simulation: on-the-fly visualization

Similar to above, but instead of a fixed temperature, the temperature is slowly
increased and then decreased again. At the same time, the current state of the
simulation along with the current temperature is visualized along the way.

`uv run animation.py`

If you set `USE_AUDIO = True`, live audio captured from the microphone is used
to create a disturbance in the simulation. You can think of it as a crude
version of a music visualizer.

Feel free to play around with all the settings!
