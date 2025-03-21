import os
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
from trends_fetcher import GoogleTrendsFetcher
from excel_generator import ExcelReportGenerator
from email_sender import EmailSender
from config import LOG_FILE

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_and_send_report(report_type="daily"):
    """
    Generate a Google Trends report and send it via email.
    
    Args:
        report_type (str): Type of report to generate (daily, weekly, monthly)
        
    Returns:
        bool: True if report was generated and sent successfully, False otherwise
    """
    try:
        logger.info(f"Generating {report_type} report")
        
        # Check for required environment variables
        if not os.environ.get("EMAIL_SENDER") or not os.environ.get("EMAIL_PASSWORD"):
            logger.warning("Email credentials not set. Report will be generated but not sent.")
        
        # Create Google Trends fetcher
        fetcher = GoogleTrendsFetcher()
        
        # Fetch all data
        data = fetcher.fetch_all_data()
        
        if data is None:
            logger.error("Failed to fetch Google Trends data")
            return False
        
        # Generate Excel report
        excel_generator = ExcelReportGenerator()
        report_path = excel_generator.create_report(data, include_charts=True)
        
        if report_path is None:
            logger.error("Failed to generate Excel report")
            return False
        
        # Check if email credentials are available
        if os.environ.get("EMAIL_SENDER") and os.environ.get("EMAIL_PASSWORD") and os.environ.get("EMAIL_RECIPIENT"):
            # Send report via email
            email_sender = EmailSender()
            email_sent = email_sender.send_report(report_path, report_type)
            
            if not email_sent:
                logger.warning("Failed to send email, but report was generated")
                return False
        else:
            logger.info(f"Report generated successfully at {report_path} (not sent via email)")
        
        logger.info(f"{report_type.capitalize()} report process completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error generating/sending report: {str(e)}")
        return False

def main():
    """
    Main function to run the Google Trends Tracker.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate Google Trends reports")
    parser.add_argument(
        "--type",
        choices=["daily", "weekly", "monthly"],
        default="daily",
        help="Type of report to generate (default: daily)"
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Generate report without sending email"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no-email flag is set, temporarily clear email settings
    if args.no_email:
        original_email = os.environ.get("EMAIL_SENDER")
        os.environ["EMAIL_SENDER"] = ""
    
    # Generate and send report
    success = generate_and_send_report(args.type)
    
    # Restore email settings if they were changed
    if args.no_email and original_email:
        os.environ["EMAIL_SENDER"] = original_email
    
    return 0 if success else 1

if __name__ == "__main__":
    main()
