# Event-gate-QR

# QR-Based Event Gate System

## 📌 Project Overview
The **QR-Based Event Gate System** is designed to control access to an event using QR codes with a limited lifespan and scan count. Each QR code contains event details and restrictions, such as the number of allowed scans and an expiration time. Upon successful scanning, the system validates the QR, updates scan counts, and controls a servo motor (for gate access) through an Arduino.

## 🔧 Features
- 📷 **Real-time QR code scanning** via webcam.
- ⏳ **QR lifespan management** with expiration time.
- 🔄 **Limited scan counts** for each QR code.
- 🔍 **Validation of QR data** (security key, user details, scan limits).
- 🎭 **Graphical User Interface (GUI)** for displaying QR details.
- ⚙️ **Automated gate access** via a servo motor controlled through an Arduino.
- 💾 **Persistent data storage** using JSON for tracking scan counts.

## 🏗️ System Workflow
1. The system scans a QR code using OpenCV.
2. Extracts and verifies details from the QR.
3. Checks if the QR is still valid (scan count & expiration time).
4. Displays the details in a GUI window.
5. If valid, increments scan count and allows access.
6. Rotates the servo motor (to open the gate) via Arduino communication.
7. If the scan limit is reached, denies access and shows a warning.

## 📂 Project Structure
```
qr-based-event-gate/
│── scan_counts.json      # Stores scanned QR data persistently
│── main.py               # QR scanning & validation logic
│── README.md             # Project documentation
│── requirements.txt      # Dependencies
└── arduino_code.ino      # Arduino script for servo control
```

## 🛠️ Installation & Setup
### 1️⃣ Prerequisites
Ensure you have the following installed:
- Python 3.x
- OpenCV (`cv2`)
- Tkinter (for GUI)
- PySerial (for Arduino communication)

### 2️⃣ Install Dependencies
```bash
pip install opencv-python pyserial
```

### 3️⃣ Run the Program
```bash
python main.py
```

## 🔌 Hardware Requirements
- Webcam (for scanning QR codes)
- Arduino board
- Servo motor
- USB connection (for serial communication)

## 🛠️ Arduino Setup
1. Connect the servo motor to Arduino.
2. Upload the provided `arduino_code.ino` file.
3. Ensure the correct COM port is used in `main.py`.

## 📸 Demo
![Screenshot 2024-11-28 201235](https://github.com/user-attachments/assets/e753bafd-2e1d-49d9-a0e4-33b50c2be6d5)
![Screenshot 2024-11-24 224407](https://github.com/user-attachments/assets/ac2ed98b-8ab2-47a8-a99c-e66b138052fd)


## 📝 Future Enhancements
- 🔒 Encrypt QR data for security.
- 📡 Cloud-based validation for QR codes.
- 📱 Mobile app integration.
- 📊 Admin dashboard for monitoring entry logs.

## 📜 License
This project is open-source under the [MIT License](LICENSE).

## 🤝 Contributions
Feel free to fork the repository and submit pull requests!

---
Made with ❤️ for secure event management 🚀

