from hwdraw import Diagram, GREY

d = Diagram(180, 154, "fig11_dormitory")

d.node("ca", 50, 8, "core_switch", "Site core A", "S6750-H48Y8C · dorm gateway", size=8, pos="left", name_size=5.6)
d.node("cb", 130, 8, "core_switch", "Site core B", "S6750-H48Y8C · dorm gateway", size=8, pos="right", name_size=5.6)
d.link("ca", "cb", "mlag", a_side="e", b_side="w")
d.tag(90, 8, "M-LAG", color="#1F3864", size=4.4)
d.zone(3, 17, 174, 122, "Dormitory S1-D1 · AND plan · copper, one AP per three rooms",
       "basement + 4 floors · 88 rooms (common rooms included) · 315 residents · 631 end devices · walls: brick",
       title_pos="bottom")

XS = 40            # stack column (closet riser)
levels = [  # name, y, APs, text, height
    ("4th floor", 24, "2 × 5773-21", "4 rooms · 2 APs, one per three rooms as on floor 2", 12),
    ("3rd floor", 38, "10 × 5773-21", "22 rooms · 10 APs, one per three rooms as on floor 2", 12),
    ("2nd floor · LLD floor", 52, "12 × 5773-21", "", 34),
    ("1st floor", 88, "8 × 5773-21", "17 rooms · 8 APs, incl. the 170 m² common hall (34 people)", 12),
    ("Basement", 102, "8 × 5773-21", "17 rooms and the kitchen, counted by the task norm", 26),
]
member = 1
for name, y, aps, txt, h in levels:
    d.box(9, y, 162, h, fc="#FAFAFA" if h == 12 else "#FFFFFF", ec="#C8C8C8" if h == 12 else "#7F7F7F",
          lw=0.5 if h == 12 else 0.7)
    d.text(10.5, y + 2.6, name, size=5.2, weight="bold", bg=False)
    ym = y + 6.8
    d.node(f"sw{y}", XS, ym, "access_switch", size=6)
    n = int(aps.split(" ")[0])
    d.line([(XS + 3, ym), (65, ym)], "copper")
    d.node(f"ap{y}", 68, ym, "ap", size=5.6, stack=2 if n > 2 else 1)
    d.text(73, ym, aps, size=5.0, weight="bold", bg=False)
    if txt:
        d.text(92, ym, txt, size=4.6, color=GREY, bg=False)
    if name == "Basement":
        d.node("swsh", XS, y + 18, "access_switch", size=6)
        d.line([(XS + 3, y + 18), (65, y + 18)], "copper")
        d.node("apsh", 68, y + 18, "ap", size=5.6, stack=2)
        d.text(73, y + 18, "3 × 5761-21", size=5.0, weight="bold", bg=False)
        d.text(92, y + 18, "shelter, Wi-Fi 6: 221 people (70 %) during an alert\nthis switch has its own UPS, 8 h",
               size=4.6, color=GREY, bg=False)

# stack ring through the closet riser
ys = [30.8, 44.8, 58.8, 94.8, 108.8, 120.0]
d.line([(XS - 3.2, ys[0]), (XS - 6, ys[0]), (XS - 6, ys[-1]), (XS - 3.2, ys[-1])], "mlag", z=1.2)
for y in ys[1:-1]:
    d.line([(XS - 6, y), (XS - 3.2, y)], "mlag", z=1.2)
# uplinks: two stack members, one to each core
d.line([(XS - 1, 27.4), (XS - 1, 21), (46.5, 21), (46.5, 11.6)], "uplink")
d.line([(XS + 1.5, 27.4), (XS + 1.5, 19.5), (128.5, 19.5), (128.5, 11.6)], "uplink")
d.tag(90, 19.5, "2 × 10GE: two stack members, one to each core (no agg layer, building peak 1.0 Gbit/s)",
      color="#404040", size=4.4)
d.text(XS - 7.5, 76, "iStack\nring", size=4.4, color="#1F3864", ha="right", bg=False)

# ---------------------------------------------------------------- floor 2 detail
y0 = 52
d.text(10.5, y0 + 9.5, "S1-D1-STK\nmember 2\nS5755-S24P8Y\ncloset 203J", size=4.3, color=GREY, va="top", bg=False)
# room strip: groups of three rooms, AP in the middle room
rooms = [("202", 20.1, 4), ("204", 14.8, 2), ("206", 21.2, 4), ("208", 19.1, 3), ("210", 18.6, 3), ("212", 18.6, 3),
         ("214", 18.5, 3), ("216", 18.6, 3), ("218", 18.3, 3)]
rx, rw, ry, rh = 92, 8.4, y0 + 13, 8
for i, (r, a, p) in enumerate(rooms):
    x = rx + i * rw
    d.box(x, ry, rw, rh, fc="#FFFFFF", ec="#A6A6A6", lw=0.5)
    d.text(x + rw / 2, ry + 2.3, r, size=4.4, weight="bold", ha="center", bg=False)
    d.text(x + rw / 2, ry + 5.4, f"{a} m² → {p}", size=3.7, color=GREY, ha="center", bg=False)
    if i % 3 == 1:
        d.node(f"rap{i}", x + rw / 2, ry + rh + 3.3, "ap", size=4.2)
        d.line([(x - rw + 1, ry + rh + 3.3), (x + rw / 2 - 2.2, ry + rh + 3.3)], "drop")
        d.line([(x + rw / 2 + 2.2, ry + rh + 3.3), (x + 2 * rw - 1, ry + rh + 3.3)], "drop")
d.text(rx + 9 * rw + 1.5, ry + 4, "…", size=6, color=GREY, bg=False)
d.note(92, y0 + 27.5, "AP on the ceiling of the middle room of every group of three;\nit covers both neighbouring rooms",
       size=4.4)
d.note(92, y0 + 3.5, "28 rooms · 80 residents (room m² ÷ 5, rounded down) · 160 Wi-Fi devices\n"
       "1 printer (study room 201SL) · 12 APs from WLAN Planner: 10 for\ngroups of rooms, 2 in the corridor · 97.5 % of the area ≥ −65 dBm",
       size=4.4)

d.legend([("uplink", "10GE uplinks"), ("mlag", "iStack ring / M-LAG"), ("copper", "Cat 6A copper, PoE+"),
          ("drop", "AP covers both neighbouring rooms"), ("access_switch", "S5755-S24P8Y, one per floor")],
         5, 147, w=170, size=4.7)
d.save()
