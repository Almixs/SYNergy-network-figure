from hwdraw import Diagram, GREY
from templates import building, core_buses
from sitewan import rails, to_rails

d = Diagram(180, 172, "fig08_site3")
rails(d)
d.zone(3, 21, 174, 132, "Site 3 · 1 academic building",
       "3,460 clients · 7,020 end devices · 111 APs (84 indoor, 25 shelter, 2 outdoor) · site peak 7.3 Gbit/s · "
       "holds the HyperMetro quorum", title_pos="bottom")
d.zone(6, 25, 80, 55, "Fire zone A", "UPS 2 h + generator", kind="room", title_size=5.8)
d.zone(94, 25, 80, 55, "Fire zone B", "UPS 2 h + generator", kind="room", title_size=5.8)

d.node("we1", 40, 37, "core_router", "S3-WE-1", "AR8700-8", pos="left")
d.node("we2", 140, 37, "core_router", "S3-WE-2", "AR8700-8", pos="right")
to_rails(d, 40, 37 - d.n["we1"]["h"] / 2)
to_rails(d, 140, 37 - d.n["we2"]["h"] / 2)
d.node("corea", 40, 68, "core_switch", "S3-CORE-A", "S6750-H48Y8C", "collapsed core", pos="left")
d.node("coreb", 140, 68, "core_switch", "S3-CORE-B", "S6750-H48Y8C", "collapsed core", pos="right")
d.link("we1", "corea", "uplink", a_side="s", b_side="n")
d.link("we2", "coreb", "uplink", a_side="s", b_side="n")
d.line([(43, 41), (137, 64.5)], "uplink")
d.line([(137, 41), (43, 64.5)], "uplink")
d.tag(90, 46, "2 × 10GE per AR · one to each core", color="#404040", size=4.3)
d.link("corea", "coreb", "mlag", a_side="e", b_side="w")
d.tag(90, 68, "M-LAG · 2 × 100GE", color="#1F3864", size=4.3)

# 5G last resort
for key, x, name, cx in (("ara", 16, "S3-AR-A", 37), ("arb", 164, "S3-AR-B", 143)):
    d.node(key, x, 57, "custom_router_5g", name, "AR5710-S8T2XE-NRGL", "SIMs of 2 operators", size=7.5,
           pos="above", name_size=5.2)
    d.line([(x, 60.6), (x, 76), (cx, 76), (cx, 71.7)], "g5")
d.note(5, 166.5, "Both ISPs down at the site: the AR5710 pair carries 100 / 40 Mbit/s for management, login, voice, staff work and "
       "lectures (audio + slides); students get messengers only. The AR5710 pair is also the out-of-band path.", size=4.5)

core_buses(d, 9, 171, 86, 90, 40, 140, 71.7, 71.7)
building(d, "academic_collapsed", 40, 94, 1, 86, 90)
# quorum server, fire zone B, one NIC to each core
d.zone(112, 94, 50, 36, "Quorum server", "fire zone B · MGMT VRF", kind="room", title_pos="bottom", title_size=6.0)
d.node("q", 137, 106, "general_server", "HyperMetro quorum", "arbiter for Dorado\nin DC-1 and DC-2", size=8, name_size=5.4)
d.line([(135.5, 86), (135.5, 101.8)], "uplink"); d.dot(135.5, 86, r=0.5)
d.line([(138.5, 90), (138.5, 101.8)], "uplink"); d.dot(138.5, 90, "#2E75B6", r=0.5)
d.text(114, 97, "2 NICs, one\nper core", size=4.4, color=GREY, va="top", bg=False)

d.legend([("isp", "ISP line (10GE)"), ("uplink", "Uplinks (10GE / 25GE)"), ("mlag", "M-LAG peer-link"),
          ("g5", "5G router ↔ core (OOB)")], 5, 160, w=170, size=4.8)
d.save()
