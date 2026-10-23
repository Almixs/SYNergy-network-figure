from hwdraw import Diagram, GREY

d = Diagram(180, 160, "fig10_academic")

d.node("ca", 50, 8, "core_switch", "Site core A", "S6750-H48Y8C", size=8, pos="left", name_size=5.6)
d.node("cb", 130, 8, "core_switch", "Site core B", "S6750-H48Y8C", size=8, pos="right", name_size=5.6)
d.zone(3, 17, 174, 129, "Academic building S1-K3 · architecture school plan · GE PoE+ copper",
       "4 floors × 34 zones + basement shelter · 3,460 clients · 7,020 end devices · walls: reinforced concrete 120 mm",
       title_pos="bottom")

d.node("aa", 56, 26, "aggregation_switch", "S1-K3-AGG-A", "S6750-H48Y8C · gateway", "IDF west", size=8, pos="left",
       name_size=5.6)
d.node("ab", 124, 26, "aggregation_switch", "S1-K3-AGG-B", "S6750-H48Y8C · gateway", "IDF east", size=8, pos="right",
       name_size=5.6)
d.link("aa", "ca", "uplink", a_side="n", b_side="s")
d.link("ab", "cb", "uplink", a_side="n", b_side="s")
d.line([(57.5, 22.6), (128.5, 11.4)], "uplink")
d.line([(122.5, 22.6), (51.5, 11.4)], "uplink")
d.tag(90, 15.5, "4 × 25GE per building: each agg to both cores", color="#404040", size=4.4)
d.link("aa", "ab", "mlag", a_side="e", b_side="w")
d.tag(90, 26, "M-LAG · 2 × 100GE", color="#1F3864", size=4.4)

# ---------------------------------------------------------------- floor 2
d.box(9, 36, 162, 66, fc="#FFFFFF", ec="#7F7F7F", lw=0.7)
d.text(10.5, 38.6, "Floor 2 · the task's LLD floor", size=5.6, weight="bold", bg=False)
d.zone(12, 42, 56, 16, "IDF west", "12U wall rack · UPS", kind="floor", title_size=5.2)
d.zone(112, 42, 56, 16, "IDF east", "12U wall rack · UPS", kind="floor", title_size=5.2, title_ha="right")
d.node("acw", 56, 51, "access_switch", "ACC-1, ACC-2", "S5755-S48P8Y", "48 × GE PoE+ · 8 × 25GE", size=7.5,
       pos="left", stack=2, name_size=5.4)
d.node("ace", 124, 51, "access_switch", "ACC-3", "S5755-S48P8Y", "48 × GE PoE+ · 8 × 25GE", size=7.5,
       pos="right", name_size=5.4)
d.link("acw", "aa", "uplink", a_side="n", b_side="s", a_off=-1)
d.link("ace", "ab", "uplink", a_side="n", b_side="s")
d.line([(58, 47.6), (121.5, 29.6)], "uplink")
d.line([(122, 47.6), (58.5, 29.6)], "uplink")
d.tag(90, 34.5, "2 × 25GE per access switch, one to each agg", color="#404040", size=4.4)

# wired devices of the floor (between the IDFs)
wired = [(77, "pc", "59 PCs"), (87, "ip_phone", "12 IP phones"), (97, "printer", "7 printers"),
         (107, "display", "6 projectors")]

# copper distribution
YB = 66
d.line([(16, YB), (164, YB)], "copper", lw=1.0)
d.line([(56, 54.4), (56, YB)], "copper", lw=1.0)
d.line([(124, 54.4), (124, YB)], "copper", lw=1.0)
d.dot(56, YB, r=0.5); d.dot(124, YB, r=0.5)
d.text(90, YB - 2.0, "GE PoE+ copper to every AP and wired outlet · one Cat 6A U/FTP cable each, ≤ 90 m · five trays above the corridors",
       size=4.4, color=GREY, ha="center", bg=True)
for x, ic, lab in wired:
    d.line([(x, YB), (x, 59.5)], "copper")
    d.node(f"w{x}", x, 56.5, ic, size=5.2)
    d.text(x, 52.3, lab, size=4.2, color=GREY, ha="center", va="bottom", bg=False)

groups = [  # x, title, APs, people
    (18, "North studio", "2 × 5776-57", "top row · 150 people"),
    (42, "Flex / lecture", "2 × 5776-57", "185 people · 2 projectors"),
    (66, "Auditorium", "2 × 5776-57", "152 seats · projector"),
    (90, "Laptop classroom", "1 × 5776-57", "91 seats · projector"),
    (114, "Hotdesks", "2 × 5773-21", "west and east · 48 people"),
    (138, "Crits, seminars, offices", "9 × 5773-21", "239 people · 2 projectors"),
    (162, "Corridors, lounge", "3 × 5773-21", "coverage only"),
]
for x, t, aps, ppl in groups:
    n = int(aps.split(" ")[0])
    d.line([(x, YB), (x, 71)], "copper")
    d.dot(x, YB, r=0.45)
    d.node(f"g{x}", x, 75, "ap", t, aps, ppl, size=6.5, stack=min(n, 3), name_size=5.0)

d.note(12, 90.5, "Wi-Fi: 1,671 devices on the floor, about 500 active at once (30 %); 21 Wi-Fi 7 APs from the WLAN Planner "
       "design: 7 × AirEngine 5776-57 in the rooms above 32 active clients, 14 × AirEngine 5773-21 elsewhere.\n"
       "Wired: 59 PCs + 12 IP phones + 7 printers + 6 projectors + 21 APs = 105 PoE+ ports → 3 × S5755-S48P8Y "
       "(73 % of 144 ports). Rooms with a projector: one port for the projector, seats on Wi-Fi.", size=4.5)

# ---------------------------------------------------------------- floors 1, 3, 4
d.box(9, 104, 162, 11, fc="#FAFAFA", ec="#C8C8C8", lw=0.5)
d.text(10.5, 106.6, "Floors 1, 3 and 4", size=5.4, weight="bold", bg=False)
d.text(10.5, 111.0, "each floor the same: 2 IDF rooms, 3 access switches, 21 APs (7 × 5776-57 + 14 × 5773-21), 865 clients",
       size=4.6, color=GREY, bg=False)

# ---------------------------------------------------------------- shelter
y0 = 117
d.box(9, y0, 162, 21, fc="#F3F7F2", ec="#9DB89A", lw=0.6)
d.text(10.5, y0 + 2.6, "Basement shelter · UPS 8 h", size=5.6, weight="bold", bg=False)
d.node("sap", 42, y0 + 11.5, "ap", "25 × AirEngine 5761-21", "Wi-Fi 6 · ≤ 100 phones per AP", size=6.5, stack=3,
       name_size=5.0)
d.node("ssw", 86, y0 + 11.5, "access_switch", "2 × S5755-S48P8Y", "uplinks to Agg-A and Agg-B", size=6.5, stack=2,
       name_size=5.0)
d.link("sap", "ssw", "copper", a_side="e", b_side="w")
d.node("oap", 126, y0 + 11.5, "outdoor_antenna", "2 × AirEngine 5776I-X6H", "outdoor · at the entrances", size=6.5,
       name_size=5.0)
d.note(146, y0 + 6, "2,422 people (70 %)\nduring an alert; the\nsame SSIDs as\nupstairs", size=4.3)

d.legend([("uplink", "25GE uplinks"), ("mlag", "M-LAG peer-link"), ("copper", "GE PoE+ copper, Cat 6A"),
          ("ap", "AP (stacked icon = several)"), ("access_switch", "access switch, PoE+")],
         5, 153, w=170, size=4.7)
d.save()
