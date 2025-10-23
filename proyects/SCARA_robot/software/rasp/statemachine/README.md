# 🔄 State Machine

This directory contains the source code for a state machine that controls the robot.

---

## 📂 Files

- **`main.py`**: The main entry point for the application, which initializes the state machine and the PLC communication.
- **`states.py`**: Implements the core logic of the application by managing states and transitions.
- **`box_detector.py`**: Manages camera operations, detects geometric shapes on boxes, and sends data to a server.
- **`plc_communication.py`**: Handles network communication with a Siemens S7 PLC using the `snap7` library.
- **`console_styler.py`**: A utility for styling the console output.

---

## 🚀 Usage

To run the state machine, you can use the `main.py` script:

```bash
python3 main.py
```

The application will prompt you to select between a real PLC and a simulator. If you choose the real PLC, you will need to provide the IP address of the PLC.
