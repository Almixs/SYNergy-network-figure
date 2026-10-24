"""Fig. 14 Sheet SYN-LLD-A1-101: administrative building S1-A1, floor 1, FTTO room units, fibre routes and floor boxes.

Plan layer: plans/A1-101_plan_layer.png (rev. B of the sheet: architect's "First floor Plan" with the team's
RUs, trays CT-A / CT-B, floor boxes and APs), drawn here with wider lines for A4.
Port names as Table 27 of the document (RU ports GE1/0/x, central ports 10GE1/0/x).
"""
from math import ceil

from matplotlib.patches import Rectangle

from hwdraw import GREY, INK
from lldsheet import NAVY, RED, W, Sheet, plan_layer

s = Sheet("fig14_lld_admin_ftto")
ax = s.ax

plan = plan_layer("A1-101_plan_layer.png")
ph = s.image(plan, 2, 2, W - 4)            # 3200 px -> 262 mm
MM_PER_PX = (W - 4) / plan.shape[1]
Y = 2 + ph + 2.5

# ------------------------------------------------------------ floor box port schedule
s.heading(3, Y + 1.2, "Floor box port schedule, floor 1 · ODF-A and ODF-B ports are the same: port n = RU n; "
                      "FTTO switch and port 10GE1/0/x in ELV rooms 1 and 2", 5.8)


def room(n):
    return n if n <= 12 else (n - 1 if n <= 17 else n - 2)


cells = []
for n in range(1, 37):
    if n <= 28:
        sw = ceil(n / 10)
        cells.append(f"{n:02d} · rm {room(n)}\nFT{sw}\n10GE1/0/{n - 10 * (sw - 1)}")
    else:
        cells.append(f"{n}\nspare\n")
rows = [cells[i:i + 12] for i in (0, 12, 24)]
yy = s.table(3, Y + 3.2, [12.25] * 12, rows, size=5.1, rh=3.0, header=False, align=["center"] * 12)


# ------------------------------------------------------------ room details
def ru(x, y, name, ports, w=19, h=8.5):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=NAVY, lw=1.0, zorder=2))
    s.text(x + w / 2, y + 3.0, name, size=6, weight="bold", ha="center", color=NAVY, bg=False, z=3)
    s.text(x + w / 2, y + 6.0, "S5735-L8P4X", size=5, ha="center", color=GREY, bg=False, z=3)
    for lab, col, dy in (("ODF-A", NAVY, 2.6), ("ODF-B", RED, 5.9)):
        ax.plot([x - 6, x], [y + dy, y + dy], color=col, lw=1.0, ls="-" if col == NAVY else (0, (3, 1.5)), zorder=2)
        s.text(x - 6.5, y + dy, lab, size=5, color=col, ha="right", bg=False)
    for k, (p, txt) in enumerate(ports):
        py = y + 2.2 + k * 4.2
        ax.plot([x + w, x + w + 10], [py, py], color=INK, lw=0.7, zorder=2)
        s.text(x + w + 0.8, py - 1.3, p, size=4.8, color=GREY, bg=False)
        s.text(x + w + 11, py, txt, size=5.4, bg=False)


DY = yy + 3
s.heading(3, DY, "Detail 1 · typical office (one RU)", 6.0)
ru(13, DY + 3, "RU nn", [("GE1/0/1", "PC · access 101 STAFF, 802.1X"), ("GE1/0/8", "AP · trunk, pvid 12, PoE+")])
s.para(3, DY + 14, "10GE1/0/1 → ODF-A (Smart Link master in blocks E, F), 10GE1/0/2 → ODF-B; 10GE LR optics; "
                   "spare ports shut down", 68, size=5.2, color=GREY)
X2 = 74
s.heading(X2, DY, "Detail 2 · room 12, clerks (RU 12 + RU 13)", 6.0)
ru(X2 + 12, DY + 3, "RU 12", [("GE1/0/1–5", "5 PCs · access 101 STAFF"),
                              ("GE1/0/6–8", "3 IP phones · hybrid 101 / voice 551")])
ru(X2 + 12, DY + 15, "RU 13", [("GE1/0/1", "printer · access 601 PRINT"), ("GE1/0/8", "AP-L1 · trunk, PoE+, lift lobby")])
s.para(X2, DY + 26.5, "Both RUs: 10GE1/0/1 → ODF-A, 10GE1/0/2 → ODF-B, as in Detail 1.", 70, size=5.2, color=GREY)

# ------------------------------------------------------------ legend, scale, revisions
X = 153
s.legend_panel(X, Y - 1, 53, 42.5, [("routeA", "fibre tray CT-A → ODF-A / ELV room 1"),
                                     ("routeB", "fibre tray CT-B → ODF-B / ELV room 2"),
                                     ("drop", "OS2 duplex drop (A solid, B dashed)"),
                                     ("ru", "room unit, number = floor-box port"),
                                     ("ap_dashed", "access point (dashed = to be added)"),
                                     ("odf", "floor box (ODF) at the riser"),
                                     ("riser", "riser shaft (vertical fibre route)"),
                                     ("room", "room number (Appendix B)")], size=5.5, step=4.3)
s.scalebar(X + 2, Y + 45, 48.4 * MM_PER_PX, 10, [0, 5, 10])
s.revisions(X, Y + 51, 53, [["A", "21.10.2026", "first issue: 29 RUs per floor"],
                            ["B", "22.10.2026", "task V3: 28 RUs, renumbered"],
                            ["C", "24.10.2026", "A4 sheet; ports as Table 27"]], size=4.9)

# ------------------------------------------------------------ notes and title block
X3 = 209
RW = W - X3 - 3
s.notes(X3, Y - 1, RW, 50.5, [
    'Background: architect\'s plan "First floor Plan" (task file); floors 2–4 are the same, so sheets A1-101 to '
    "A1-401 differ only in names and central ports.",
    "Room numbers in ellipses as Appendix B; RU numbers 01–28 are the floor-box ports of the room's fibres.",
    "Each RU: on the wall by the door at 0.4 m, mains from the network-power circuit of its block; two OS2 duplex "
    "drops, CT-A to ODF-A and CT-B to ODF-B.",
    "CT-A, CT-B: 100 × 50 mm perforated trays in the corridor ceiling void, on opposite sides, ≥ 300 mm apart, "
    "fibre only.",
    "APs from the team's WLAN Planner design; each AP takes PoE+ from GE1/0/8 of its room's RU; AP-L1 (lift lobby) "
    "is fed from RU 13.",
    "Dimensions in mm. Confirm runs and box positions at the site survey; do not scale for installation.",
], size=5.3)
s.title_block(X3, Y + 51, RW, [("Project", "SYNergy campus · Huawei STC 2026"),
                                ("Title", "Administrative building S1-A1, floor 1: FTTO room units, fibre routes "
                                          "and floor boxes"),
                                ("Drawing no.", "SYN-LLD-A1-101"), ("Scale", "see scale bar"),
                                ("Date / rev.", "24.10.2026 · rev. C"), ("Drawn / checked", "Team SYNergy / —"),
                                ("Sheet", "1 of 4 (FTTO)")], size=5.3, lw=15, tsize=6.0, rh=3.3)
s.save()
