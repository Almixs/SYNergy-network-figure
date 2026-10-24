"""Fig. 15 Sheet SYN-LLD-A1-002: FTTO fibre riser, ELV rooms and central ports (administrative building S1-A1).

Source: FTTO Design of the document (Table 23, central ports; Table 27 port names), 28 RUs per floor (task V3).
"""
from matplotlib.patches import Rectangle

from hwdraw import GREY, INK
from lldsheet import NAVY, ODF_FILL, RED, RU_FILL, W, Sheet

s = Sheet("fig15_ftto_riser")
ax = s.ax

RA, RB = 46, 160          # riser axes (mm)
FLOORS = [("FLOOR 4", "FFL +9.0 m"), ("FLOOR 3", "FFL +6.0 m"), ("FLOOR 2", "FFL +3.0 m"), ("FLOOR 1", "FFL +0.0 m")]
FH = 22.5                 # floor band height
Y0 = 6


def box(x, y, w, h, fc="white", ec=NAVY, lw=0.9, z=2, ls="-"):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))


# risers
for x, name in ((RA, "RISER A"), (RB, "RISER B")):
    box(x - 3, Y0 + 1, 6, 4 * FH + 9, fc="none", ec=INK, lw=0.6, ls=(0, (3, 2)), z=1)
    s.text(x, Y0 - 1.6, name, size=6.2, weight="bold", ha="center", bg=False)

for i, (fl, ffl) in enumerate(FLOORS):
    y = Y0 + i * FH
    if i:
        ax.plot([4, 186], [y, y], color="#7F8FA6", lw=0.6, ls=(0, (6, 3)), zorder=0.9)
    s.text(5, y + 4, fl, size=7, weight="bold", bg=False)
    s.text(5, y + 8, ffl, size=5.8, color=GREY, bg=False)
    cy = y + 12
    # floor boxes
    box(RA - 13, cy - 2.2, 9, 4.4, fc=ODF_FILL, ec=NAVY)
    s.text(RA - 8.5, cy, "ODF-A", size=5.8, weight="bold", ha="center", bg=False, z=3)
    box(RB + 4, cy - 2.2, 9, 4.4, fc=ODF_FILL, ec=RED)
    s.text(RB + 8.5, cy, "ODF-B", size=5.8, weight="bold", ha="center", bg=False, z=3, color=RED)
    # room units of the floor
    box(82, cy - 5, 42, 10, fc=RU_FILL, ec=NAVY)
    s.text(103, cy - 1.6, "28 × RU · rooms 1–26", size=6.2, weight="bold", ha="center", bg=False, z=3)
    s.text(103, cy + 2, "RU 01–28 = ODF ports 01–28", size=5.6, ha="center", bg=False, z=3, color=GREY)
    # drops
    ax.plot([RA - 4, 82], [cy - 2.5, cy - 2.5], color=NAVY, lw=1.2, zorder=1.8)
    s.text(63, cy - 4.4, "28 × duplex OS2 (CT-A)", size=5.4, color=NAVY, ha="center", bg=False)
    ax.plot([124, RB + 4], [cy + 1.5, cy + 1.5], color=RED, lw=1.2, ls=(0, (4, 2)), zorder=1.8)
    s.text(142, cy + 4.2, "28 × duplex OS2 (CT-B)", size=5.4, color=RED, ha="center", bg=False)
    # riser cables down to the ELV rooms
    ax.plot([RA - 4, RA - 1.5 + i * 0.9, RA - 1.5 + i * 0.9], [cy + 0.6, cy + 0.6, 106], color=NAVY, lw=1.0, zorder=1.7)
    ax.plot([RB + 4, RB + 1.5 - i * 0.9, RB + 1.5 - i * 0.9], [cy - 0.6, cy - 0.6, 106], color=RED, lw=1.0,
            ls=(0, (4, 2)), zorder=1.7)
    if fl == "FLOOR 2":
        s.text(RA + 4, cy + 5.6, "3 × 72f OS2 G.657.A2,\none per floor 2–4", size=5.3, color=NAVY, bg=False, va="top")
        s.text(RB - 4, cy + 5.6, "3 × 72f OS2 G.657.A2,\none per floor 2–4", size=5.3, color=RED, bg=False, va="top",
               ha="right")
s.text(103, Y0 + 4 * FH - 2.2, "floor 1 boxes patch straight into ODF-R1 / ODF-R2", size=5.3, color=GREY,
       ha="center", bg=False)

# ELV rooms
ax.plot([4, 186], [Y0 + 4 * FH + 2, Y0 + 4 * FH + 2], color="#7F8FA6", lw=0.6, ls=(0, (6, 3)), zorder=0.9)
EY = 106
for x0, room, side, odf, ftn, agg, col in ((6, "ELV ROOM 1", "A", "ODF-R1", "S1-A1-FT1", "S1-A1-AGG-A", NAVY),
                                            (110, "ELV ROOM 2", "B", "ODF-R2", "S1-A1-FT2", "S1-A1-AGG-B", RED)):
    box(x0, EY, 76, 36, fc="#FAFAFA", ec=INK, lw=1.0, z=1)
    s.text(x0 + 1.5, EY + 2.8, f"{room} · 42U rack, UPS 4 h, A/C N+1", size=6.2, weight="bold", bg=False)
    ox = x0 + 4 if side == "A" else x0 + 50
    box(ox, EY + 6, 22, 7.5, fc=ODF_FILL, ec=col)
    s.text(ox + 11, EY + 8.6, odf, size=6, weight="bold", ha="center", bg=False, z=3, color=col)
    s.text(ox + 11, EY + 11.5, "riser panel 4 × 72f LC", size=5.2, ha="center", bg=False, z=3, color=GREY)
    fx = x0 + 34 if side == "A" else x0 + 4
    for k in range(3):
        fy = EY + 7 + k * 6
        box(fx, fy, 38, 4.8, fc=RU_FILL, ec=NAVY)
        s.text(fx + 19, fy + 2.4, f"{ftn}-{k + 1} · S6730-H48X6C-V2", size=5.6, weight="bold", ha="center",
               bg=False, z=3)
        # patch from the riser panel to the FTTO switch
        px = ox + 22 if side == "A" else ox
        ax.plot([px, px + (3 if side == "A" else -3), px + (3 if side == "A" else -3),
                 fx if side == "A" else fx + 38],
                [EY + 9.75, EY + 9.75, fy + 2.4, fy + 2.4], color=col, lw=0.8, zorder=1.6)
    ax_ = x0 + 4 if side == "A" else x0 + 46
    box(ax_, EY + 27, 26, 7, fc="#E8EDF4", ec=NAVY, lw=1.1)
    s.text(ax_ + 13, EY + 29.4, agg, size=6, weight="bold", ha="center", bg=False, z=3)
    s.text(ax_ + 13, EY + 32.2, "S6750-H48Y8C", size=5.3, color=GREY, ha="center", bg=False, z=3)
    # local 10GE uplinks of the three FTTO switches
    lx = fx if side == "A" else fx + 38
    ax.plot([lx, lx + (-2 if side == "A" else 2), lx + (-2 if side == "A" else 2), ax_ + (26 if side == "A" else 0)],
            [EY + 21.4, EY + 21.4, EY + 30.5, EY + 30.5], color=INK, lw=0.8, zorder=1.6)
    s.text(72 if side == "A" else 120, EY + 26.4, "3 × 10GE to the local AGG\n(10GE1/0/47)", size=5.2, ha="right" if side == "A" else "left", bg=False, color=GREY)
    # core
    cx = x0 + 8 if side == "A" else x0 + 48
    box(cx, EY + 44, 26, 8, fc="white", ec=INK, lw=0.9)
    s.text(cx + 13, EY + 46.6, f"S1-CORE-{side}", size=6, weight="bold", ha="center", bg=False, z=3)
    s.text(cx + 13, EY + 49.6, f"site core room {side} · 2 × 25GE", size=5.2, color=GREY, ha="center", bg=False, z=3)
    ax.plot([ax_ + 13, ax_ + 13, cx + 13, cx + 13], [EY + 34, EY + 39, EY + 39, EY + 44], color=INK, lw=0.9, zorder=1.6)

# peer-link and crossed uplinks between the rooms
ax.plot([36, 156], [EY + 30, EY + 30], color=NAVY, lw=2.2, zorder=1.5)
s.text(96, EY + 28.4, "M-LAG peer-link 2 × 100GE (both risers)", size=5.4, ha="center", bg=True, color=NAVY)
ax.plot([74, 74, 160, 160], [EY + 23.8, EY + 38.5, EY + 38.5, EY + 34], color=INK, lw=0.7, ls=(0, (2, 1.5)), zorder=1.4)
ax.plot([118, 118, 26, 26], [EY + 23.8, EY + 40.5, EY + 40.5, EY + 34], color=INK, lw=0.7, ls=(0, (2, 1.5)), zorder=1.4)
s.text(96, EY + 37.3, "3 × 10GE: FT1-1…3 → AGG-B (10GE1/0/48)", size=5.2, ha="center", bg=True, color=GREY)
s.text(96, EY + 42.1, "3 × 10GE: FT2-1…3 → AGG-A (10GE1/0/48)", size=5.2, ha="center", bg=True, color=GREY)

# central ports
s.heading(46, 152, "Central ports · RU k of floor f → switch s = ceil(k / 10), port 10GE1/0/(10(f−1) + k − 10(s−1))", 5.8)
s.table(46, 154.5, [12, 33, 33, 33],
        [["", "FT-1 (RU 01–10)", "FT-2 (RU 11–20)", "FT-3 (RU 21–28)"],
         ["F1–F4", "10GE1/0/1–10, 11–20, 21–30, 31–40", "10GE1/0/1–10, 11–20, 21–30, 31–40",
          "10GE1/0/1–8, 11–18, 21–28, 31–38"],
         ["used", "40 RU + 2 up = 42 / 48", "40 RU + 2 up = 42 / 48", "32 RU + 2 up = 34 / 48"]],
        size=5.2, rh=3.4, align=["center", "center", "center", "center"])

# right panel
X = 190
RW = W - X - 3
s.legend_panel(X, 4, RW, 25, [("routeA", "route A: CT-A, riser A, ELV room 1"),
                               ("routeB", "route B: CT-B, riser B, ELV room 2"),
                               ("uplink", "10GE / 25GE / 100GE links"),
                               ("odf", "floor box or riser panel (ODF)")], step=4.2)
s.notes(X, 31, RW, 46, [
    "Schematic, not to scale: two risers by the lift cores (A between blocks E–F, B between F–G).",
    "Every floor: ODF-A and ODF-B with 28 duplex drops each (one per RU); one 72-fibre OS2 cable per floor and "
    "riser runs down to the riser panel ODF-R1 or ODF-R2 in its ELV room.",
    "ELV room 1 (riser A) and ELV room 2 (riser B) are on floor 1, each with its own UPS, cooling and fire "
    "compartment; either room carries the whole building alone.",
    "Each FTTO switch: 2 × 10GE uplinks, one to each aggregation switch (Eth-Trunk to the M-LAG pair), "
    "10GE1/0/47–48.",
    "Riser cables: 72 fibres for 28 duplex drops leave 16 spare fibres per floor and riser.",
], size=6.2)
s.revisions(X, 114, RW, [["A", "21.10.2026", "first issue: 29 RUs per floor, switch 3: 36 ports"],
                         ["B", "22.10.2026", "task V3 phones: 28 RUs per floor, switch 3: 32 ports"],
                         ["C", "24.10.2026", "redrawn for A4 landscape; ports 10GE1/0/x"]], size=5.2)
s.title_block(X, 135, RW, [("Project", "SYNergy campus network · Huawei STC 2026"),
                            ("Title", "Administrative building S1-A1: FTTO fibre riser, ELV rooms and central ports"),
                            ("Drawing no.", "SYN-LLD-A1-002"), ("Scale", "not to scale"),
                            ("Date / rev.", "24.10.2026 · rev. C"), ("Drawn / checked", "Team SYNergy / —"),
                            ("Sheet", "riser (FTTO)")], size=5.6)
s.save()
