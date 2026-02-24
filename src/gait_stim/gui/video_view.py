from __future__ import annotations

import cv2
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


def draw_pose(img: np.ndarray, kxy: np.ndarray, conf: np.ndarray) -> np.ndarray:
    out = img.copy()

    edges = [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7)]
    if len(kxy) >= 8 and len(conf) >= 8:
        for a, b in edges:
            if float(conf[a]) < 0.1 or float(conf[b]) < 0.1:
                continue
            p1 = (int(kxy[a][0]), int(kxy[a][1]))
            p2 = (int(kxy[b][0]), int(kxy[b][1]))
            cv2.line(out, p1, p2, (255, 200, 0), 2)

    for (x, y), c in zip(kxy, conf):
        if float(c) < 0.1:
            continue
        cv2.circle(out, (int(x), int(y)), 4, (0, 255, 0), -1)

    return out


def cv_to_pixmap(img_bgr: np.ndarray) -> QPixmap:
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]
    qimg = QImage(img_rgb.data, w, h, 3 * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg)


class VideoView(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setText("Video stream...")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)
        self.setMinimumSize(320, 180)
        self._last_pixmap: QPixmap | None = None

    def update_frame(self, img_bgr: np.ndarray) -> None:
        self._last_pixmap = cv_to_pixmap(img_bgr)
        self._apply_scaled()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._apply_scaled()

    def _apply_scaled(self) -> None:
        if self._last_pixmap is None:
            return

        target = self.size()
        if target.width() <= 1 or target.height() <= 1:
            return

        scaled = self._last_pixmap.scaled(
            target,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)
