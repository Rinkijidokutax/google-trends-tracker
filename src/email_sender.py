import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import logging
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SMTP_SERVER, SMTP_PORT

class EmailSender:
    def __init__(self):
        self.sender = EMAIL_SENDER
        self.password = EMAIL_PASSWORD
        self.recipient = EMAIL_RECIPIENT
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.logger = logging.getLogger(__name__)
    
    def send_report(self, report_path, report_type="daily"):
        """
        Send the Excel report via email.
        
        Args:
            report_path (str): Path to the Excel report file
            report_type (str): Type of report (daily, weekly, monthly)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            self.logger.info(f"Sending {report_type} report email")
            
            # Check if credentials are available
            if not all([self.sender, self.password, self.recipient]):
                self.logger.error("Email credentials missing. Check your .env file.")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.recipient
            msg['Subject'] = f"Google Trends {report_type.capitalize()} Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Add body text
            body = f"""
            <html>
            <body>
                <h2>Google Trends Report</h2>
                <p>Please find attached the {report_type} Google Trends report.</p>
                <p>This report includes:</p>
                <ul>
                    <li>Top trending searches for the past day, week, and month</li>
                    <li>Stock market and trading related search trends</li>
                    <li>Related queries and rising search terms</li>
                </ul>
                <p>This report was automatically generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}.</p>
                <p>Regards,<br>Google Trends Tracker</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))
            
            # Attach the report
            with open(report_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='xlsx')
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(report_path))
                msg.attach(attachment)
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to {self.recipient}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False
