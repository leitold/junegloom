#!/usr/bin/env python3

import pyaudio

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.05


def plot_spectrum_and_return_axis(axis):
    axis.set_ylim([0.0, 1.0E0])
    ps_plot = axis.plot(ps, '*-', animated=True)[0]

    return ps_plot


def grab_audio_and_transform(audio):
    # stream = audio.open(
    #     format=FORMAT,
    #     channels=CHANNELS,
    #     rate=RATE,
    #     input=True,
    #     frames_per_buffer=CHUNK,
    # )

    # frames = []

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    SMALL_CHUNK = 800

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=SMALL_CHUNK,
    )

    data = stream.read(SMALL_CHUNK)

    stream.stop_stream()
    stream.close()

    # full = np.concatenate([np.frombuffer(frame, np.int16) for frame in frames])
    full = np.frombuffer(data, np.int16)
    ft = np.fft.rfft(full)
    ps = np.abs(ft)

    scaling = np.linspace(0.01, 2.0, len(ps))
    ps = ps * scaling

    ps = ps / ps.max()

    return ps


def update_plot(parameter_index):
    print(f"UPDATING {parameter_index}")

    ps = grab_audio_and_transform(audio)
    the_plot.set_ydata(ps)

    return [the_plot, ]


if __name__ == '__main__':
    audio = pyaudio.PyAudio()

    fig, axis = plt.gcf(), plt.gca()

    ps = grab_audio_and_transform(audio)

    the_plot = plot_spectrum_and_return_axis(axis)

    # Interval is the time between animation updates in ms. Set to larger value to slow everything down.
    ani = animation.FuncAnimation(
        fig,
        update_plot,
        range(10),
        interval=0,
        blit=True,
        repeat=True,
    )

    plt.show()

    audio.terminate()
