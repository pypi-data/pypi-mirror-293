![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🧬 Tau Fibrils Yolo - Object detection in EM images

![screenshot](assets/screenshot.png)

We provide a [YoloV8](https://docs.ultralytics.com/) model for the detection of oriented bounding boxes (OBBs) of Tau fibrils in EM images.

[[`Installation`](#installation)] [[`Model`](#model)] [[`Usage`](#usage)] [[`Training`](#training)]

This project is part of a collaboration between the [EPFL Center for Imaging](https://imaging.epfl.ch/) and the [Laboratory of Biological Electron Microscopy](https://www.lbem.ch/).

## Installation

### As a standalone app

Download and run the latest installer from the [Releases](https://github.com/EPFL-Center-for-Imaging/tau-fibrils-yolo/releases) page.

### As a Python package

We recommend performing the installation in a clean Python environment. Install our package from PyPi:

```sh
pip install tau-fibrils-yolo
```

or from the repository:

```sh
pip install git+https://gitlab.com/center-for-imaging/tau-fibrils-object-detection.git
```

or clone the repository and install with:

```sh
git clone https://github.com/EPFL-Center-for-Imaging/tau-fibrils-yolo.git
cd tau-fibrils-yolo
pip install -e .
```

## Model

The model weights (6.5 Mb) are automatically downloaded from [this repository on Zenodo](https://sandbox.zenodo.org/records/99113) the first time you run inference. The model files are saved in the user home folder in the `.yolo` directory.

## Usage

**In Napari**

To use our model in Napari, start the viewer with

```sh
napari -w tau-fibrils-yolo
```

or open the Napari menu bar and select `Plugins > Tau fibrils detection`.

Open an image using `File > Open files` or drag-and-drop an image into the viewer window.

**Sample data**: To test the model, you can run it on our provided sample image. In Napari, open the image from `File > Open Sample > [TODO - add a sample image]`.


**As a library**

You can run the model to detect fibrils in an image (represented as a numpy array).

```py
from tau_fibrils_yolo import FibrilsDetector

detector = FibrilsDetector()

boxes, probabilities = detector.predict(your_image)
```

**As a CLI**

Run inference on an image from the command-line. For example:

```sh
tau_fibrils_predict_image -i /path/to/folder/image_001.tif
```

The command will save the segmentation next to the image:

```
folder/
    ├── image_001.tif
    ├── image_001_results.csv
```

Optionally, you can use the `-r` flag to also rescale the image by a given factor.

To run inference in batch on all images in a folder, use:

```sh
tau_fibrils_predict_folder -i /path/to/folder/
```

This will produce:

```
folder/
    ├── image_001.tif
    ├── image_001_results.csv
    ├── image_002.tif
    ├── image_002_results.csv
```

## Training

The instructions for training the model can be found [here](./scripts/instructions.md).

## Issues

If you encounter any problems, please file an issue along with a detailed description.

## License

This project is licensed under the [AGPL-3](LICENSE) license.

This project depends on the [ultralytics](https://github.com/ultralytics/ultralytics) package which is licensed under AGPL-3.

## Acknowledgements

We would particularly like to thank **Valentin Vuillon** for annotating the images on which this model was trained, and for developing the preliminary code that laid the foundation for this image analysis project. The repository containing his original version of the project can be found [here](https://gitlab.com/epfl-center-for-imaging/automated-analysis-tau-fibrils-project).