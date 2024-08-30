import numpy as np
import pandas as pd
import napari
import napari.layers
from napari.utils.notifications import show_info
from napari.qt.threading import thread_worker
from PyQt5.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QWidget,
    QSizePolicy,
    QDoubleSpinBox,
    QFileDialog,
)
from matplotlib.backends.backend_qt5agg import FigureCanvas

from tau_fibrils_yolo.predict import FibrilsDetector
from tau_fibrils_yolo.postprocess import (
    boxes_kernel_density_map,
    minimum_neighbor_distance_filter,
    outside_image_border_filter,
    overlapping_obb_filter,
)
from tau_fibrils_yolo.measure import (
    box_measurements,
    line_profile_measurements,
    crossover_distance_measurement,
)

import matplotlib as mpl

mpl.rc("axes", edgecolor="white")
mpl.rc("axes", facecolor="#262930")
mpl.rc("axes", labelcolor="white")
mpl.rc("savefig", facecolor="#262930")
mpl.rc("text", color="white")
mpl.rc("xtick", color="white")
mpl.rc("ytick", color="white")


class YoloDetectorWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer
        self.predictor = FibrilsDetector()

        self.shapes_layer = None
        self.crossover_shapes_layer = None
        self.df = None

        # Layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        self.setLayout(grid_layout)

        # Image
        self.cb_image = QComboBox()
        self.cb_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(QLabel("Image", self), 0, 0)
        grid_layout.addWidget(self.cb_image, 0, 1)

        # Rescale factor
        self.bx_rescale = QDoubleSpinBox()
        self.bx_rescale.setMinimum(0.01)
        self.bx_rescale.setMaximum(100.0)
        self.bx_rescale.setSingleStep(0.05)
        self.bx_rescale.setValue(1.0)
        grid_layout.addWidget(QLabel("Rescale factor", self), 2, 0)
        grid_layout.addWidget(self.bx_rescale, 2, 1)

        # Compute button
        self.btn = QPushButton("Detect fibrils", self)
        self.btn.clicked.connect(self._start_detection)
        grid_layout.addWidget(self.btn, 3, 0, 1, 2)

        # Progress bar
        self.pbar = QProgressBar(self, minimum=0, maximum=1)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout.addWidget(self.pbar, 4, 0, 1, 2)

        self.cd_label = QLabel("Crossover distance: -", self)
        grid_layout.addWidget(self.cd_label, 5, 0, 1, 2)

        export_btn = QPushButton("Export results (.csv)", self)
        export_btn.clicked.connect(self._save_csv)
        grid_layout.addWidget(export_btn, 6, 0, 1, 2)

        # Line profile plot
        self.canvas = FigureCanvas()
        self.canvas.figure.set_tight_layout(True)
        self.canvas.figure.patch.set_facecolor("#262930")
        self.axes = self.canvas.figure.subplots()
        self.axes.cla()
        self.axes.set_ylabel("Intensity")
        self.axes.set_xlabel("Pixels")
        self.canvas.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.canvas.setMaximumSize(500, 300)
        self.canvas.setMinimumSize(300, 150)
        grid_layout.addWidget(self.canvas, 7, 0, 1, 2)

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._reset_shapes_layer)
        self._on_layer_change(None)

    def _on_layer_change(self, e):
        self.cb_image.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image):
                if x.data.ndim in [2, 3]:
                    self.cb_image.addItem(x.name, x.data)

    def _reset_shapes_layer(self, e):
        if (self.shapes_layer is not None) and not (self.shapes_layer in e.sources[0]):
            self.shapes_layer = None

    @thread_worker
    def _prediction_thread(self, rescale_factor):
        all_boxes = []
        all_probas = []
        for k, boxes, probas in self.predictor.yield_predictions(
            self.selected_image, rescale_factor
        ):
            all_boxes.extend(boxes)
            all_probas.extend(probas)
            yield k, boxes, probas

        all_boxes = np.array(all_boxes)
        all_probas = np.array(all_probas)

        return all_boxes, all_probas, rescale_factor

    def _start_detection(self):
        self.selected_image = self.cb_image.currentData()
        if self.selected_image is None:
            return

        if self.shapes_layer is not None:  # Note: How to properly delete a layer?
            self.shapes_layer.data = []
            self.shapes_layer = None

        if self.crossover_shapes_layer is not None:
            self.crossover_shapes_layer.data = []
            self.crossover_shapes_layer = None

        rescale_factor = self.bx_rescale.value()

        worker = self._prediction_thread(rescale_factor)

        worker.yielded.connect(self._update_viewer)
        worker.yielded.connect(lambda payload: self.pbar.setValue(payload[0]))
        worker.returned.connect(lambda _: self.pbar.setMaximum(1))
        worker.returned.connect(self._load_in_viewer)
        n_crops = self.predictor.n_crops(self.selected_image, rescale_factor)
        self.pbar.setMaximum(n_crops)
        self.pbar.setValue(0)
        worker.start()

    def _update_viewer(self, payload):
        _, boxes, probas = payload

        if len(boxes) == 0:
            return

        if self.shapes_layer is None:
            shape_kwargs = {
                "shape_type": "rectangle",
                "name": "Tau fibrils (Yolo)",
                "face_color": "transparent",
                "opacity": 1.0,
                "edge_width": 1,
                "edge_color": "#ff0000",
            }

            self.shapes_layer = self.viewer.add_shapes(boxes, **shape_kwargs)
            self.shapes_layer.mouse_double_click_callbacks.append(
                self._handle_double_click
            )
            self.shapes_layer.mode = "DIRECT"
        else:
            # Update the layer data
            current_data = self.shapes_layer.data
            current_data.extend(boxes)
            self.shapes_layer.data = current_data
            self.shapes_layer.refresh()

    def _load_in_viewer(self, payload):
        """Callback from thread returning."""
        boxes, probas, rescale_factor = payload

        if len(boxes):
            filt = outside_image_border_filter(boxes)
            boxes = boxes[filt]
            probas = probas[filt]

            filt = overlapping_obb_filter(boxes)
            boxes = boxes[filt]
            probas = probas[filt]

            filt = minimum_neighbor_distance_filter(boxes, rescale_factor)
            boxes = boxes[filt]
            probas = probas[filt]

        if len(boxes) == 0:
            show_info("No fibrils were detected.")
            return

        density_map = boxes_kernel_density_map(boxes, self.selected_image)

        density_layer = self.viewer.add_image(
            density_map, colormap="inferno", opacity=0.5, blending="additive"
        )
        density_layer.visible = False
        self.viewer.layers.selection.active = self.shapes_layer

        probas = list(probas)

        # Get the lines and crossover distances
        centers_x = []
        centers_y = []
        lengths = []
        widths = []
        for box in boxes:
            center, length, width = box_measurements(box)
            centers_x.append(center[0])
            centers_y.append(center[1])
            lengths.append(length)
            widths.append(width)

        self.shapes_layer.data = boxes
        self.shapes_layer.properties = {
            "probability": probas,
            "length": lengths,
            "width": widths,
            "center_x": centers_x,
            "center_y": centers_y,
        }

        self.shapes_layer.edge_color = "#00ff00"
        self.shapes_layer.refresh()

        self.df = pd.DataFrame(
            {
                "probability": probas,
                "length": lengths,
                "width": widths,
                "center_x": centers_x,
                "center_y": centers_y,
            }
        )

    def _save_csv(self):
        if self.df is None:
            print("No detection data found.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save as CSV", ".", "*.csv")
        if not filename.endswith(".csv"):
            filename += ".csv"

        self.df.to_csv(filename)
        print(f"Saved {filename}!")

    def _handle_double_click(self, *args, **kwargs):
        if self.shapes_layer.mode in ["direct", "select"]:
            selected_data = self.shapes_layer.selected_data
            if len(selected_data) == 1:
                selected_shape_idx = list(self.shapes_layer.selected_data)[0]
                boxes = self.shapes_layer.data
                image = self.cb_image.currentData()
                box = boxes[selected_shape_idx]
                line_profile_width, line_profile_centerline = line_profile_measurements(box, image)
                crossover_distance = crossover_distance_measurement(box, image)
                crossover_distance_centerline = crossover_distance_measurement(box, image, method="centerline")
                self._draw(line_profile_width, line_profile_centerline, crossover_distance, crossover_distance_centerline)

    def _draw(self, line_profile_width, line_profile_centerline, crossover_distance, crossover_distance_centerline):
        self.axes.cla()
        self.axes.plot(line_profile_width, label=f"box_width (crossover_dist: {crossover_distance:.0f} px)")
        self.axes.plot(line_profile_centerline, color="orange", label=f"centerline (crossover_dist: {crossover_distance_centerline:.0f} px)")
        self.axes.set_ylabel("Intensity")
        self.axes.set_xlabel("Pixels")
        self.axes.set_xlim(0, len(line_profile_width))
        self.axes.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=1)
        self.canvas.draw()
