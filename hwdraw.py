from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image

HERE = Path(__file__).parent
ICONS = HERE / "icons"
OUT = HERE / "out"

FONT = "Liberation Sans"
plt.rcParams["font.family"] = FONT
plt.rcParams["svg.fonttype"] = "none"      # text stays text in the SVG

# ---------------------------------------------------------------- colours
INK = "#1A1A1A"        # device names
GREY = "#595959"       # models, notes
LIGHT = "#8C8C8C"
BLUE = "#0262A9"       # Huawei icon blue

ZONES = {   # fill, edge, line style
    "site":     ("#F5F8FC", "#9DB3CC", "-"),
    "dc":       ("#FCF7F1", "#D2A46E", "-"),
    "internet": ("#F8F5FB", "#A58BC2", "-"),
    "room":     ("#FFFFFF", "#A6A6A6", "-"),
    "floor":    ("#FAFAFA", "#C8C8C8", "-"),
    "group":    ("none",    "#B4B4B4", (0, (3, 2))),
    "shelter":  ("#F3F7F2", "#9DB89A", "-"),
    "vrf":      ("#FFFFFF", "#9DB3CC", "-"),
}

LINKS = {   # colour, width (pt), dash
    "isp":     ("#C55A11", 1.0, "-"),
    "ipsec":   ("#C55A11", 0.8, (0, (5, 2.5))),
    "fiberA":  ("#2E7D32", 1.5, "-"),
    "fiberB":  ("#2E7D32", 1.5, (0, (7, 2, 1.5, 2))),
    "uplink":  ("#404040", 0.8, "-"),
    "mlag":    ("#1F3864", 2.4, "-"),
    "pe":      ("#2E75B6", 1.0, "-"),
    "fw":      ("#C00000", 1.0, "-"),
    "server":  ("#9A9A9A", 0.6, "-"),
    "inet":    ("#7030A0", 1.2, "-"),
    "g5":      ("#7030A0", 0.9, (0, (1.5, 1.5))),
    "copper":  ("#404040", 0.6, "-"),
    "riserA":  ("#2E75B6", 1.2, "-"),
    "riserB":  ("#C00000", 1.2, (0, (5, 2.5))),
    "drop":    ("#7F7F7F", 0.5, "-"),
    "vrf":     ("#2E75B6", 0.7, "-"),
    "ibgp":    ("#7030A0", 0.7, (0, (3, 2))),
}

LEGEND_TEXT = {
    "isp": "ISP line", "ipsec": "IPsec tunnel (GRE + MPLS L3VPN inside)",
    "fiberA": "Fibre L4, circuit A (100GE)", "fiberB": "Fibre L4, circuit B (100GE)",
    "uplink": "Building / edge uplink", "mlag": "M-LAG peer-link / HRP / iStack",
    "pe": "PE, hub ↔ border leaf", "fw": "Firewall ↔ border leaf",
    "server": "Server link (2 × 25GE)", "inet": "Internet side (100GE)",
    "g5": "5G last resort", "copper": "Cat 6A copper",
    "double": "double line to a dashed frame = one link to each device of the pair",
}

_cache = {}


def _icon(name):
    if name not in _cache:
        p = ICONS / f"{name}.png"
        if not p.exists():
            raise FileNotFoundError(f"icon {name!r} not in {ICONS}")
        _cache[name] = Image.open(p).convert("RGBA")
    return _cache[name]


class Diagram:
    def __init__(self, w, h, name):
        self.w, self.h, self.name = w, h, name
        self.fig = plt.figure(figsize=(w / 25.4, h / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(h, 0)
        self.ax.axis("off")
        self.n = {}

    # ------------------------------------------------------------ text
    def text(self, x, y, s, size=6, color=INK, weight="normal", ha="left",
             va="center", bg=True, z=6, style="normal"):
        kw = dict(boxstyle="square,pad=0.15", fc="white", ec="none") if bg else None
        return self.ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                            ha=ha, va=va, zorder=z, bbox=kw, fontstyle=style,
                            linespacing=1.15)

    def note(self, x, y, s, size=5.3, color=GREY, ha="left", va="top", bg=False):
        return self.text(x, y, s, size=size, color=color, ha=ha, va=va, bg=bg)

    # ------------------------------------------------------------ zones
    def zone(self, x, y, w, h, title=None, sub=None, kind="site", title_size=6.6,
             title_pos="top", z=0, title_ha="left"):
        fc, ec, ls = ZONES[kind]
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.7, ls=ls, zorder=z))
        ty = y + 2.6 if title_pos == "top" else y + h - (5.4 if sub else 2.6)
        tx = x + 2 if title_ha == "left" else x + w - 2
        if title:
            self.text(tx, ty, title, size=title_size, weight="bold", bg=False, z=2, ha=title_ha)
        if sub:
            self.text(tx, ty + 2.8, sub, size=5.0, color=GREY, bg=False, z=2, ha=title_ha)

    def rail(self, x1, x2, y, h, title, sub="", color="#C55A11", fc="#FBF1EA", icon=None):
        """A provider network drawn as a horizontal bar; devices drop onto it."""
        self.ax.add_patch(Rectangle((x1, y - h / 2), x2 - x1, h, fc=fc, ec=color,
                                    lw=0.7, zorder=4))
        tx = x1 + 2
        self.text(tx, y, title, size=6.2, weight="bold", color=color, bg=False, z=5)
        if sub:
            self.text(tx + 2 + len(title) * 1.25, y, sub, size=5.0, color=GREY, bg=False, z=5)
        if icon:
            img = _icon(icon)
            ih = 8 * img.height / img.width
            self.ax.imshow(img, extent=(x1 - 10, x1 - 2, y + ih / 2, y - ih / 2), zorder=5)

    def dot(self, x, y, color=INK, r=0.55):
        from matplotlib.patches import Circle
        self.ax.add_patch(Circle((x, y), r, fc=color, ec="none", zorder=5))

    def box(self, x, y, w, h, fc="white", ec="#A6A6A6", lw=0.6, z=1, ls="-"):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))

    def hline(self, x1, x2, y, color="#C8C8C8", lw=0.5, ls=(0, (3, 2))):
        self.ax.plot([x1, x2], [y, y], color=color, lw=lw, ls=ls, zorder=0.5)

    # ------------------------------------------------------------ devices
    def node(self, key, x, y, icon, name=None, model=None, sub=None, size=10,
             pos="below", stack=1, name_size=6.2):
        img = _icon(icon)
        iw = size
        ih = size * img.height / img.width
        for k in range(stack - 1, -1, -1):          # stacked copies behind
            dx, dy = 1.4 * k, -1.4 * k
            self.ax.imshow(img, extent=(x - iw / 2 + dx, x + iw / 2 + dx,
                                        y + ih / 2 + dy, y - ih / 2 + dy),
                           zorder=3 + (stack - k) * 0.01, interpolation="lanczos",
                           alpha=1.0 if k == 0 else 0.55)
        self.n[key] = dict(x=x, y=y, w=iw, h=ih)
        lines = [(name, name_size, INK, "bold"), (model, name_size - 0.9, GREY, "normal"),
                 (sub, name_size - 1.2, GREY, "normal")]
        lines = [l for l in lines if l[0]]
        if not lines:
            return
        gap = 1.2
        if pos == "below":
            ty = y + ih / 2 + gap
            for s, fs, c, wt in lines:
                self.text(x, ty, s, size=fs, color=c, weight=wt, ha="center", va="top")
                ty += fs * 0.42 * (s.count("\n") + 1) + 0.5
        elif pos == "above":
            ty = y - ih / 2 - gap - 1.4 * (stack - 1)
            for s, fs, c, wt in reversed(lines):
                self.text(x, ty, s, size=fs, color=c, weight=wt, ha="center", va="bottom")
                ty -= fs * 0.42 * (s.count("\n") + 1) + 0.5
        else:   # right / left: block vertically centred on the icon
            ha = "left" if pos == "right" else "right"
            tx = x + iw / 2 + gap + 1.4 * (stack - 1) if pos == "right" else x - iw / 2 - gap
            hts = [fs * 0.42 * (s.count("\n") + 1) + 0.5 for s, fs, _, _ in lines]
            ty = y - sum(hts) / 2
            for (s, fs, c, wt), ht in zip(lines, hts):
                self.text(tx, ty, s, size=fs, color=c, weight=wt, ha=ha, va="top")
                ty += ht

    def cloud(self, key, x, y, label, sub=None, size=18, icon="network_cloud_2"):
        """Provider cloud: Huawei cloud icon with the name written on it."""
        self.node(key, x, y, icon, size=size)
        self.text(x, y + 0.6, label, size=6.4, color="white", weight="bold",
                  ha="center", bg=False, z=6)
        if sub:
            self.text(x, y + self.n[key]["h"] / 2 + 1.2, sub, size=5.0, color=GREY,
                      ha="center", va="top")

    def p(self, key, side=None, off=0.0):
        """Anchor point of a node: centre, or a side n/s/e/w shifted by off."""
        d = self.n[key]
        x, y = d["x"], d["y"]
        if side == "n":
            return (x + off, y - d["h"] / 2)
        if side == "s":
            return (x + off, y + d["h"] / 2)
        if side == "e":
            return (x + d["w"] / 2, y + off)
        if side == "w":
            return (x - d["w"] / 2, y + off)
        return (x + off, y)

    # ------------------------------------------------------------ links
    def line(self, pts, kind, z=1.5, lw=None, double=False):
        c, w, ls = LINKS[kind]
        if double:      # two parallel lines: one link to each device of a pair
            import math
            for sgn in (-1, 1):
                q = []
                for i, (x, y) in enumerate(pts):
                    a = pts[max(i - 1, 0)] if i else pts[0]
                    b = pts[min(i + 1, len(pts) - 1)] if i < len(pts) - 1 else pts[-1]
                    if i == 0:
                        a, b = pts[0], pts[1]
                    elif i == len(pts) - 1:
                        a, b = pts[-2], pts[-1]
                    else:
                        a, b = pts[i - 1], pts[i]
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L = math.hypot(dx, dy) or 1
                    q.append((x - dy / L * 0.55 * sgn, y + dx / L * 0.55 * sgn))
                xs, ys = zip(*q)
                self.ax.plot(xs, ys, color=c, lw=(lw or w) * 0.75, ls=ls, zorder=z,
                             solid_capstyle="butt")
            return
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=c, lw=lw or w, ls=ls, zorder=z,
                     solid_capstyle="butt", solid_joinstyle="miter")

    def group(self, key, x, y, w, h, label=None, ec="#7F7F7F"):
        """Dashed frame round a device pair (M-LAG, HRP, stack). A link drawn to
        the frame with double=True means one link to each member."""
        self.ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=ec, lw=0.6,
                                    ls=(0, (3, 2)), zorder=2))
        self.n[key] = dict(x=x + w / 2, y=y + h / 2, w=w, h=h)
        if label:
            self.text(x + w - 1.5, y + 2.2, label, size=4.8, color=GREY, ha="right", z=6)

    def link(self, a, b, kind, via=(), label=None, t=0.5, a_side=None, b_side=None,
             a_off=0.0, b_off=0.0, route=None, label_size=5.0, label_dx=0, label_dy=0,
             double=False):
        p1 = self.p(a, a_side, a_off) if isinstance(a, str) else a
        p2 = self.p(b, b_side, b_off) if isinstance(b, str) else b
        pts = [p1]
        if route == "hv":
            pts.append((p2[0], p1[1]))
        elif route == "vh":
            pts.append((p1[0], p2[1]))
        elif route == "vhv":        # down, across, down (mid y)
            my = (p1[1] + p2[1]) / 2
            pts += [(p1[0], my), (p2[0], my)]
        elif route == "hvh":
            mx = (p1[0] + p2[0]) / 2
            pts += [(mx, p1[1]), (mx, p2[1])]
        pts += list(via) + [p2]
        self.line(pts, kind, double=double)
        if label:
            # label on the longest segment at fraction t
            segs = list(zip(pts[:-1], pts[1:]))
            s = max(segs, key=lambda q: abs(q[1][0] - q[0][0]) + abs(q[1][1] - q[0][1]))
            lx = s[0][0] + (s[1][0] - s[0][0]) * t + label_dx
            ly = s[0][1] + (s[1][1] - s[0][1]) * t + label_dy
            self.tag(lx, ly, label, size=label_size, color=LINKS[kind][0])
        return pts

    def tag(self, x, y, s, size=5.0, color=GREY):
        """Link annotation: small text in a thin frame of the link colour."""
        self.ax.text(x, y, s, fontsize=size, color=color, ha="center", va="center",
                     zorder=7, bbox=dict(boxstyle="square,pad=0.25", fc="white",
                                         ec=color, lw=0.4))

    # ------------------------------------------------------------ legend
    def legend(self, kinds, x, y, w=None, extra=(), cols=None, size=5.3, gap=4):
        """Line and icon samples in a row at the bottom; wraps to a new row
        when the next item does not fit into width w."""
        items = [(k, LEGEND_TEXT.get(k, k)) if isinstance(k, str) else k for k in kinds]
        items += list(extra)
        w = w or (self.w - 2 * x)
        self.ax.plot([x, x + w], [y - 3.4, y - 3.4], color="#BFBFBF", lw=0.4, zorder=1)
        r = self.fig.canvas.get_renderer()
        mm_per_px = 25.4 / self.fig.dpi
        cx, cy = x, y
        for k, s in items:
            t = self.text(0, 0, s, size=size, color=GREY, bg=False)
            tw = t.get_window_extent(r).width * mm_per_px
            if cx + 10 + tw > x + w and cx > x:
                cx, cy = x, cy + 4.0
            t.set_position((cx + 10, cy))
            if k == "double":
                self.line([(cx, cy), (cx + 8, cy)], "uplink", double=True)
            elif k in LINKS:
                c, lw, ls = LINKS[k]
                self.ax.plot([cx, cx + 8], [cy, cy], color=c, lw=lw, ls=ls, zorder=2)
            else:
                img = _icon(k)
                ih = 5 * img.height / img.width
                self.ax.imshow(img, extent=(cx + 1.5, cx + 6.5, cy + ih / 2, cy - ih / 2), zorder=3)
            cx += 10 + tw + gap

    # ------------------------------------------------------------ output
    def save(self):
        OUT.mkdir(exist_ok=True)
        png = OUT / f"{self.name}.png"
        self.fig.savefig(png, dpi=300, facecolor="white")
        self.fig.savefig(OUT / f"{self.name}.svg", facecolor="white")
        plt.close(self.fig)
        print("saved", png.relative_to(HERE))
