from hwdraw import Diagram, GREY, LINKS

d = Diagram(180, 198, "fig09_admin_ftto")
RA, RB = 6.0, 174.0          # riser A / riser B columns

# ---------------------------------------------------------------- site cores
d.node("ca", 50, 8, "core_switch", "Site core A", "S6750-H48Y8C", size=8, pos="left", name_size=5.6)
d.node("cb", 130, 8, "core_switch", "Site core B", "S6750-H48Y8C", size=8, pos="right", name_size=5.6)

d.zone(3, 17, 174, 166, "Administrative building S1-A1 · Amravati plan · FTTO: active point-to-point fibre to every room",
       "4 floors × 26 rooms + basement shelter · 444 clients · 972 end devices · 112 room units · walls: reinforced concrete 120 mm",
       title_pos="bottom")

# ---------------------------------------------------------------- ELV rooms
d.zone(9, 21, 70, 36, "ELV room 1", "floor 1, block E · riser A · 42U, UPS 4 h", kind="room", title_size=5.6)
d.zone(101, 21, 70, 36, "ELV room 2", "floor 1, block G · riser B · 42U, UPS 4 h", kind="room", title_size=5.6,
       title_ha="right")
d.node("aa", 56, 32, "aggregation_switch", "S1-A1-AGG-A", "S6750-H48Y8C", "building gateway", size=8, pos="left", name_size=5.6)
d.node("ab", 124, 32, "aggregation_switch", "S1-A1-AGG-B", "S6750-H48Y8C", "building gateway", size=8, pos="right", name_size=5.6)
d.node("fa", 56, 49, "general_switch", "S1-A1-FT1-1…3", "S6730-H48X6C-V2", "48 × 10GE SFP+ to the RUs", size=8, pos="left",
       stack=3, name_size=5.6)
d.node("fb", 124, 49, "general_switch", "S1-A1-FT2-1…3", "S6730-H48X6C-V2", "48 × 10GE SFP+ to the RUs", size=8, pos="right",
       stack=3, name_size=5.6)

# aggs to both cores
d.link("aa", "ca", "uplink", a_side="n", b_side="s", a_off=-1)
d.link("ab", "cb", "uplink", a_side="n", b_side="s", a_off=1)
d.line([(57, 28.6), (128.5, 11.4)], "uplink")
d.line([(123, 28.6), (51.5, 11.4)], "uplink")
d.tag(90, 16.5, "4 × 25GE per building: each agg to both cores", color="#404040", size=4.4)
d.link("aa", "ab", "mlag", a_side="e", b_side="w")
d.tag(90, 32, "M-LAG · 2 × 100GE over both risers", color="#1F3864", size=4.4)
# every FTTO switch: 10GE to each agg
d.link("fa", "aa", "uplink", a_side="n", b_side="s")
d.link("fb", "ab", "uplink", a_side="n", b_side="s")
d.line([(60, 47), (119.5, 35)], "uplink")
d.line([(120, 47), (60.5, 35)], "uplink")
d.tag(90, 47.5, "10GE from every FTTO switch to each agg (Eth-Trunk to the M-LAG pair)", color="#404040", size=4.3)

# risers
d.line([(52, 52), (52, 59), (RA, 59), (RA, 117.75)], "riserA", z=1.6)
d.line([(128, 52), (128, 59), (RB, 59), (RB, 117.75)], "riserB", z=1.6)
d.text(RA + 1.5, 61.2, "riser A: one 72-fibre OS2 cable per floor", size=4.4, color=LINKS["riserA"][0], bg=True)
d.text(RB - 1.5, 61.2, "riser B: one 72-fibre OS2 cable per floor", size=4.4, color=LINKS["riserB"][0], ha="right", bg=True)


def floor_trays(y0, xa, xb, rus, ya, yb):
    """ODF A/B on the risers, tray A above and tray B below the room units."""
    d.node(f"odfa{y0}", xa, (ya + yb) / 2, "custom_odf", size=6.5)
    d.node(f"odfb{y0}", xb, (ya + yb) / 2, "custom_odf", size=6.5)
    ym = (ya + yb) / 2
    d.line([(RA, ym), (xa - 3.3, ym)], "riserA", z=1.6)
    d.dot(RA, ym, LINKS["riserA"][0], r=0.5)
    d.line([(xb + 3.3, ym), (RB, ym)], "riserB", z=1.6)
    d.dot(RB, ym, LINKS["riserB"][0], r=0.5)
    d.line([(xa + 3.3, ym), (xa + 5, ym), (xa + 5, ya), (max(rus) + 1, ya)], "riserA", z=1.4, lw=0.8)
    d.line([(xb - 3.3, ym), (xb - 5, ym), (xb - 5, yb), (min(rus) - 1, yb)], "riserB", z=1.4, lw=0.8)
    for x in rus:
        d.line([(x - 0.8, ya), (x - 0.8, ym - 1.6)], "riserA", z=1.4, lw=0.6)
        d.line([(x + 0.8, yb), (x + 0.8, ym + 1.6)], "riserB", z=1.4, lw=0.6)
        d.node(f"ru{y0}{x}", x, ym, "access_switch", size=5)


# ---------------------------------------------------------------- floors 4, 3, 2
for i, f in enumerate((4, 3, 2)):
    y0 = 64 + i * 14
    d.box(9, y0, 162, 12.5, fc="#FAFAFA", ec="#C8C8C8", lw=0.5)
    d.text(10.5, y0 + 2.4, f"Floor {f}", size=5.2, weight="bold", bg=False)
    rus = [44, 54, 64, 74, 84]
    floor_trays(y0, 26, 154, rus, y0 + 3.4, y0 + 9.6)
    d.text(90, y0 + 6.5, "…", size=6, color=GREY, ha="center", bg=False)
    d.text(97, y0 + 6.5, "26 rooms · 28 room units · 12 APs · the same plan as floor 1\n"
                         "ODF A and ODF B: 36 × LC duplex each, 28 in use · no power in the boxes",
           size=4.4, color=GREY, bg=True)
d.text(26, 63, "ODF A", size=4.4, color=GREY, ha="center", bg=False)
d.text(154, 63, "ODF B", size=4.4, color=GREY, ha="center", bg=False)

# ---------------------------------------------------------------- floor 1 (LLD)
y0 = 106
d.box(9, y0, 162, 44, fc="#FFFFFF", ec="#7F7F7F", lw=0.7)
d.text(10.5, y0 + 2.6, "Floor 1 · the task's LLD floor", size=5.6, weight="bold", bg=False)
rus = [48, 74, 100, 126]
floor_trays(y0, 26, 154, rus, y0 + 8, y0 + 15.5)
rooms = [  # x, room label, devices [(icon, label)]
    (48, "RU · single office\n(21 rooms)", [("pc", "PC"), ("ap", "AP 5773-21")]),
    (74, "RU 12 + RU 13 · clerks'\nroom (2 RUs)", [("pc", "5 × PC"), ("ip_phone", "3 × IP phone")]),
    (100, "RU · library", [("printer", "printer"), ("ap", "AP 5773-21")]),
    (126, "RU · conference hall\n(60 seats)", [("display", "projector, AV"), ("ap", "AP 5776-57")]),
]
for x, lab, devs in rooms:
    for k, (ic, dl) in enumerate(devs):
        dx = x - 5.5 + 11 * k
        d.line([(x, y0 + 13.8), (x, y0 + 21), (dx, y0 + 21), (dx, y0 + 24)], "copper", z=1.3)
        d.node(f"dev{x}{k}", dx, y0 + 27.5, ic, size=5.4)
        d.text(dx, y0 + 31.3, dl, size=4.2, color=GREY, ha="center", va="top", bg=False)
    d.text(x, y0 + 36.0, lab, size=4.3, color="#1A1A1A", ha="center", va="top", bg=False)
d.text(140, y0 + 11.8, "…", size=6, color=GREY, ha="center", bg=False)
d.note(10.5, y0 + 19.5, "26 rooms · 28 RUs\n67 of 224 RU ports used\n35 PCs · 6 IP phones\n13 printers · 2 AV\n"
       "11 Wi-Fi 7 APs (WLAN\nPlanner) + 1 in the\nlift lobby", size=4.3)
d.note(170, y0 + 19.5, "Every RU: fibre 1 → ODF A\n→ ELV room 1; fibre 2 →\nODF B → ELV room 2.\n"
       "Smart Link moves the RU\nto its other fibre in\n< 50 ms. PoE+ for APs\nand phones from the RU.",
       size=4.3, ha="right")

# ---------------------------------------------------------------- basement shelter
y0 = 152
d.box(9, y0, 162, 22, fc="#F3F7F2", ec="#9DB89A", lw=0.6)
d.text(10.5, y0 + 2.6, "Basement shelter · UPS 8 h", size=5.6, weight="bold", bg=False)
d.node("sap", 44, y0 + 12, "ap", "4 × AirEngine 5761-21", "Wi-Fi 6 · ≤ 100 phones per AP", size=6.5, stack=2, name_size=5.0)
d.node("ssw", 88, y0 + 12, "access_switch", "2 × S5755-S48P8Y", "uplinks to Agg-A and Agg-B", size=6.5, stack=2,
       name_size=5.0)
d.link("sap", "ssw", "copper", a_side="e", b_side="w")
d.node("oap", 128, y0 + 12, "outdoor_antenna", "2 × AirEngine 5776I-X6H", "outdoor, IP68 · entrance and route", size=6.5,
       name_size=5.0)
d.note(150, y0 + 7, "311 people (70 %)\nduring an alert;\nthe same SSIDs\nas upstairs", size=4.3)

d.legend([("riserA", "Fibre 1 of a room unit → ODF A → ELV room 1"),
          ("riserB", "Fibre 2 of a room unit → ODF B → ELV room 2"),
          ("uplink", "10GE / 25GE uplinks"), ("mlag", "M-LAG peer-link"), ("copper", "GE PoE+ copper in the room"),
          ("custom_odf", "floor box (ODF), passive"), ("access_switch", "room unit S5735-L8P4X-QA-V2")],
         5, 189, w=170, size=4.7)
d.save()
