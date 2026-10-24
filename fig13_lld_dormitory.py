"""Fig. 13 Sheet SYN-LLD-D1-201: dormitory S1-D1 (AND), floor 2, floor switch, tray and drops to the APs.

Plan layer: plans/D1-201_plan_layer.png (rev. A of the sheet: AND plan, floor 2, with the team's IDF closet,
trays CT-1, CT-2, drops and APs from WLAN Planner; the feet scale of the source plan removed), drawn with wider
lines for A4. Port schedule as Appendix A.8 (S1-D1-STK member 2).
"""
from lldsheet import W, Sheet, plan_layer

s = Sheet("fig13_lld_dormitory")
plan = plan_layer("D1-201_plan_layer.png")
ph = s.image(plan, 2, 2, W - 4)
MM_PER_PX = (W - 4) / plan.shape[1]

# notes and legend in the free area of the plan, right of the IDF callout and below the east wing
s.notes(99, 70, 103, 34, [
    "Background: AND plan, floor 2 (task file); areas on the plan in ft².",
    "One AP 5773-21 on the ceiling of the middle room of every three, plus room 224 and two corridor APs "
    "(team's WLAN Planner design).",
    "Cat 6A U/FTP from the floor switch to every AP and the printer outlet, ≤ 90 m; longest run to AP-108 = 62 m.",
    "CT-1, CT-2: 100 × 60 mm wire-mesh trays above the corridor ceiling; room drops in conduit through the corridor "
    "wall.",
    "The other floors repeat this layout with their own stack member (APs per level 8, 8, 12, 10, 2).",
    "Closet 203J and the routes are confirmed at the site survey.",
], size=5.4)
s.legend_panel(205, 79, 58, 25, [("tray", "cable tray (CT-n)"),
                                  ("apdrop", "Cat 6A drop to an AP (PoE+)"),
                                  ("outlet", "telecom outlet (P = printer)"),
                                  ("ap", "AP 5773-21"),
                                  ("idf", "IDF closet with the floor switch")], size=5.4, step=3.6)

Y = 2 + ph + 2.5
s.heading(3, Y + 1, "Port schedule · S1-D1-STK member 2 (floor 2), CloudEngine S5755-S24P8Y", 6.0)
VL = "pvid 21 MGMT; 212 STUDENT, 512 GUEST"
rows = [["Port", "To", "Where", "Device", "Mode", "VLANs (VRF)"]]
aps = [("AP-117", "room 204"), ("AP-118", "room 210"), ("AP-119", "room 216"), ("AP-116", "room 224"),
       ("AP-108", "room 228"), ("AP-120", "room 211"), ("AP-121", "room 217"), ("AP-111", "room 223"),
       ("AP-112", "room 229"), ("AP-103", "hall 200HL"), ("AP-123", "corridor at the hall junction"),
       ("AP-122", "corridor by washrooms 220B, 222B")]
for i, (ap, where) in enumerate(aps, 1):
    rows.append([f"GE2/0/{i}", ap, where, "AP 5773-21", "trunk, PoE+", VL])
rows += [["GE2/0/13", "201SL", "study room", "printer", "access, MAB", "612 PRINT"],
         ["GE2/0/14–24", "—", "—", "spare", "shut down", "—"],
         ["25GE2/0/1–2", "—", "closet riser", "stack cables", "iStack ring", "to members 1 and 3"]]
s.table(3, Y + 3, [17, 12, 38, 17, 17, 50], rows, size=5.1, rh=3.15)

X = 158
RW = W - X - 3
s.revisions(X, Y - 0.5, RW, [["A", "22.10.2026", "first issue (LLD floor of task V3)"],
                             ["B", "24.10.2026", "A4 sheet; feet scale of the source plan removed"]], size=5.0)
s.title_block(X, Y + 14.5, RW, [("Project", "SYNergy campus network · Huawei STC 2026"),
                                 ("Title", "Dormitory S1-D1 (AND), floor 2: floor switch, tray, drops to the APs"),
                                 ("Drawing no.", "SYN-LLD-D1-201"), ("Scale", "see scale bar"),
                                 ("Date / rev.", "24.10.2026 · rev. B"), ("Drawn / checked", "Team SYNergy / —"),
                                 ("Sheet", "1 of 1 (dormitory)")], size=5.3, lw=17, tsize=6.2, rh=3.3)
s.scalebar(X + 2, 159, 54.7 * MM_PER_PX, 10, [0, 5, 10])
s.save()
