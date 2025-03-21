import os
from advanced_trends_fetcher import AdvancedTrendsFetcher
from config import CONFIG

def main():
    """
    Main entry point for Google Trends Tracker
    """
    # Initialize trends fetcher with configuration
    trends_fetcher = AdvancedTrendsFetcher(
        regions=CONFIG['regions'],
        output_dir=CONFIG['output_dir']
    )
    
    # Fetch keywords from configuration
    keywords = CONFIG.get('keywords', [
        'Tesla stock', 'Bitcoin', 'Ethereum', 
        'Stock market', 'Cryptocurrency', 
        'Investment trends'
    ])
    
    # Generate comprehensive report
    trends_fetcher.generate_comprehensive_report(
        keywords=keywords,
        timeframe=CONFIG.get('timeframe', 'today 3-m')
    )

if __name__ == '__main__':
    main()