import qrcode
import tkinter as tk
from tkinter import messagebox
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Function to send the QR code via email
def send_email():
    recipient_email = email_entry.get()
    if not recipient_email:
        messagebox.showwarning("Warning", "Please enter a recipient email.")
        return

    try:
        # Email credentials (use a test email for this purpose)
        sender_email = "projectsss@gmail.com"  # Replace with your email
        sender_password = "owae xxx xxxca xxf"  # Replace with your email's password

        # Create email content
        subject = "Your Generated QR Code"
        body = "Here is your QR code with the requested details."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the QR code image
        filename = "generated_qr.png"
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)

        # Connect to the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", f"QR Code sent to {recipient_email}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")


# Generate QR Code with details
def generate_qr():
    unique_key = security_key_entry.get()
    name = name_entry.get()
    scans_allowed = scans_entry.get()
    expiration_time = expiration_entry.get()
    level = level_entry.get()

    # Create a dictionary to store the details
    qr_details = {
        'security_key': unique_key,
        'name': name,
        'scans_allowed': int(scans_allowed),
        'expiration_time': int(expiration_time),
        'level': level,
        'generated_time': time.time()  # Timestamp for when the QR code was generated
    }

    # Convert the dictionary to JSON format
    qr_data = json.dumps(qr_details)

    # Create QR code
    qr = qrcode.make(qr_data)
    qr.save("generated_qr.png")  # Save QR code image

    messagebox.showinfo("Success", "QR Code generated successfully and saved as 'generated_qr.png'")


# GUI Setup
root = tk.Tk()
root.title("QR Code Generator")

# Input fields for details
tk.Label(root, text="Security Key").grid(row=0, column=0)
security_key_entry = tk.Entry(root)
security_key_entry.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Scans Allowed").grid(row=2, column=0)
scans_entry = tk.Entry(root)
scans_entry.grid(row=2, column=1)

tk.Label(root, text="Expiration Time (minutes)").grid(row=3, column=0)
expiration_entry = tk.Entry(root)
expiration_entry.grid(row=3, column=1)

tk.Label(root, text="Level").grid(row=4, column=0)
level_entry = tk.Entry(root)
level_entry.grid(row=4, column=1)

tk.Label(root, text="Recipient Email").grid(row=5, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=5, column=1)

# Generate QR button
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.grid(row=6, column=0, columnspan=2)

# Send Email button
send_email_button = tk.Button(root, text="Send QR via Email", command=send_email)
send_email_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
