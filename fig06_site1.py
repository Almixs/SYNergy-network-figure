from hwdraw import Diagram
from templates import building, core_buses

d = Diagram(180, 168, "fig06_site1")
d.zone(3, 17, 174, 134, "Site 1 · main campus",
       "23,724 clients · 48,140 end devices · 1,064 APs (872 indoor, 178 shelter, 14 outdoor) · site peak 50.3 Gbit/s",
       title_pos="bottom")

# DC-2 over fibre L4
d.cloud("dc2", 90, 7, "DC-2", None, size=16)
d.note(5, 3, "Fibre L4 to DC-2: 2 × 100GE, SR-MPLS, MACsec: replication and backup path.\n"
       "Internet of Site 1 leaves through DC-1's edge routers; Sites 2 and 3 reach DC-1's hubs over IPsec.", size=4.5)

# rooms
d.zone(6, 21, 62, 57, "Core room A", "academic building 1", kind="room", title_size=5.8)
d.zone(112, 21, 62, 57, "Core room B", "academic building 4", kind="room", title_size=5.8)
d.zone(73, 27, 34, 23, "DC-1 · border leafs", "admin building basement", kind="dc", title_size=5.6,
       title_pos="bottom")

d.node("pea", 50, 35, "core_router", "S1-PE-A", "NE8000E F1A", pos="left")
d.node("peb", 130, 35, "core_router", "S1-PE-B", "NE8000E F1A", pos="right")
d.node("dc1", 90, 35, "data_center", size=8)
d.node("corea", 50, 66, "core_switch", "S1-CORE-A", "S6750-H48Y8C", pos="left")
d.node("coreb", 130, 66, "core_switch", "S1-CORE-B", "S6750-H48Y8C", pos="right")

# fibre L4
d.link("pea", "dc2", "fiberA", a_side="n", b_side="w", route="vh")
d.link("peb", "dc2", "fiberB", a_side="n", b_side="e", route="vh")
# PE <-> DC-1 border leafs (each PE to BL-1 and BL-2)
d.link("pea", "dc1", "pe", a_side="e", b_side="w", double=True)
d.link("peb", "dc1", "pe", a_side="w", b_side="e", double=True)
d.tag(90, 53.5, "4 × 100GE: PE ↔ border leafs", color="#2E75B6", size=4.3)
# PE-A <-> PE-B over the top
d.line([(52, 31.3), (52, 19), (128, 19), (128, 31.3)], "pe")
d.tag(110, 19, "PE-A ↔ PE-B · 100GE", color="#2E75B6", size=4.3)
# PE -> cores
d.link("pea", "corea", "uplink", a_side="s", b_side="n")
d.link("peb", "coreb", "uplink", a_side="s", b_side="n")
d.line([(52.5, 38.7), (127.5, 62.3)], "uplink")
d.line([(127.5, 38.7), (52.5, 62.3)], "uplink")
d.tag(90, 60, "8 × 25GE per PE · 4 to each core", color="#404040", size=4.3)
d.link("corea", "coreb", "mlag", a_side="e", b_side="w")
d.tag(90, 66, "M-LAG · 2 × 100GE", color="#1F3864", size=4.3)

# 5G routers: OOB and last resort
for key, x, side, name in (("ara", 15, "right", "S1-AR-A"), ("arb", 165, "left", "S1-AR-B")):
    d.node(key, x, 50, "custom_router_5g", name, "AR5710 · 5G", "OOB, last resort", size=7, pos=side, name_size=5.2)
    cx = 47 if x < 90 else 133
    d.line([(x, 53.3), (x, 74), (cx, 74), (cx, 69.7)], "g5")

# buses and buildings
core_buses(d, 9, 171, 84, 88, 50, 130, 69.7, 69.7)
building(d, "admin", 6, 92, 1, 84, 88)
building(d, "academic", 63, 92, 6, 84, 88)
building(d, "dorm", 120, 92, 8, 84, 88)

d.legend([("fiberA", "Fibre L4, circuit A"), ("fiberB", "Fibre L4, circuit B"),
          ("pe", "PE links (100GE)"), ("uplink", "Uplinks (25GE / 10GE)"),
          ("mlag", "M-LAG peer-link"), ("g5", "5G router ↔ core (OOB)"), "double"],
         5, 158, w=170, size=4.8)
d.save()
