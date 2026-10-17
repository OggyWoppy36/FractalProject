# Mandelbrot Fractal Explorer

<img width="1200" height="800" alt="mandelbrot-screenshot (2)" src="https://github.com/user-attachments/assets/6b1f4154-fc65-4a32-9040-2d69eb27645f" />



A GPU-accelerated Mandelbrot renderer built in python using Taichi Lang for parallelization. Includes simple zooming with the cursor and the ability to save a screenshot of the current window.

### Features:
- Renders at high frame rates using the GPU
- Uses 64-bit floats and a dynamically updated iteration count to provide the best real-time accuracy possible
- Interactive controls (listed below)

### Controls:
- Esc: Quit
- Left-Click: Zoom in
- Right-Click: Zoom out
- 'h': Show/hide help window
- 's': Save current window as png
- 'r': Reset zoom
- 'c': Toggle fun mode (color)
- Zoom Speed Modifier Keys
  - \[No Key\]: Zoom Speed 1
  - Shift: Zoom Speed 2
  - Alt: Zoom Speed 3
  - Ctrl: Zoom Speed 4
 
### Requirements
- Python 3.13+
- A GPU (not required, but will run smoother)

### Installation
- Go to the [Releases](https://github.com/OggyWoppy36/FractalProject/releases) tab and download the appropriate release
- Run the .exe (or if not on Windows, unzip the file & run the source code)
- If Windows will likely flag it as unsafe the first time you run it:
  - Click 'More Info', then 'Run Anyway'

### Run from Source
1. Clone this repository and navigate to the project directory:
   ```bash
   git clone https://github.com/OggyWoppy36/FractalProject.git
   cd FractalProject
2. Create a virtual environment:
   ```bash
   py -3.13 -m venv venv
   .\venv\Scripts\Activate
3. Upgrade pip and install Taichi:
   ```bash
   python -m pip install --upgrade pip
   pip install taichi
5. Run the script:
   ```bash
   python mandelbrot.py

<img width="1200" height="800" alt="image" src="https://github.com/user-attachments/assets/9906f56c-c50f-4875-ab02-5677f9da2da7" />
