import shutil
import smtplib
from email.mime.text import MIMEText

# Check disk usage
def check_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    usage_percent = (used / total) * 100
    return usage_percent

# Send email alert
def send_email_alert(usage, to_email):
    msg = MIMEText(f"Warning: Disk usage is at {usage:.2f}%!")
    msg['Subject'] = "Disk Space Alert"
    msg['From'] = "admin@example.com"
    msg['To'] = to_email

    with smtplib.SMTP('localhost') as server:
        server.sendmail("admin@example.com", [to_email], msg.as_string())

# Set threshold and monitor disk space
threshold = 80.0
disk_usage = check_disk_usage("/")

if disk_usage > threshold:
    send_email_alert(disk_usage, "admin@example.com")
    print(f"Disk usage is {disk_usage:.2f}%. Alert sent.")
else:
    print(f"Disk usage is {disk_usage:.2f}%. No alert needed.")
