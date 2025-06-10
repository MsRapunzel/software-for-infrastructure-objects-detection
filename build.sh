#!/bin/bash

# --- Environment Setup ---
ENV_NAME="buildvenv"
TEST_COMMAND="PYTHONPATH=src pytest -s -v tests/test_gui.py"

if [ ! -d "$ENV_NAME" ]; then
    echo "Creating new virtual environment: $ENV_NAME"
    python3 -m venv "$ENV_NAME"
else
    echo "Virtual environment '$ENV_NAME' already exists."
fi

echo "Activating virtual environment: $ENV_NAME"
source "$ENV_NAME/bin/activate"

echo "Installing/updating dependencies from requirements.txt"
pip install -r requirements.txt
pip install --upgrade pip

# --- Testing ---
pip install pytest==8.4.0
pip install pytest-qt==4.4.0

echo "Running tests..."
# cd "$TEST_DIR"
if ! eval $TEST_COMMAND; then
    echo "Tests failed! Aborting build."
    deactivate
    exit 1
fi
echo "Tests passed successfully!"

# --- Build Process ---
echo "Cleaning previous builds..."
rm -rf build dist

echo "Building the application with PyInstaller..."
pip install pyinstaller==6.14.1
pyinstaller app.spec

echo "Build process complete."

# --- Create DMG ---
if [ -d "dist/Infrastructure Objects Detector.app" ]; then
    echo "Creating DMG..."
    hdiutil create -volname "Infrastructure Objects Detector" -srcfolder "dist/Infrastructure Objects Detector.app" -ov -format UDZO "dist/Infrastructure Objects Detector.dmg"
else
    echo "Skipping DMG creation: .app bundle not found (build might have failed)."
fi

# --- Cleanup ---
echo "Cleaning up workspace..."
deactivate