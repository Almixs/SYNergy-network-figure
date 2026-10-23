YA, YB, RH = 8, 15, 4.2


def rails(d, x1=14, x2=176):
    d.rail(x1, x2, YA, RH, "ISP A", "10GE business line to every WAN edge AR, separate building entry",
           icon="network_cloud_2")
    d.rail(x1, x2, YB, RH, "ISP B", "10GE business line to every WAN edge AR, separate building entry",
           icon="network_cloud_2")


def to_rails(d, x, ytop):
    """Two ISP lines from the top of a WAN edge AR at x to both rails."""
    d.line([(x - 1.6, ytop), (x - 1.6, YB + RH / 2)], "isp")
    d.dot(x - 1.6, YB + RH / 2, "#C55A11", r=0.5)
    d.line([(x + 1.6, ytop), (x + 1.6, YA + RH / 2)], "isp", z=1.4)
    d.dot(x + 1.6, YA + RH / 2, "#C55A11", r=0.5)
