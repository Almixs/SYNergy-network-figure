"""Fig. 26 Deployment plan (Gantt) for Installation and Deployment.

Phases and exit criteria: Table 76 of the document (Installation and Deployment);
pilot building of each type first: Implementation Plan and Testing.
Durations are planning values in weeks from the contract (week 1).
"""
from matplotlib.patches import Polygon, Rectangle
from hwdraw import Diagram, GREY, INK

W, H = 180, 106
d = Diagram(W, H, "fig26_gantt")

X0, X1 = 64, 176          # timeline, mm
WEEKS = 40
MM = (X1 - X0) / WEEKS    # mm per week
Y0 = 16                    # first row
RH = 7.2                   # row height

LEAD = {   # who leads the work: colour
    "Integrator (Huawei partner)": "#0262A9",
    "ISPs": "#C55A11",
    "University IT and NOC": "#2E7D32",
}
C_INT, C_ISP, C_UNI = LEAD.values()

rows = [   # (phase, sub-label, [(start, end, colour, text)])
    ("0. Survey", "fibre L4, ISP entries, 5G, rooms",
     [(1, 4, C_INT, "")]),
    ("Orders and lead time", "equipment, 12 ISP lines, IPv4 /24s",
     [(3, 12, C_UNI, "")]),
    ("1. Data centres", "DC-1 room works · equipment",
     [(5, 11, "#7FB0D9", "room"), (12, 16, C_INT, "fabric, FW")]),
    ("2. WAN and Internet", "ISP circuits, hubs, edges, L4",
     [(12, 18, C_ISP, "")]),
    ("3. Site cores", "core pairs, OOB, 5G routers",
     [(13, 18, C_INT, "")]),
    ("4. Buildings", "pilot of each type · then 19 more",
     [(17, 20, C_INT, "pilot"), (21, 36, C_INT, "site by site")]),
    ("5. Wi-Fi 7", "APs per floor, AC pair, SSIDs",
     [(19, 21, C_INT, "pilot"), (22, 38, C_INT, "")]),
    ("6. Services", "install · move users",
     [(15, 24, C_UNI, "DHCP, DNS, AD, LMS"), (25, 38, C_UNI, "migration")]),
    ("DR test", "planned move to one DC and back",
     [(35, 36, C_UNI, "")]),
    ("7. Handover", "documents, runbooks, spares",
     [(37, 40, C_UNI, "")]),
]

# ------------------------------------------------------------ week grid
d.text(4, 4.5, "Deployment plan: weeks from the contract", size=6.6, weight="bold", bg=False)
d.text(4, 8.6, "Durations are planning values for the tender; each phase ends with the exit criterion of Table 76.",
       size=5.0, color=GREY, bg=False)
yb = Y0 + RH * len(rows)
for wk in range(0, WEEKS + 1, 4):
    x = X0 + wk * MM
    d.ax.plot([x, x], [Y0 - 1.5, yb], color="#D9D9D9", lw=0.4, zorder=0.5)
    if wk:
        d.text(x - 2 * MM, Y0 - 3.2, f"{wk - 3}–{wk}", size=4.6, color=GREY, ha="center", bg=False)
d.text(X0 - 1, Y0 - 3.2, "weeks", size=4.6, color=GREY, ha="right", bg=False)
# months under the chart (≈ 4.35 weeks each)
for m in range(1, 10):
    x = X0 + (m * 4.35 - 2.2) * MM
    d.text(x, yb + 3.0, f"M{m}", size=4.6, color=GREY, ha="center", bg=False)
d.text(X0 - 1, yb + 3.0, "month", size=4.6, color=GREY, ha="right", bg=False)

# ------------------------------------------------------------ rows and bars
for i, (name, sub, bars) in enumerate(rows):
    y = Y0 + i * RH
    if i % 2 == 0:
        d.ax.add_patch(Rectangle((3, y), X1 - 3 + 1, RH, fc="#F5F8FC", ec="none", zorder=0.2))
    d.text(4, y + 2.6, name, size=5.6, weight="bold", bg=False)
    d.text(4, y + 5.3, sub, size=4.6, color=GREY, bg=False)
    for s, e, c, t in bars:
        x = X0 + (s - 1) * MM
        w = (e - s + 1) * MM
        d.ax.add_patch(Rectangle((x, y + 1.6), w - 0.5, RH - 3.2, fc=c, ec="none", zorder=2))
        if t:
            d.text(x + w / 2, y + RH / 2, t, size=4.4, color="white", ha="center", bg=False, z=3)

# ------------------------------------------------------------ milestones
def milestone(week, row, label, above=True, left=False):
    x = X0 + week * MM
    y = Y0 + row * RH + RH / 2
    r = 1.5
    d.ax.add_patch(Polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], closed=True,
                           fc=INK, ec="white", lw=0.4, zorder=4))
    d.text(x - 2 if left else x + 2, y - (2.4 if above else -2.4), label, size=4.5, color=INK, bg=True, z=5,
           ha="right" if left else "left")


milestone(4, 1, "orders placed")
milestone(20, 5, "pilot buildings accepted")
milestone(36, 8, "DR test passed", left=True)
milestone(40, 9, "acceptance signed", above=True, left=True)

# ------------------------------------------------------------ legend
ly = yb + 9
cx = 4
for lab, c in list(LEAD.items()) + [("DC-1 room works (building contractor)", "#7FB0D9")]:
    d.ax.add_patch(Rectangle((cx, ly - 1.4), 6, 2.8, fc=c, ec="none", zorder=2))
    t = d.text(cx + 8, ly, lab, size=4.9, color=GREY, bg=False)
    cx += 8 + len(lab) * 1.05 + 5
d.text(4, ly + 5, "Team SYNergy acts as the design authority: it reviews the exit criterion of every phase "
       "and keeps the documents and NCE templates up to date.", size=4.9, color=GREY, bg=False)
d.save()
