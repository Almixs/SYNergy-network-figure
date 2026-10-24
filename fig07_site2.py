from hwdraw import Diagram
from templates import building, core_buses
from sitewan import rails, to_rails

d = Diagram(180, 172, "fig07_site2")
rails(d)
d.zone(3, 21, 174, 132, "Site 2",
       "1 administrative · 2 academic · 3 dormitories · 8,309 clients · 16,905 end devices · "
       "405 APs (336 indoor, 63 shelter, 6 outdoor) · site peak 17.6 Gbit/s", title_pos="bottom")
d.zone(6, 25, 80, 55, "Core room A", "administrative building", kind="room", title_size=5.8)
d.zone(94, 25, 80, 55, "Core room B", "academic building 2", kind="room", title_size=5.8)

# WAN edges in pairs
for g, xs, names in (("ga", (36, 62), ("S2-WE-1", "S2-WE-2")),
                     ("gb", (118, 144), ("S2-WE-3", "S2-WE-4"))):
    d.group(g, xs[0] - 11, 33.5, xs[1] - xs[0] + 22, 16.5)
    for x, n in zip(xs, names):
        d.node(n, x, 39.5, "core_router", n, "AR8700-8", size=8.5, name_size=5.6)
        to_rails(d, x, 39.5 - d.n[n]["h"] / 2)
d.node("corea", 49, 70, "core_switch", "S2-CORE-A", "S6750-H48Y8C", pos="left")
d.node("coreb", 131, 70, "core_switch", "S2-CORE-B", "S6750-H48Y8C", pos="right")
d.link("ga", "corea", "uplink", a_side="s", b_side="n", double=True)
d.link("gb", "coreb", "uplink", a_side="s", b_side="n", double=True)
d.line([(53, 50), (127, 66)], "uplink", double=True)
d.line([(127, 50), (53, 66)], "uplink", double=True)
d.tag(90, 58, "2 × 10GE per AR · one to each core", color="#404040", size=4.3)
d.link("corea", "coreb", "mlag", a_side="e", b_side="w")
d.tag(90, 70, "M-LAG · 2 × 100GE", color="#1F3864", size=4.3)

for key, x, side, name in (("ara", 15, "right", "S2-AR-A"), ("arb", 165, "left", "S2-AR-B")):
    d.node(key, x, 61, "custom_router_5g", name, "AR5710 · 5G", "OOB, last resort", size=7, pos=side, name_size=5.2)
    cx = 46 if x < 90 else 134
    d.line([(x, 64.3), (x, 76.5), (cx, 76.5), (cx, 73.7)], "g5")

d.note(5, 166.5, "Every WAN edge AR: IPsec over ISP A and ISP B to the hubs of DC-1 and DC-2, MPLS L3VPN inside; home DC-2. "
       "APs register to AC-3 (DC-2, active) and AC-4 (DC-1, standby) through the tunnels; user data is forwarded locally.", size=4.5)

core_buses(d, 9, 171, 86, 90, 49, 131, 73.7, 73.7)
building(d, "admin", 6, 94, 1, 86, 90)
building(d, "academic", 63, 94, 2, 86, 90)
building(d, "dorm", 120, 94, 3, 86, 90)

d.legend([("isp", "ISP line (10GE)"), ("uplink", "Uplinks (10GE / 25GE)"), ("mlag", "M-LAG peer-link"),
          ("g5", "5G router ↔ core (OOB)"), "double"], 5, 160, w=170, size=4.8)
d.save()
