# 📦 McLium

<p align="center">
  <img src="docs/assets/mclium_logo.png" width="500">
</p>

**McLium** is a penetration testing tool designed for analyzing and assessing the security of Minecraft server environments.

It provides a set of powerful built-in utilities along with an extendable plugin capability, allowing users to perform network inspection, protocol interaction, and controlled stress testing.

Additionally, McLium offers low-level packet crafting capabilities, giving users near - complete control over packet structure - from modifying individual bytes to constructing fully custom and non - compliant packets - enabling advanced testing scenarios such as protocol fuzzing, malformed packet injection, and boundary manipulation.
Core features include:  
> Port scanning <br>
> UDP/TCP flood simulation<br>
> Network behavior analysis<br>
> Protocol-level testing<br>

**McLium is developed strictly for educational purposes and authorized security research only.**

---
# 📄 Documentation

Comprehensive guides for developing and extending McLium:

- **Plugin Development Guide**  
  https://github.com/Notkenftr/McLium/blob/main/docs/how_to_make_a_plugin.md

- **Packet Creation Guide**  
  https://github.com/Notkenftr/McLium/tree/main/docs/how_to_create_a_packet.md
---
# 📑 Installation

## 1. Clone repository
```bash
git clone https://github.com/your-username/McLium.git
cd McLium
```

## 2. Create virtual environment (recommended)

### Linux / macOs
```bash
python -m venv .venv
source .venv/bin/activate   
```

### Window
```bash
python -m venv .venv
.venv\Scripts\activate 
```

## 3. Run McLium
```bash
python Mclium.py --help
```
