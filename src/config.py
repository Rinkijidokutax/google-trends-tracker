import os

# Base configuration for Google Trends Tracker
CONFIG = {
    # Regions to track
    'regions': ['US', 'GB', 'CA'],
    
    # Output directory for reports and visualizations
    'output_dir': os.path.join(os.path.dirname(__file__), '..', 'google_trends_output'),
    
    # Keywords to track
    'keywords': [
        'Tesla stock', 'Bitcoin', 'Ethereum', 
        'Stock market', 'Cryptocurrency', 
        'Investment trends'
    ],
    
    # Timeframe for trend analysis
    'timeframe': 'today 3-m',
    
    # Email configuration (optional)
    'email_config': {
        'sender_email': 'your_email@example.com',
        'sender_password': 'your_password',
        'recipient_emails': ['recipient1@example.com'],
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
    },
    
    # Logging configuration
    'logging': {
        'level': 'INFO',
        'file': 'trends_tracker.log'
    }
}