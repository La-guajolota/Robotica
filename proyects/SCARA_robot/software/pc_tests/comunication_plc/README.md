# 📡 PLC Communication

This directory contains scripts for testing the communication with a PLC using Modbus TCP/IP.

---

## 📂 Files

- **`modbusTCPIP.py`**: A script that uses the `snap7` library to communicate with a Siemens S7 PLC.
- **`PRUEBA_ESCRITURA.py`**: A script for testing the writing of integer and boolean values to the PLC.

---

## 🚀 Usage

To use these scripts, you need to have the `snap7` library installed. You can install it using pip:

```bash
pip install python-snap7
```

You also need to have a Siemens S7 PLC connected to the same network as your computer. You can then run the scripts from the terminal, making sure to change the IP address of the PLC in the scripts to match your setup.
