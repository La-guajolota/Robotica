# 📊 GUI Dashboard

This directory contains the source code for a dashboard that communicates with a PLC and a Firebase database.

---

## 📂 Files

- **`dashboard.py`**: A Streamlit application that displays the data from the PLC in a dashboard.
- **`conector_PLC.py`**: A script that connects to a Siemens S7 PLC using the `snap7` library and reads data from it.
- **`config.py`**: A configuration file for the Firebase connection.
- **`run.py`**: A script to run the PLC connector and the Streamlit dashboard.
- **`firebase-credentials.json`**: The credentials for the Firebase project.
- **`requirements.txt`**: A list of the required Python libraries.

---

## 🚀 Usage

To use this dashboard, you need to have the required libraries installed. You can install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

You also need to have a `firebase-credentials.json` file with your Firebase project credentials.

To run the dashboard, you can use the `run.py` script:

```bash
python3 run.py
```

This will start the PLC connector and the Streamlit dashboard. You can then access the dashboard in your browser at `http://localhost:8501`.
