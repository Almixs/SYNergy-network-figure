"""Drawing sheets (LLD) on A4 landscape: plan layer, legend, notes, tables, revisions, title block.

A sheet is 266 x 168 mm, the printable width and height of an A4 landscape page of the document,
so text keeps its point size in print: 5.5-7 pt text, 0.5-1.5 pt lines.
"""
import textwrap
from pathlib import Path

import cv2
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
from PIL import Image

from hwdraw import Diagram, GREY, INK

PLANS = Path(__file__).parent / "plans"

W, H = 266, 168
NAVY = "#1F3864"
RED = "#C00000"
PURPLE = "#7030A0"
BLUE = "#2E75B6"
ODF_FILL = "#FBE5D6"
RU_FILL = "#F2F6FB"


def plan_layer(name, k=3, gamma=1.35, white=()):
    """Plan layer of an earlier sheet issue, with every line made k px wider and the greys darker,
    so plan, trays and labels stay visible when the sheet is printed on A4."""
    a = np.array(Image.open(PLANS / name).convert("RGB"))
    for x0, y0, x1, y1 in white:
        a[y0:y1, x0:x1] = 255
    a = cv2.erode(a, np.ones((k, k), np.uint8))
    a = (255 * (a / 255.0) ** gamma).astype(np.uint8)
    return a


class Sheet(Diagram):
    def __init__(self, name):
        super().__init__(W, H, name)
        self.ax.add_patch(Rectangle((0.6, 0.6), W - 1.2, H - 1.2, fc="none", ec=INK, lw=1.0, zorder=0.5))

    # ------------------------------------------------------------ raster
    def image(self, arr, x, y, w):
        h = w * arr.shape[0] / arr.shape[1]
        self.ax.imshow(arr, extent=(x, x + w, y + h, y), zorder=0.8, interpolation="lanczos")
        return h

    # ------------------------------------------------------------ text helpers
    @staticmethod
    def wrap(s, w, size):
        n = max(10, int(w / (0.172 * size)))
        return textwrap.wrap(s, n)

    def heading(self, x, y, s, size=6.4):
        self.text(x, y, s, size=size, weight="bold", bg=False, va="center")

    def para(self, x, y, s, w, size=5.8, color=INK, lh=1.32):
        lines = self.wrap(s, w, size)
        step = size * 0.3528 * lh
        for i, l in enumerate(lines):
            self.text(x, y + i * step, l, size=size, color=color, bg=False, va="top")
        return len(lines) * step

    def panel(self, x, y, w, h, title=None, size=6.4):
        self.ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=0.6, zorder=1))
        if title:
            self.heading(x + 1.5, y + 2.6, title, size)
        return y + (5.2 if title else 1.5)

    def notes(self, x, y, w, h, items, size=5.8):
        yy = self.panel(x, y, w, h, "Notes")
        step = size * 0.3528 * 1.32
        for i, s in enumerate(items, 1):
            lines = self.wrap(s, w - 7, size)
            self.text(x + 1.5, yy, f"{i}.", size=size, bg=False, va="top")
            for j, l in enumerate(lines):
                self.text(x + 5, yy + j * step, l, size=size, bg=False, va="top")
            yy += len(lines) * step + 0.6
        return yy

    def table(self, x, y, cols, rows, size=5.6, rh=3.4, header=True, colors=None, align=None):
        """cols: widths in mm; rows: lists of cell texts (a cell may hold '\\n'); first row is the header."""
        yy = y
        for r, row in enumerate(rows):
            n = max(len(str(c).split("\n")) for c in row)
            h = rh + (n - 1) * size * 0.3528 * 1.2
            xx = x
            for c, (cw, cell) in enumerate(zip(cols, row)):
                fc = "#E8EDF4" if (header and r == 0) else "white"
                self.ax.add_patch(Rectangle((xx, yy), cw, h, fc=fc, ec=INK, lw=0.5, zorder=1))
                lines = str(cell).split("\n")
                for k, l in enumerate(lines):
                    ha = (align[c] if align else "left")
                    tx = xx + (cw / 2 if ha == "center" else 1.0)
                    ty = yy + h / 2 + (k - (len(lines) - 1) / 2) * size * 0.3528 * 1.2
                    self.text(tx, ty, l, size=size, bg=False, va="center", ha=ha,
                              weight="bold" if (header and r == 0) else "normal",
                              color=(colors[c] if colors and not (header and r == 0) else INK))
                xx += cw
            yy += h
        return yy

    def revisions(self, x, y, w, rows, size=5.6):
        self.heading(x, y + 1.6, "Revisions", size + 0.6)
        return self.table(x, y + 3.6, [9, 17, w - 26], [["Rev.", "Date", "Description"]] + rows, size=size,
                          align=["center", "center", "left"])

    def title_block(self, x, y, w, fields, size=5.8, lw=20, tsize=6.8, rh=3.6):
        yy = y
        for k, v in fields:
            big = k == "Title"
            lines = self.wrap(v, w - lw - 2, tsize) if big else [v]
            lstep = tsize * 0.3528 * 1.2
            h = rh + (len(lines) - 1) * lstep if big else rh
            self.ax.add_patch(Rectangle((x, yy), lw, h, fc="#F2F2F2", ec=INK, lw=0.5, zorder=1))
            self.ax.add_patch(Rectangle((x + lw, yy), w - lw, h, fc="white", ec=INK, lw=0.5, zorder=1))
            self.text(x + 1, yy + h / 2, k, size=size - 0.4, color=GREY, bg=False, va="center")
            for j, l in enumerate(lines):
                self.text(x + lw + 1, yy + h / 2 + (j - (len(lines) - 1) / 2) * lstep, l,
                          size=tsize if big else size, weight="bold" if big else "normal", bg=False, va="center")
            yy += h
        return yy

    def scalebar(self, x, y, mm_per_m, meters, ticks, size=5.6):
        L = mm_per_m * meters
        half = mm_per_m * ticks[len(ticks) // 2]
        self.ax.add_patch(Rectangle((x, y), half, 1.2, fc=INK, ec=INK, lw=0.5, zorder=2))
        self.ax.add_patch(Rectangle((x + half, y), L - half, 1.2, fc="white", ec=INK, lw=0.5, zorder=2))
        for t in ticks:
            self.text(x + t * mm_per_m, y + 3.2, str(t), size=size, ha="center", bg=False, va="center")
        self.text(x + L + 1.5, y + 0.6, "m", size=size, bg=False, va="center")

    # ------------------------------------------------------------ legend symbols
    def sym(self, kind, x, y):
        ax = self.ax
        if kind == "tray":
            for dy in (-0.45, 0.45):
                ax.plot([x, x + 9], [y + dy, y + dy], color=NAVY, lw=1.1, zorder=2)
        elif kind == "drop":
            ax.plot([x, x + 9], [y, y], color=NAVY, lw=0.7, zorder=2)
        elif kind == "apdrop":
            ax.plot([x, x + 9], [y, y], color=RED, lw=0.9, ls=(0, (1.2, 1.2)), zorder=2)
        elif kind == "outlet":
            ax.add_patch(Polygon([(x + 3, y - 1.3), (x + 6, y - 1.3), (x + 4.5, y + 1.3)], closed=True,
                                 fc="white", ec=INK, lw=0.8, zorder=2))
        elif kind in ("ap", "ap_purple", "ap_dashed"):
            col = PURPLE if kind == "ap_purple" else RED
            ax.add_patch(Circle((x + 4.5, y), 1.6, fc="white", ec=col, lw=0.9, zorder=2,
                                ls=(0, (1.5, 1)) if kind == "ap_dashed" else "-"))
            self.text(x + 4.5, y, "AP", size=4.2, color=col, ha="center", va="center", bg=False, z=3)
        elif kind == "idf":
            ax.add_patch(Rectangle((x + 2.5, y - 1.6), 4, 3.2, fc="white", ec=INK, lw=0.8, hatch="/////", zorder=2))
        elif kind == "routeA":
            ax.plot([x, x + 9], [y, y], color=NAVY, lw=1.6, zorder=2)
        elif kind == "routeB":
            ax.plot([x, x + 9], [y, y], color=RED, lw=1.6, ls=(0, (3, 1.5)), zorder=2)
        elif kind == "uplink":
            ax.plot([x, x + 9], [y, y], color=INK, lw=0.8, zorder=2)
        elif kind == "odf":
            ax.add_patch(Rectangle((x + 1, y - 1.5), 7, 3, fc=ODF_FILL, ec=NAVY, lw=0.8, zorder=2))
            self.text(x + 4.5, y, "ODF", size=4.4, ha="center", va="center", bg=False, weight="bold", z=3)
        elif kind == "ru":
            ax.add_patch(Rectangle((x + 1.5, y - 1.5), 6, 3, fc="white", ec=NAVY, lw=0.9, zorder=2))
            self.text(x + 4.5, y, "07", size=4.6, ha="center", va="center", bg=False, weight="bold", color=NAVY, z=3)
        elif kind == "riser":
            ax.add_patch(Rectangle((x + 2.8, y - 1.7), 3.4, 3.4, fc="white", ec=INK, lw=0.8, zorder=2))
            ax.plot([x + 2.8, x + 6.2], [y - 1.7, y + 1.7], color=INK, lw=0.7, zorder=3)
            ax.plot([x + 2.8, x + 6.2], [y + 1.7, y - 1.7], color=INK, lw=0.7, zorder=3)
        elif kind == "room":
            ax.add_patch(Ellipse((x + 4.5, y), 6, 3, fc="white", ec=INK, lw=0.8, zorder=2))
            self.text(x + 4.5, y, "12", size=4.6, ha="center", va="center", bg=False, z=3)

    def legend_panel(self, x, y, w, h, entries, size=5.8, step=4.3):
        yy = self.panel(x, y, w, h, "Legend") + 1.6
        for kind, label in entries:
            self.sym(kind, x + 1.5, yy)
            self.text(x + 13, yy, label, size=size, bg=False, va="center")
            yy += step
        return yy
