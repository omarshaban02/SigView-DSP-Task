# Multi-Port, Multi-Signal Channel Signal Viewer

## Description

Monitoring vital signals is crucial in any ICU room. The Multi-Port, Multi-Signal Channel Signal Viewer is a desktop application built with PyQt and Qt Designer. It provides a user-friendly interface for browsing and visualizing multiple signals for medical signals such as ECG, EMG, EEG, etc, or nonmedical signals on your desktop. This README file provides an overview of the application's features, usage, and setup.

![Application Screenshot](screenshots/app_screenshot.png)

## Features

- Browse your desktop to select the signals you want to view.
- Create a list of selected signals for plotting.
- Play, pause, stop, replay, zoom in, zoom out, and reset the view for each signal.
- Toggle the activation of individual signals with a single click.
- Double-click to toggle the activation status of all signals.
- Move signals between different port views.
- Synchronize two ports to view the same signals simultaneously.
- Apply control actions to the active signals in both ports.

## Usage

1. **Selecting Signals:**
   - Click the "Open" button to navigate your desktop and select the signals you want to view.
   - The selected signals will appear in a list.
     
2. **Ploting Selected Signals:**
   - Choose the signals you want to plot from the list
   - Click the "Plot" button to plot it on the graph.
     
3. **Signal Activation:**
   - Single-click on a signal at the graph to activate it to control it.
   - Single-click again to deactivate it.
   - Double-click in any place in the graph to deactivate all signals.

4. **Port Views:**
   - Move active signals between port views.
   - Synchronize two ports to view signals simultaneously.

5. **Control Actions:**
   - Use the control buttons (Play, Pause, Stop, Replay, Zoom In, Zoom Out, Reset View) to interact with the selected signals.
   - Control actions can be applied to active signals or all signals, depending on your selection.

## Setup

1. **Prerequisites:**
   - [List any prerequisites or dependencies here, including the versions of PyQt and Qt Designer you used.]

2. **Installation:**
   - [Provide installation instructions if applicable, e.g., how to install the application and any additional packages.]

3. **Running the Application:**
   - [Explain how to start and run the application.]

## Screenshots

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)
![Screenshot 3](screenshots/screenshot3.png)

## Contributing

- [Explain how others can contribute to your project, including guidelines for pull requests and code contributions.]

## License

- [Specify the project's license and any relevant copyright information.]

## Acknowledgments

- [Give credit to any third-party libraries, resources, or inspirations you used.]

## Contact

- [Provide your contact information for questions, feedback, or issues.]

---

<!--
 <h2>Features</h2>
The user can browse their PC to open any signal file. Each signal type should have examples of both normal and abnormal signals.
The application contains two main identical graphs. Each graph can display different signals, and the user can control each graph independently or link them together.
When a signal file is opened, it is displayed in cine mode, simulating a running signal over time.
The user can manipulate the running signals through various UI elements, including changing color, adding labels/titles, showing/hiding signals, controlling cine speed, zooming in/out, pausing/playing/rewinding signals, and scrolling/panning the signal in any direction.
Signals can be moved between graphs.
The application takes care of boundary conditions to ensure signals are displayed within appropriate ranges.
The user can generate reports of snapshots from the graphs, including data statistics such as mean, standard deviation, duration, minimum, and maximum values for each signal. The report is generated in PDF format directly from the code. -->
