import os
import pandas as pd
from pytrends.request import TrendReq
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

class AdvancedTrendsFetcher:
    def __init__(self, 
                 regions: List[str] = ['US'], 
                 categories: List[str] = None,
                 output_dir: str = 'trends_output'):
        """
        Initialize Advanced Trends Fetcher
        
        :param regions: List of region codes (e.g., ['US', 'GB', 'CA'])
        :param categories: Optional list of Google Trends categories
        :param output_dir: Directory to save output files
        """
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.regions = regions
        self.categories = categories or []
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def fetch_top_keywords(self, 
                           timeframe: str = 'now 1-d', 
                           top_n: int = 50) -> pd.DataFrame:
        """
        Fetch top keywords across multiple regions
        
        :param timeframe: Google Trends timeframe
        :param top_n: Number of top keywords to return
        :return: DataFrame with top keywords
        """
        top_keywords_list = []
        
        # Fetch top keywords for each region
        for region in self.regions:
            try:
                # Daily trending searches
                daily_trends = self.pytrends.trending_searches(pn=region)
                
                # Add region column
                daily_trends['region'] = region
                daily_trends = daily_trends.head(top_n)
                
                top_keywords_list.append(daily_trends)
            except Exception as e:
                print(f"Error fetching trends for {region}: {e}")
        
        # Combine results from all regions
        if top_keywords_list:
            top_keywords_df = pd.concat(top_keywords_list, ignore_index=True)
            
            # Save to CSV
            output_path = os.path.join(self.output_dir, 'top_keywords.csv')
            top_keywords_df.to_csv(output_path, index=False)
            
            return top_keywords_df
        
        return pd.DataFrame()

    def analyze_keyword_demographics(self, 
                                     keywords: List[str], 
                                     timeframe: str = 'today 3-m') -> Dict[str, Any]:
        """
        Analyze demographic trends for given keywords
        
        :param keywords: List of keywords to analyze
        :param timeframe: Google Trends timeframe
        :return: Dictionary of demographic insights
        """
        demographic_insights = {}
        
        for keyword in keywords:
            try:
                # Fetch interest by region
                self.pytrends.build_payload([keyword], timeframe=timeframe)
                interest_by_region = self.pytrends.interest_by_region(resolution='REGION')
                
                # Fetch interest over time
                interest_over_time = self.pytrends.interest_over_time()
                
                # Analyze top regions
                top_regions = interest_by_region.nlargest(10, keyword)
                
                # Visualize regional interest
                plt.figure(figsize=(12, 6))
                top_regions[keyword].plot(kind='bar')
                plt.title(f'Top Regions - {keyword} Interest')
                plt.xlabel('Regions')
                plt.ylabel('Interest Score')
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f'{keyword}_regional_interest.png'))
                plt.close()
                
                # Store insights
                demographic_insights[keyword] = {
                    'top_regions': top_regions,
                    'time_series': interest_over_time
                }
                
                # Save detailed insights to CSV
                top_regions.to_csv(os.path.join(self.output_dir, f'{keyword}_top_regions.csv'))
                interest_over_time.to_csv(os.path.join(self.output_dir, f'{keyword}_time_series.csv'))
            
            except Exception as e:
                print(f"Error analyzing demographics for {keyword}: {e}")
        
        return demographic_insights

    def generate_comprehensive_report(self, 
                                      keywords: List[str] = None, 
                                      timeframe: str = 'today 3-m'):
        """
        Generate a comprehensive trends report
        
        :param keywords: Optional list of keywords to deep dive
        :param timeframe: Google Trends timeframe
        """
        # Fetch top keywords if not provided
        if not keywords:
            top_keywords_df = self.fetch_top_keywords()
            keywords = top_keywords_df['title'].tolist()[:50]
        
        # Analyze demographic trends
        demographic_insights = self.analyze_keyword_demographics(keywords, timeframe)
        
        # Create a summary report
        report_df = pd.DataFrame(columns=['Keyword', 'Top Regions', 'Peak Interest'])
        
        for keyword, insights in demographic_insights.items():
            top_regions = insights['top_regions']
            time_series = insights['time_series']
            
            report_df = report_df.append({
                'Keyword': keyword,
                'Top Regions': ', '.join(top_regions.index[:5]),
                'Peak Interest': time_series[keyword].max()
            }, ignore_index=True)
        
        # Save summary report
        report_df.to_csv(os.path.join(self.output_dir, 'trends_summary_report.csv'), index=False)
        
        print(f"Comprehensive report generated in {self.output_dir}")

def main():
    """
    Main function to run trends fetcher
    """
    # Initialize fetcher
    trends_fetcher = AdvancedTrendsFetcher(
        regions=['US', 'GB', 'CA'],
        output_dir='google_trends_output'
    )
    
    # Example keywords for stock market and crypto
    stock_keywords = [
        'Tesla stock', 'Bitcoin', 'Ethereum', 
        'Stock market', 'Cryptocurrency', 
        'Investment trends'
    ]
    
    # Generate comprehensive report
    trends_fetcher.generate_comprehensive_report(
        keywords=stock_keywords, 
        timeframe='today 3-m'
    )

if __name__ == '__main__':
    main()
