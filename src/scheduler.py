import os
import time
import schedule
import logging
from datetime import datetime
import threading
from config import DAILY_REPORT_TIME, WEEKLY_REPORT_DAY, WEEKLY_REPORT_TIME, MONTHLY_REPORT_DAY, MONTHLY_REPORT_TIME
from main import generate_and_send_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "scheduler.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_threaded(job_func, *args, **kwargs):
    """
    Run a job in a separate thread to avoid blocking the scheduler.
    """
    job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
    job_thread.start()

def schedule_reports():
    """
    Schedule daily, weekly, and monthly reports.
    """
    # Schedule daily report
    schedule.every().day.at(DAILY_REPORT_TIME).do(run_threaded, generate_and_send_report, "daily")
    logger.info(f"Daily report scheduled for {DAILY_REPORT_TIME}")
    
    # Schedule weekly report
    schedule.every().monday.at(WEEKLY_REPORT_TIME).do(run_threaded, generate_and_send_report, "weekly")
    logger.info(f"Weekly report scheduled for {WEEKLY_REPORT_DAY} at {WEEKLY_REPORT_TIME}")
    
    # Schedule monthly report (on specified day of month)
    def monthly_job():
        # Check if today is the specified day of the month
        if datetime.now().day == MONTHLY_REPORT_DAY:
            generate_and_send_report("monthly")
    
    # Check daily at the specified time if it's the monthly report day
    schedule.every().day.at(MONTHLY_REPORT_TIME).do(run_threaded, monthly_job)
    logger.info(f"Monthly report scheduled for day {MONTHLY_REPORT_DAY} at {MONTHLY_REPORT_TIME}")

def run_scheduler():
    """
    Run the scheduler continuously.
    """
    schedule_reports()
    
    logger.info("Scheduler started")
    logger.info("Press Ctrl+C to exit")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    run_scheduler()
