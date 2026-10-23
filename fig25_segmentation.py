from matplotlib.patches import Rectangle
from hwdraw import Diagram, GREY, INK

d = Diagram(180, 158, "fig25_segmentation")
BLUE_T = "#2E75B6"

# ---------------------------------------------------------------- campus VRFs
d.zone(3, 3, 60, 141, "Campus VRFs (all three sites)",
       "EVPN-VXLAN in the site · MPLS L3VPN between sites", kind="site", title_size=6.0)
vrfs = [
    ("STAFF", "50001", 82, "staff PCs, teachers, SSL VPN users", "DC services, print server, DMZ,\nInternet (own logged /27)"),
    ("STUDENT", "50002", 60, "students' laptops and phones", "LMS, lectures, print server, DMZ,\nInternet (NAT44)"),
    ("GUEST", "50003", 40, "visitors after the portal", "portal, DHCP / DNS, DMZ,\nInternet ≤ 5 Mbit/s"),
    ("VOICE", "50004", 75, "IP phones, Wi-Fi calling", "PBX and SBC only · no Internet"),
    ("PRINT", "50005", 55, "printers and MFPs", "print server only · no Internet"),
    ("CCTV", "50006", 48, "cameras (future)", "VMS only · no Internet"),
    ("IOT", "50007", 45, "access control, BMS, sensors", "ACS and BMS servers only\nno Internet"),
    ("MGMT", "50000", 95, "switches, APs, RUs, UPS", "NCE, AAA, SIEM only\nmanaged from the jump hosts"),
]
YBUS_X = 67
y = 12
card_y = []
for name, vni, prio, who, reach in vrfs:
    h = 15
    d.box(6, y, 54, h, fc="white", ec="#9DB3CC", lw=0.6, z=1)
    d.ax.add_patch(Rectangle(
        (6, y), 1.2, h, fc=BLUE_T, ec="none", zorder=2))
    d.text(9, y + 2.8, name, size=5.8, weight="bold", bg=False)
    d.text(58.5, y + 2.8, f"VNI {vni} · zone {prio}", size=4.4, color=GREY, ha="right", bg=False)
    d.text(9, y + 6.2, who, size=4.6, color=GREY, bg=False)
    d.text(9, y + 8.6, "→ " + reach, size=4.6, color=BLUE_T, va="top", bg=False)
    cy = y + h / 2
    d.line([(60, cy), (YBUS_X, cy)], "vrf")
    card_y.append(cy)
    y += h + 1.6
d.line([(YBUS_X, card_y[0]), (YBUS_X, card_y[-1])], "vrf", lw=1.4)
for cy in card_y:
    d.dot(YBUS_X, cy, BLUE_T, r=0.45)

# ---------------------------------------------------------------- DC-1 border leafs and FW pair
d.zone(70, 3, 54, 141, "DC-1", "DC-2 is built the same way", kind="dc", title_size=6.0)
d.group("blg", 74, 13, 46, 20, "M-LAG")
d.node("bl1", 85, 21, "core_switch", "DC1-BL-1", "border leaf", size=7.5, name_size=5.2)
d.node("bl2", 109, 21, "core_switch", "DC1-BL-2", "border leaf", size=7.5, name_size=5.2)
d.link("bl1", "bl2", "mlag", a_side="e", b_side="w")
d.line([(YBUS_X, 27), (74, 27)], "vrf", lw=1.4)
d.tag(YBUS_X + 0.5, 37, "VRF subinterfaces\nto the BLs", color=BLUE_T, size=4.3)

d.group("fwg", 74, 48, 46, 22, "HRP pair")
d.node("fw1", 85, 56, "firewall", "DC1-FW-1", "USG6875G · active", size=7.5, name_size=5.2)
d.node("fw2", 109, 56, "firewall", "DC1-FW-2", "USG6875G · standby", size=7.5, name_size=5.2)
d.link("fw1", "fw2", "mlag", a_side="e", b_side="w")
d.tag(97, 52, "HRP 2 × 100GE", color="#1F3864", size=4.2)
d.link((97, 33), (97, 48), "fw", double=True)
d.tag(97, 40.5, "one 802.1Q subinterface\nand one /29 per VRF", color="#C00000", size=4.2)

d.note(73.5, 74, "One security zone per VRF,\ndefault deny; every denied\nsession is logged in HiSec\nInsight.\n\n"
       "Zone priorities:\nMGMT 95 · DC 90 · STAFF 82\nVOICE 75 · STUDENT 60\nPRINT 55 · DMZ 50 · CCTV 48\n"
       "IOT 45 · GUEST 40 · Internet 5\n\n"
       "Rules P01–P11 (policy matrix):\none rule per server group and\nport set; IPS on every permit;\n"
       "AV, URL filter and SAC towards\nthe Internet.\n\n"
       "The address plan has no\noverlaps, so the FW needs\none routing table only.", size=4.5, color=INK)

# ---------------------------------------------------------------- right: INTERNET, DMZ, DC
d.zone(128, 3, 49, 38, "VRF INTERNET", "own AS · ISP A + ISP B · RPKI · FlowSpec", kind="internet", title_size=5.8)
d.cloud("ia", 140, 18, "ISP A", size=11)
d.cloud("ib", 164, 18, "ISP B", size=11)
d.node("er", 152, 32, "core_router", "DC1-ER-1, 2", "NE8000E F1A", size=6.5, stack=2, pos="right", name_size=4.9)
d.link("ia", "er", "inet", a_side="s", b_side="w", route="vh")
d.link("ib", "er", "inet", a_side="s", b_side="e", route="vh", b_off=0)
d.line([(120, 59), (124, 59), (124, 32), (148.4, 32)], "inet")
d.tag(136, 37.5, "zone untrust · NAT44 · SSL VPN", color="#7030A0", size=4.2)

d.zone(128, 45, 49, 44, "VRF DMZ · 10.210.1.0/24", "VMs in the DC fabric · gateway = FW", kind="room", title_size=5.8)
d.node("dmz", 136, 63, "web_server", size=7)
d.text(142, 55.5, "From the Internet:", size=4.5, weight="bold", bg=False)
for i, (ip, what) in enumerate([(".10", "web site proxy · HTTPS"), (".11", "LMS proxy · HTTPS"),
                                (".12", "Jitsi Meet web · HTTPS"), (".14", "TURN relay · 3478, 5349"),
                                ("anycast /24", "authoritative DNS")]):
    yy = 59.5 + i * 3.6
    d.text(142, yy, ip, size=4.4, color=INK, bg=False)
    d.text(142 + (12 if ip.startswith("any") else 5.5), yy, what, size=4.4, color=GREY, bg=False)
d.line([(120, 63), (126, 63), (126, 63), (132.5, 63)], "fw")

d.zone(128, 93, 49, 51, "VRF DC · 10.200.0.0/16", "server leafs · reached only through the FW", kind="room",
       title_size=5.8)
d.node("dc", 136, 112, "general_server", size=7, stack=2)
for i, (ip, what) in enumerate([(".10.x", "DHCP, DNS, NTP, NCE + RADIUS,"), ("", "jump hosts, Samba AD, EJBCA, SIEM"),
                                (".20.x", "Moodle, PostgreSQL"), (".30.x", "Jitsi bridges, Jibri"),
                                (".40.x", "Asterisk, Kamailio SBC"), (".50.x", "PaperCut, VMS, ACS / BMS")]):
    yy = 104 + i * 3.8
    d.text(142, yy, ip, size=4.4, color=INK, bg=False)
    d.text(149, yy, what, size=4.4, color=GREY, bg=False)
d.line([(110, 70), (110, 115), (132.5, 115)], "fw")
d.tag(121, 115, "zone DC", color="#C00000", size=4.2)
d.tag(127.5, 68.5, "zone dmz", color="#C00000", size=4.2)

d.legend([("vrf", "VRF subinterfaces to the border leafs"), ("fw", "FW ↔ security zones"),
          ("inet", "Internet side"), ("mlag", "M-LAG / HRP"), "double"], 5, 151, w=170, size=4.7)
d.save()
