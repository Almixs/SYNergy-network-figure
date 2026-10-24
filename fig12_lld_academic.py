"""Fig. 12 Sheet SYN-LLD-K3-201: academic building S1-K3, floor 2, IDF rooms, trays, Cat 6A drops, outlets and APs.

Plan layer: plans/K3-201_plan_layer.png (rev. A of the sheet: plan "Level 02" of the task with the team's IDF rooms,
trays CT-1..CT-5, drops, outlet groups and APs from WLAN Planner), drawn here with wider lines for A4.
Port names as Table 27 of the document (GE1/0/x).
"""
from hwdraw import GREY
from lldsheet import H, W, Sheet, plan_layer

s = Sheet("fig12_lld_academic")
plan = plan_layer("K3-201_plan_layer.png")
pw = (H - 4) * plan.shape[1] / plan.shape[0]
s.image(plan, 2, 2, pw)

X = 2 + pw + 3
RW = W - X - 3
s.legend_panel(X, 3, RW, 32, [("tray", "cable tray (CT-n)"),
                              ("drop", "Cat 6A drops to outlets"),
                              ("apdrop", "Cat 6A drop to an AP (PoE+)"),
                              ("outlet", "outlet group (telecom outlet / floor box)"),
                              ("ap", "AP 5773-21 (red) or 5776-57 (purple)"),
                              ("idf", "IDF room with access switches")], size=5.5, step=4.2)
s.notes(X, 37, RW, 52, [
    'Background: plan "Level 02" of the task (architecture school), scale from the drawn 3 m bar.',
    "Outlet labels: zone (Appendix B) and its ports: D = PC, V = IP phone, P = printer, AV = projector. Seats use "
    "Wi-Fi; computer stations and the PhD desks get floor boxes.",
    "Cabling: Cat 6A U/FTP, one cable per port and AP, ≤ 90 m permanent link; longest run IDF-E to AP-89 = 78 m.",
    "CT-1 to CT-5: 200 × 60 mm wire-mesh trays above the corridor and studio ceilings; drops in conduit.",
    "Switch ports in use: ACC-1 36, ACC-2 34, ACC-3 35 of 48 (APs from GE1/0/33); port schedule in Table 27.",
    "AP positions from the team's WLAN Planner design (purple = 5776-57). Routes are confirmed at the site survey.",
], size=5.6)
s.revisions(X, 106, RW, [["A", "22.10.2026", "first issue (LLD floor of task V3)"],
                         ["B", "24.10.2026", "A4 sheet; ports GE1/0/x"]], size=5.0)
s.title_block(X, 131, RW, [("Project", "SYNergy campus · Huawei STC 2026"),
                            ("Title", "Academic building S1-K3, floor 2: IDF rooms, trays, Cat 6A drops, outlets "
                                      "and APs"),
                            ("Drawing no.", "SYN-LLD-K3-201"), ("Scale", "see scale bar (bottom left)"),
                            ("Date / rev.", "24.10.2026 · rev. B"), ("Drawn / checked", "Team SYNergy / —"),
                            ("Sheet", "1 of 1 (academic)")], size=5.3, lw=15, tsize=6.0, rh=3.3)
s.save()
