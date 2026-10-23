from hwdraw import Diagram

d = Diagram(180, 158, "fig04_wan")

# ------------------------------------------------------------ Site 1 + DC-1
d.zone(4, 4, 84, 60, "Site 1 · main campus",
       "1 administrative · 6 academic · 8 dormitories · Internet through DC-1")
d.node("s1pea", 72, 17, "core_router", "S1-PE-A", "NetEngine 8000E F1A", "core room A · RR", pos="left")
d.node("s1peb", 72, 31, "core_router", "S1-PE-B", "NetEngine 8000E F1A", "core room B", pos="left")
d.zone(7, 41, 78, 20, "DC-1 · admin building basement", kind="dc", title_size=5.8)
d.node("dc1er", 34, 53, "core_router", "DC1-ER-1, 2", "NetEngine 8000E F1A", "Internet edge", pos="left", stack=2)
d.node("dc1hub", 62, 53, "core_router", "DC1-HUB-1…4", "AR8700-8", "IPsec hubs", pos="right", stack=3)
d.link("dc1er", "dc1hub", "uplink", label="10GE", label_dy=-2.6)

# ------------------------------------------------------------ DC-2
d.zone(92, 4, 84, 60, "DC-2 · own cage in ISP B's Tier III data centre",
       "> 10 km from the campus · 2N power from the operator")
d.node("dc2pea", 108, 17, "core_router", "DC2-PE-A", "NetEngine 8000E F1A", "rack row A", pos="right")
d.node("dc2peb", 108, 31, "core_router", "DC2-PE-B", "NetEngine 8000E F1A", "rack row B · RR", pos="right")
d.zone(95, 41, 78, 20, "DC-2 Internet edge", kind="dc", title_size=5.8)
d.node("dc2hub", 118, 53, "core_router", "DC2-HUB-1…4", "AR8700-8", "IPsec hubs", pos="left", stack=3)
d.node("dc2er", 146, 53, "core_router", "DC2-ER-1, 2", "NetEngine 8000E F1A", "Internet edge", pos="right", stack=2)
d.link("dc2hub", "dc2er", "uplink", label="10GE", label_dy=-2.6)

# ------------------------------------------------------------ fibre L4
d.link("s1pea", "dc2pea", "fiberA", a_side="e", b_side="w")
d.link("s1peb", "dc2peb", "fiberB", a_side="e", b_side="w")
d.tag(90, 24, "Fibre L4 · 2 × 100GE\nSR-MPLS · MACsec · ≤ 25 km", color="#2E7D32")

# hub-to-hub tunnel T1 (falls back to L4)
d.line([(62, 49), (62, 37.5), (118, 37.5), (118, 49)], "ipsec")
d.tag(90, 37.5, "T1 · hub ↔ hub IPsec", color="#C55A11", size=4.8)

# ------------------------------------------------------------ ISP rails
YA, YB, RH = 77, 88, 5
d.rail(16, 176, YA, RH, "ISP A", "100GE to each DC edge router · 10GE to each WAN edge AR · clean-pipe scrubbing",
       icon="network_cloud_2")
d.rail(16, 176, YB, RH, "ISP B", "100GE to each DC edge router · 10GE to each WAN edge AR · clean-pipe scrubbing",
       icon="network_cloud_2")




def to_rails_from_above(x, y0):
    d.line([(x - 2, y0), (x - 2, YA - RH / 2)], "isp")
    d.dot(x - 2, YA - RH / 2, "#C55A11")
    d.line([(x + 2, y0), (x + 2, YB - RH / 2)], "isp")
    d.dot(x + 2, YB - RH / 2, "#C55A11")


def to_rails_from_below(x, y0):
    d.line([(x - 3.5, y0), (x - 3.5, YB + RH / 2)], "isp")
    d.dot(x - 3.5, YB + RH / 2, "#C55A11")
    d.line([(x - 1, y0), (x - 1, YA + RH / 2)], "isp", z=1.4)
    d.dot(x - 1, YA + RH / 2, "#C55A11")


to_rails_from_above(34, 57)
to_rails_from_above(146, 57)

# ------------------------------------------------------------ IPsec overlay bus
YBUS = 100
d.line([(62, 57), (62, YBUS)], "ipsec", z=1.3)
d.line([(118, 57), (118, YBUS)], "ipsec", z=1.3)
d.line([(27, YBUS), (155, YBUS)], "ipsec")
d.tag(90, YBUS, "IPsec AES-256-GCM, IKEv2: every edge AR ↔ hubs of DC-1 and DC-2 · GRE + MPLS L3VPN inside · BFD 300 ms × 3",
      color="#C55A11", size=4.8)

# ------------------------------------------------------------ Sites 3 and 2
d.zone(4, 106, 72, 34, "Site 3 · 1 academic building",
       "home DC-1 · HyperMetro quorum · both ISPs down: 5G", title_pos="bottom")
d.zone(82, 106, 94, 34, "Site 2 · 1 administrative · 2 academic · 3 dormitories",
       "home DC-2 · Internet and IPv6 through DC-2 · both ISPs down: 5G", title_pos="bottom")
edges = [("s3we1", 24, "S3-WE-1", "fire zone A", 1),
         ("s3we2", 58, "S3-WE-2", "fire zone B", 1),
         ("s2we12", 104, "S2-WE-1, 2", "core room A · admin bldg", 2),
         ("s2we34", 152, "S2-WE-3, 4", "core room B · academic bldg 2", 2)]
for key, x, name, room, st in edges:
    d.node(key, x, 119, "core_router", name, "AR8700-8", room, stack=st)
    top = 119 - d.n[key]["h"] / 2
    to_rails_from_below(x, top)
    d.line([(x + 3, YBUS), (x + 3, top)], "ipsec")
    d.dot(x + 3, YBUS, "#C55A11", r=0.45)

d.note(6, 154.5, "Peak tunnel load: Site 2 19.4 Gbit/s, Site 3 8.1 Gbit/s · worst single failure: one ISP down, 48 % of the Site 2 edges",
       ha="left", va="center", size=4.8)

d.legend(["isp", "ipsec", "fiberA", "fiberB", ("uplink", "Hub ↔ edge router (10GE)")],
         6, 146, w=168, size=4.9)
d.save()
