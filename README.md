# Project overview: Software for Infrastructure Objects Detection Using Machine Learning

This is my Bachelor's thesis at Petro Mohyla Black Sea National University, which consists of two parts:

- Training Building Segmentation Model
- Software Development

The software is a **desktop application** that detects infrastructure objects and displays them in a GUI built with **PyQt6**. It allows users to load satellite images, visualize detected features, and manage layer interactions.

The model is a **U-Net with ResNet34 backbone** which automatically detects **building footprints** from satellite images. The model performs **semantic segmentation**, identifying the exact pixels where buildings are located.

## Repository Structure

```bash
model-train/ (use this in a separate venv)
├── building_segmentation.ipynb
├── requirements.txt
src/
├── gui/
├── object_detection/
├── resources/
│   ├── demo_images/
│   ├── icons/
│   └── model/
├── utils/
└── main.py
tests/
└── test_gui.py
app.spec
build.sh
requirements.txt
setup.py
```

## Features

- Load and display satellite images
- Detect and overlay infrastructure objects
- Manage visual layers (add, remove, reorder)
- Simple and clean PyQt6 interface
- Modular design with separate logic and UI layers
- Includes automated tests for core GUI functionality
- Provides custom building segmentation model

<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWcydjFpYmExZ201c2t6ZTh4MHNtMjJtMHJ2aTZtdGw2eGVpYXJycyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/BqQWgP4tV1TU6Siiq7/giphy.gif" width="80%" height="80%"/>

## How to Build and Run the App

### Option 1: Run from Source

Clone the repository:

```bash
git clone https://github.com/MsRapunzel/software-for-infrastructure-objects-detection.git
cd software-for-infrastructure-objects-detection
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pip install pytest pytest-qt
PYTHONPATH=src pytest -s -v tests/test_gui.py
```

Run the application:

```
python src/main.py
```

### Option 2: Build a Standalone Executable

Clone the repository:

```bash
git clone https://github.com/MsRapunzel/software-for-infrastructure-objects-detection.git
cd software-for-infrastructure-objects-detection
```

Make `build.sh` executable:

```bash
chmod +x build.sh
```

Run build script:

```bash
./build.sh
```

The built app will appear in the `dist/` directory.

### Option 3: Use a GitHub Release

1. Go to the [Releases](https://github.com/MsRapunzel/software-for-infrastructure-objects-detection/releases) tab on GitHub (or open the [latest](https://github.com/MsRapunzel/software-for-infrastructure-objects-detection/releases/latest)).
2. Download `.dmg` for macOS.
3. Open the downloaded file, then drag and drop `.app` file to `/Applications` folder.

**Note:** On first launch macOS may block the app with warning: _"macOS cannot verify that this app is free from malware"_. In this case:

1. Press and hold _Control_ ^ and click the app, then select "Open" from the context menu.
2. Go to _System Settings > Privacy & Security_ and click "Open Anyway" if the app has appeared under _Security_.
