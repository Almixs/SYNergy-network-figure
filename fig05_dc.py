from hwdraw import Diagram

d = Diagram(180, 166, "fig05_dc")

d.zone(4, 22, 172, 130, "DC-1 · own room in the basement of the Site 1 administrative building",
       "DC-2 (own cage in ISP B's Tier III hall) is built the same way: own ERs, FW pair and hubs; AC-2 (pair 1, standby) and AC-3 (pair 2, active); NCE DR copy",
       kind="dc", title_pos="bottom")

# ---- Internet
d.cloud("ispa", 52, 10, "ISP A", None)
d.cloud("ispb", 92, 10, "ISP B", None)
d.note(112, 8, "clean-pipe scrubbing from both ISPs\nRTBH and FlowSpec from our ERs", size=4.7)

# ---- Internet edge pair
d.group("erg", 32, 28, 80, 22, "own AS · full BGP tables")
d.node("er1", 52, 35, "core_router", "DC1-ER-1", "NetEngine 8000E F1A")
d.node("er2", 92, 35, "core_router", "DC1-ER-2", "NetEngine 8000E F1A")
d.link("er1", "er2", "ibgp", a_side="e", b_side="w")
d.tag(72, 35, "iBGP · RPKI · FlowSpec", color="#7030A0", size=4.6)
d.link("ispa", "er1", "inet", a_side="s", b_side="n", label="100GE")
d.link("ispb", "er2", "inet", a_side="s", b_side="n", label="100GE")

# ---- IPsec hubs
d.node("hub", 16, 39, "core_router", "DC1-HUB-1…4", "AR8700-8", "IPsec hubs", pos="above", stack=3)
d.link("hub", "erg", "uplink", a_side="e", b_side="w", double=True)
d.line([(19, 43.5), (36, 62)], "pe", double=True)
d.tag(26, 48, "10GE", color="#404040", size=4.4)

# ---- Border leaf pair
d.group("blg", 32, 62, 80, 22, "M-LAG")
d.node("bl1", 52, 69, "core_switch", "DC1-BL-1", "CE6885L-48YS8CQ · border leaf")
d.node("bl2", 92, 69, "core_switch", "DC1-BL-2", "CE6885L-48YS8CQ · border leaf")
d.link("bl1", "bl2", "mlag", a_side="e", b_side="w")
d.tag(72, 69, "peer-link 4 × 25GE", color="#1F3864", size=4.4)
d.link((72, 50), (72, 62), "inet", double=True)
d.tag(86, 56, "2 × 100GE per ER · VRF INTERNET", color="#7030A0", size=4.6)

# ---- PEs of fibre L4
d.node("pea", 15, 67, "core_router", "S1-PE-A", "NE8000E F1A", "fibre L4")
d.node("peb", 15, 88, "core_router", "S1-PE-B", "NE8000E F1A", "fibre L4")
d.link("pea", (32, 67), "pe", a_side="e", double=True)
d.line([(20, 86), (32, 80)], "pe", double=True)
d.note(6, 104.5, "PE: 4 × 100GE (L4, PE-PE,\nBL-1, BL-2) · per-VRF eBGP\nto the PEs and hubs", size=4.5)

# ---- Firewall pair
d.group("fwg", 128, 58, 48, 42, "HRP pair")
d.node("fw1", 140, 67, "firewall", "DC1-FW-1", "USG6875G", "HRP active", pos="right")
d.node("fw2", 140, 89, "firewall", "DC1-FW-2", "USG6875G", "HRP standby", pos="right")
d.link("fw1", "fw2", "mlag", a_side="s", b_side="n")
d.tag(140, 78, "HRP 2 × 100GE", color="#1F3864", size=4.4)
d.link((112, 73), (128, 73), "fw", double=True)
d.tag(120, 79, "2 × 100GE\nper FW", color="#C00000", size=4.4)
d.note(129, 103, "The only gateway between the VRFs and to the\nInternet: IPS, AV, URL filter, NAT44, SSL VPN.\nOne 802.1Q subinterface per VRF towards the BLs.", size=4.6)

# ---- Server leaf pair
d.group("slg", 32, 96, 80, 22, "M-LAG")
d.node("sl1", 52, 103, "tor_switch", "DC1-SL-1", "CE6885L-48YS8CQ · server leaf")
d.node("sl2", 92, 103, "tor_switch", "DC1-SL-2", "CE6885L-48YS8CQ · server leaf")
d.link("sl1", "sl2", "mlag", a_side="e", b_side="w")
d.tag(72, 103, "peer-link", color="#1F3864", size=4.4)
d.link((72, 84), (72, 96), "uplink", double=True)
d.tag(96, 90, "4 × 100GE (BL ↔ SL full mesh) · EVPN-VXLAN · L3 VNI per VRF", color="#404040", size=4.6)

# ---- Servers, storage, management
ends = [("srv", 14, "general_server", "Servers × 12", "TaiShan 200 · DCS", "LMS, PBX, AD, DNS", 3),
        ("lec", 43, "multicast_server", "Lecture hosts × 7", "TaiShan 200", "Jitsi bridges, Jibri", 2),
        ("dmz", 72, "web_server", "DMZ VMs", "web, LMS front-end", "authoritative DNS", 1),
        ("sto", 101, "storage_array", "OceanStor Dorado 3000", "HyperMetro with DC-2", "RPO 0 · quorum Site 3", 1),
        ("nce", 130, "general_nms", "Management", "NCE-Campus, NCE-Fabric", "SecoManager, HiSec Insight", 1),
        ("ac", 159, "ac", "WLAN AC-1, AC-4", "AirEngine 9703-S", "HSB with AC-2, AC-3", 2)]
for key, x, ic, n, m, s, st in ends:
    d.node(key, x, 129, ic, n, m, s, size=9, stack=st)
    top = 129 - d.n[key]["h"] / 2 - (1.4 if st > 1 else 0)
    bx = min(max(x, 36), 108)
    d.line([(x, top), (bx, 118)], "server", double=True)
d.tag(140, 120, "2 × 25GE per server, one to each server leaf", color="#7F7F7F", size=4.6)

d.legend(["inet", ("ibgp", "iBGP between the ERs"), ("pe", "PE, hub ↔ border leaf (100GE, 10GE)"),
          ("uplink", "Hub ↔ ER (10GE) · BL ↔ SL fabric"), "fw", ("mlag", "M-LAG peer-link / HRP"),
          "server", "double"], 6, 158, w=168, size=4.8)
d.save()
