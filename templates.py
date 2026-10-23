from hwdraw import GREY

BW, BH = 54, 50          # template box, mm

TEMPLATES = {
    "admin": dict(
        title="Administrative", icon="office_building",
        clients="444 clients · 972 end devices per building",
        gw=("Agg-A", "Agg-B"), gw_sub=("ELV room 1", "ELV room 2"),
        gw_model="S6750-H48Y8C", uplink="4 × 25GE per building",
        parts=[("general_switch", "× 6", "FTTO switch\nS6730-H48X6C-V2"),
               ("access_switch", "× 112", "room unit\nS5735-L8P4X-QA-V2"),
               ("ap", "48 + 4 + 2", "APs: indoor,\nshelter, outdoor")]),
    "academic": dict(
        title="Academic", icon="education",
        clients="3,460 clients · 7,020 end devices per building",
        gw=("Agg-A", "Agg-B"), gw_sub=("IDF room 1", "IDF room 2"),
        gw_model="S6750-H48Y8C", uplink="4 × 25GE per building",
        parts=[("access_switch", "12 + 2", "access + shelter\nS5755-S48P8Y"),
               ("ap", "84 + 25 + 2", "APs: indoor,\nshelter, outdoor"),
               ("ip_phone", "48 · 28", "IP phones ·\nprinters")]),
    "academic_collapsed": dict(
        title="Academic", icon="education",
        clients="3,460 clients · 7,020 end devices per building",
        gw=("Access × 12 + 2",), gw_sub=("",),
        gw_model="S5755-S48P8Y · gateway on the core", uplink="2 × 25GE per access switch",
        parts=[("ap", "84 + 25 + 2", "APs: indoor,\nshelter, outdoor"),
               ("ip_phone", "48 · 28", "IP phones ·\nprinters")],
        note="no agg layer:\neach access switch\nhas one 25GE\nto each core", gw_icon="access_switch"),
    "dorm": dict(
        title="Dormitory", icon="residence",
        clients="315 clients · 631 end devices per building",
        gw=("iStack",), gw_sub=("one switch per floor",),
        gw_model="5 + 1 × S5755-S24P8Y", uplink="2 × 10GE per building",
        parts=[("ap", "40 + 3", "APs: indoor,\nshelter"),
               ("printer", "× 1", "printer")],
        note="no agg layer:\nthe site core is\nthe dorm gateway"),
}


def building(d, kind, x, y, count, bus_a, bus_b, bus_color=("#1F3864", "#2E75B6")):
    """Draw one building template box at (x, y) and its drops to the two
    core buses (y = bus_a, bus_b). Returns nothing."""
    t = TEMPLATES[kind]
    d.zone(x, y, BW, BH, f"{t['title']} × {count}", t["clients"], kind="room",
           title_pos="bottom", title_size=6.0)
    d.node(f"b_{kind}_{x}", x + 6.5, y + 6, t["icon"], size=7.5)
    gy = y + 11
    if len(t["gw"]) == 2:
        xa, xb = x + 23, x + 42
        d.node(f"ga{x}", xa, gy, "aggregation_switch", t["gw"][0], t["gw_sub"][0], size=8, name_size=5.6)
        d.node(f"gb{x}", xb, gy, "aggregation_switch", t["gw"][1], t["gw_sub"][1], size=8, name_size=5.6)
        d.link(f"ga{x}", f"gb{x}", "mlag", a_side="e", b_side="w", )
        # each agg to both cores
        for gx in (xa, xb):
            d.line([(gx - 1.5, bus_a), (gx - 1.5, gy - 3.3)], "uplink", z=1.2)
            d.dot(gx - 1.5, bus_a, bus_color[0], r=0.5)
            d.line([(gx + 1.5, bus_b), (gx + 1.5, gy - 3.3)], "uplink", z=1.2)
            d.dot(gx + 1.5, bus_b, bus_color[1], r=0.5)
        hub_x = (xa + xb) / 2
        d.note(hub_x, gy + 9.5, t["gw_model"], size=4.6, ha="center", va="top", bg=True)
    else:
        gx = x + 32
        d.node(f"ga{x}", gx, gy, t.get("gw_icon", "stacked_switch"), t["gw"][0], t["gw_model"],
               size=8, name_size=5.6, stack=2 if t.get("gw_icon") else 1)
        d.line([(gx - 1.5, bus_a), (gx - 1.5, gy - 3.3)], "uplink", z=1.2)
        d.dot(gx - 1.5, bus_a, bus_color[0], r=0.5)
        d.line([(gx + 1.5, bus_b), (gx + 1.5, gy - 3.3)], "uplink", z=1.2)
        d.dot(gx + 1.5, bus_b, bus_color[1], r=0.5)
        hub_x = gx
    d.text(x + 2, y + 13.5, t["uplink"].replace(" per", "\nper"), size=4.4, color=GREY, bg=False)
    # parts row
    py = y + 29.5
    xs = [x + 10, x + 27, x + 44][:len(t["parts"])]
    d.line([(hub_x, gy + 12.6), (hub_x, py - 6.5)], "drop", z=1)
    d.line([(min(xs + [hub_x]), py - 6.5), (max(xs + [hub_x]), py - 6.5)], "drop", z=1)
    for (ic, n, lab), px in zip(t["parts"], xs):
        d.line([(px, py - 6.5), (px, py - 2.5)], "drop", z=1)
        d.node(f"p{x}{px}", px, py, ic, size=5.6)
        d.text(px + 3.4, py - 1.3, n, size=4.8, weight="bold", ha="left", bg=False)
        d.text(px, py + 3.6, lab, size=4.2, color=GREY, ha="center", va="top", bg=False)
    if t.get("note"):
        d.text(x + 38, py - 3, t["note"], size=4.4, color=GREY, va="top", bg=False)


def core_buses(d, x1, x2, ya, yb, xa, xb, ya0, yb0):
    """Two distribution buses from core A (xa) and core B (xb)."""
    d.line([(xa, ya0), (xa, ya)], "uplink")
    d.line([(x1, ya), (x2, ya)], "uplink", lw=1.2)
    d.line([(xb, yb0), (xb, yb)], "uplink")
    d.line([(x1, yb), (x2, yb)], "uplink", lw=1.2)
    d.dot(xa, ya, r=0.6)
    d.dot(xb, yb, r=0.6)
    d.text(x1, ya - 1.6, "to core A", size=4.5, color=GREY, bg=False)
    d.text(x1, yb + 1.7, "to core B", size=4.5, color=GREY, bg=False)
