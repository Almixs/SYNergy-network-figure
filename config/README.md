# Device configurations

Configurations of the 13 device roles of the SYNergy campus network, one file per role, as given in Appendix A of the design document `SYNergy_campus_HLD_LLD` v1.3 (24-10-2026). The same files are kept in the folder `config-equipment` on the project Google Drive.

| File | Appendix | Device | Name | Role | Software (Table 66) |
|---|---|---|---|---|---|
| [`A01_NE8000E-F1A_S1-PE-A.cfg`](A01_NE8000E-F1A_S1-PE-A.cfg) | A.1 | NetEngine 8000E F1A | S1-PE-A | PE and route reflector on fibre L4 | V800R025C10 |
| [`A02_NE8000E-F1A_DC1-ER-1.cfg`](A02_NE8000E-F1A_DC1-ER-1.cfg) | A.2 | NetEngine 8000E F1A | DC1-ER-1 | Internet edge | V800R025C10 |
| [`A03_AR8700-8_S2-WE-1.cfg`](A03_AR8700-8_S2-WE-1.cfg) | A.3 | NetEngine AR8700-8 | S2-WE-1 | WAN edge of Site 2 | V600R025C10 |
| [`A04_AR8700-8_DC1-HUB-1.cfg`](A04_AR8700-8_DC1-HUB-1.cfg) | A.4 | NetEngine AR8700-8 | DC1-HUB-1 | IPsec hub and VPN route reflector | V600R025C10 |
| [`A05_AR5710-S8T2XE-NRGL_S2-AR-A.cfg`](A05_AR5710-S8T2XE-NRGL_S2-AR-A.cfg) | A.5 | NetEngine AR5710-S8T2XE-NRGL | S2-AR-A | 5G last resort and out-of-band access | V600R025C10 |
| [`A06_S6750-H48Y8C_S1-A1-AGG-A.cfg`](A06_S6750-H48Y8C_S1-A1-AGG-A.cfg) | A.6 | CloudEngine S6750-H48Y8C | S1-A1-AGG-A | M-LAG and VXLAN gateway | V600R025C10 |
| [`A07_S5755-S48P8Y_S1-K3-F2-ACC-1.cfg`](A07_S5755-S48P8Y_S1-K3-F2-ACC-1.cfg) | A.7 | CloudEngine S5755-S48P8Y | S1-K3-F2-ACC-1 | access switch | V600R025C10 |
| [`A08_S5755-S24P8Y_S1-D1-STK.cfg`](A08_S5755-S24P8Y_S1-D1-STK.cfg) | A.8 | CloudEngine S5755-S24P8Y | S1-D1-STK | dormitory iStack | V600R025C10 |
| [`A09_S6730-H48X6C-V2_S1-A1-FT1-2.cfg`](A09_S6730-H48X6C-V2_S1-A1-FT1-2.cfg) | A.9 | CloudEngine S6730-H48X6C-V2 | S1-A1-FT1-2 | FTTO switch, ELV room 1 | V600R025C10 |
| [`A10_S5735-L8P4X-QA-V2_S1-A1-F1-R12-RU1.cfg`](A10_S5735-L8P4X-QA-V2_S1-A1-F1-R12-RU1.cfg) | A.10 | CloudEngine S5735-L8P4X-QA-V2 | S1-A1-F1-R12-RU1 | room unit | V600R025C10 |
| [`A11_CE6885L-48YS8CQ_DC1-BL-1.cfg`](A11_CE6885L-48YS8CQ_DC1-BL-1.cfg) | A.11 | CloudEngine CE6885L-48YS8CQ | DC1-BL-1 | DC border leaf | V300R025C10 |
| [`A12_USG6875G_DC1-FW-1.cfg`](A12_USG6875G_DC1-FW-1.cfg) | A.12 | HiSecEngine USG6875G | DC1-FW-1 | firewall pair of DC-1 | V600R025C10 |
| [`A13_AirEngine9703-S_AC-1.cfg`](A13_AirEngine9703-S_AC-1.cfg) | A.13 | AirEngine 9703-S | AC-1 | WLAN controller | V600R025C10 |

## How the configurations were written

- **Not tested in a simulator.** The Huawei network simulator does not contain most of the devices of the design (NetEngine 8000E F1A, NetEngine AR8700-8 and AR5710, CloudEngine S6750-H, S5755-S, S6730-H-V2, S5735-L-V2 and CE6885L, HiSecEngine USG6875G, AirEngine 9703-S) or their current software.
- **Written only from the official Huawei documentation.** Each file follows the configuration examples and configuration chapters listed in its header, with the commands of those examples; only the names, VLANs, VRFs, addresses and AS numbers of the design are put in. Where the nearest official example is for another model of the same software family, the header says which.
- **One file per role.** NCE-Campus turns each configuration into the template for every device of that role; names, VRFs, VLANs and addresses are those of the design document.
- **Placeholders.** Keys and secrets are shown as `<key>`, addresses given by the ISPs as `<...>`. Public addresses are documentation blocks (198.51.100.0/24, 192.0.2.0/24, 203.0.113.0/24, AS 64496-64500) until the RIPE blocks are assigned; 203.0.114.0/24 is a placeholder for the second public block, not a documentation block.
- **Text.** The configuration lines are those of the document; in the comments the typographic characters of the document (dashes, multiplication sign, arrows) are written in ASCII.

## Not configured by CLI

OceanStor Dorado storage, TaiShan servers and the iMaster NCE, HiSec Insight and SecoManager software have no network CLI of their own: they are set up through their installation guides and web interfaces, and their network side is the leaf ports and VRFs of the files above.
