import cv2
import json
import tkinter as tk
import time
import os
import serial  # Import pyserial


# Function to load scan counts from the JSON file
def load_scan_counts():
    if os.path.exists('scan_counts.json'):
        with open('scan_counts.json', 'r') as file:
            return json.load(file)
    return {}

# Function to save scan counts to the JSON file
def save_scan_counts(scan_counts):
    with open('scan_counts.json', 'w') as file:
        json.dump(scan_counts, file)

# Function to extract and display QR code details
def detect_qr_code():
    # Load the scan counts from the JSON file (persistent storage)
    scan_counts = load_scan_counts()

    # Open the webcam
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and decode QR code
        data, bbox, _ = detector.detectAndDecode(frame)

        # If QR code is detected
        if bbox is not None and data:
            try:
                # Parse the QR code data as JSON
                qr_data = json.loads(data)

                # Extract details
                unique_key = qr_data.get("security_key", "N/A")
                name = qr_data.get("name", "N/A")
                scans_allowed = int(qr_data.get("scans_allowed", 0))
                expiration_time = qr_data.get("expiration_time", "N/A")
                level = qr_data.get("level", "N/A")
                generated_time = qr_data.get("generated_time", "N/A")

                # Convert timestamp to a human-readable format
                if generated_time != "N/A":
                    generated_time = time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(generated_time)
                    )

                # Check if the scan count exists for the unique QR code
                if unique_key not in scan_counts:
                    scan_counts[unique_key] = 0  # Initialize the scan count

                # Increment the scan count
                scan_counts[unique_key] += 1

                # Check if the scan limit is reached
                if scan_counts[unique_key] > scans_allowed:
                    display_scan_limit_reached_gui()
                    break  # Stop the scanning process

                # Display the scan count and remaining scans
                remaining_scans = scans_allowed - scan_counts[unique_key]
                display_gui(unique_key, name, scans_allowed, expiration_time, level, generated_time, remaining_scans)

                # Save updated scan counts to the JSON file
                save_scan_counts(scan_counts)

                # Rotate the servo via COM3 if the QR is valid
                rotate_servo()

                return

            except json.JSONDecodeError:
                print("Invalid QR code data format")

        # Display the webcam feed
        cv2.imshow("QR Code Scanner", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


# Function to display details in a separate GUI window
def display_gui(unique_key, name, scans_allowed, expiration_time, level, generated_time, remaining_scans):
    # Create a Tkinter window
    root = tk.Tk()
    root.title("QR Code Details")

    # Set window dimensions
    root.geometry("450x400")

    # Add labels to display details
    tk.Label(root, text="QR Code Details", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(root, text=f"Security Key: {unique_key}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Name: {name}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Scans Allowed: {scans_allowed}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Expiration Time: {expiration_time} seconds", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Level: {level}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Generated Time: {generated_time}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Remaining Scans: {remaining_scans}", font=("Helvetica", 12, "bold")).pack(pady=15)

    # Add a button to close the window
    tk.Button(root, text="Close", command=root.destroy, font=("Helvetica", 12)).pack(pady=20)

    # Run the GUI
    root.mainloop()


# Function to display the "Scan Limit Reached" pop-up
def display_scan_limit_reached_gui():
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Scan Limit Reached")

    # Set window dimensions
    root.geometry("300x150")

    # Add label to inform the user
    tk.Label(root, text="Scan Limit Reached!", font=("Helvetica", 14, "bold")).pack(pady=30)

    # Add a button to close the window
    tk.Button(root, text="Close", command=root.destroy, font=("Helvetica", 12)).pack()

    # Run the GUI
    root.mainloop()


# Function to rotate the servo via COM3 (Arduino)
def rotate_servo():
    try:
        # Connect to Arduino via COM3
        ser = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize

        # Send a command to rotate the servo
        ser.write(b'r')  # Send the 'r' command to rotate the servo
        time.sleep(1)    # Wait for the servo to rotate

        ser.close()  # Close the serial connection
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")


if __name__ == "__main__":
    detect_qr_code()
