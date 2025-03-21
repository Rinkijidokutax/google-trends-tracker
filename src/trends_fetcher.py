import time
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime
import logging
from config import REGION, TIME_PERIODS, STOCK_KEYWORDS

class GoogleTrendsFetcher:
    def __init__(self, region=REGION):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.region = region
        self.logger = logging.getLogger(__name__)
    
    def fetch_trending_searches(self, period="daily"):
        """
        Fetch trending searches for a specific time period.
        
        Args:
            period (str): 'daily', 'weekly', or 'monthly'
            
        Returns:
            pandas.DataFrame: DataFrame with trending searches
        """
        try:
            self.logger.info(f"Fetching {period} trending searches for region {self.region}")
            
            if period == "daily":
                trends_df = self.pytrends.trending_searches(pn=self.region)
                trends_df.columns = ['Search Term']
                trends_df['Rank'] = range(1, len(trends_df) + 1)
                trends_df = trends_df[['Rank', 'Search Term']]
            else:
                # For weekly and monthly, we need to use different approach
                # Get top 20 trending searches for specified period
                time_frame = TIME_PERIODS[period]
                self.pytrends.build_payload(kw_list=[''], timeframe=time_frame, geo=self.region)
                trends_df = self.pytrends.trending_searches(pn=self.region)
                trends_df.columns = ['Search Term']
                trends_df['Rank'] = range(1, len(trends_df) + 1)
                trends_df = trends_df[['Rank', 'Search Term']]
            
            trends_df['Period'] = period.capitalize()
            trends_df['Date'] = datetime.now().strftime("%Y-%m-%d")
            
            return trends_df
        
        except Exception as e:
            self.logger.error(f"Error fetching {period} trending searches: {str(e)}")
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=['Rank', 'Search Term', 'Period', 'Date'])
    
    def fetch_stock_market_trends(self, keywords=STOCK_KEYWORDS, time_periods=TIME_PERIODS):
        """
        Fetch stock market related search trends.
        
        Args:
            keywords (list): List of stock market related keywords to track
            time_periods (dict): Dictionary of time periods to fetch data for
            
        Returns:
            dict: Dictionary of DataFrames with stock market trends by period
        """
        results = {}
        
        for period_name, timeframe in time_periods.items():
            try:
                self.logger.info(f"Fetching stock market trends for {period_name} period")
                
                # We can only fetch 5 keywords at a time
                all_data = []
                
                for i in range(0, len(keywords), 5):
                    batch_keywords = keywords[i:i+5]
                    
                    # Wait between requests to avoid rate limiting
                    if i > 0:
                        time.sleep(1)
                    
                    self.pytrends.build_payload(
                        kw_list=batch_keywords,
                        cat=0,  # Category: All categories
                        timeframe=timeframe,
                        geo=self.region,
                        gprop=''  # Search type: web searches
                    )
                    
                    interest_over_time = self.pytrends.interest_over_time()
                    
                    if not interest_over_time.empty:
                        all_data.append(interest_over_time)
                
                if all_data:
                    # Merge all data
                    combined_df = pd.concat(all_data, axis=1)
                    # Remove duplicated date index
                    combined_df = combined_df.loc[:,~combined_df.columns.duplicated()]
                    # Drop isPartial column if exists
                    if 'isPartial' in combined_df.columns:
                        combined_df = combined_df.drop(columns=['isPartial'])
                    
                    results[period_name] = combined_df
                else:
                    self.logger.warning(f"No data returned for {period_name} period")
                    results[period_name] = pd.DataFrame()
            
            except Exception as e:
                self.logger.error(f"Error fetching stock market trends for {period_name} period: {str(e)}")
                results[period_name] = pd.DataFrame()
        
        return results
    
    def fetch_related_queries(self, keywords=STOCK_KEYWORDS, time_periods=TIME_PERIODS):
        """
        Fetch related queries for stock market keywords.
        
        Args:
            keywords (list): List of stock market related keywords to track
            time_periods (dict): Dictionary of time periods to fetch data for
            
        Returns:
            dict: Dictionary of related queries by keyword and period
        """
        results = {}
        
        for period_name, timeframe in time_periods.items():
            results[period_name] = {}
            
            for keyword in keywords:
                try:
                    self.logger.info(f"Fetching related queries for '{keyword}' ({period_name})")
                    
                    # Wait between requests to avoid rate limiting
                    time.sleep(0.5)
                    
                    self.pytrends.build_payload(
                        kw_list=[keyword],
                        cat=0,
                        timeframe=timeframe,
                        geo=self.region,
                        gprop=''
                    )
                    
                    related_queries = self.pytrends.related_queries()
                    
                    if related_queries and keyword in related_queries:
                        # Get top and rising queries
                        top_df = related_queries[keyword]['top']
                        rising_df = related_queries[keyword]['rising']
                        
                        results[period_name][keyword] = {
                            'top': top_df if isinstance(top_df, pd.DataFrame) else pd.DataFrame(),
                            'rising': rising_df if isinstance(rising_df, pd.DataFrame) else pd.DataFrame()
                        }
                    else:
                        self.logger.warning(f"No related queries for '{keyword}' ({period_name})")
                        results[period_name][keyword] = {
                            'top': pd.DataFrame(),
                            'rising': pd.DataFrame()
                        }
                
                except Exception as e:
                    self.logger.error(f"Error fetching related queries for '{keyword}' ({period_name}): {str(e)}")
                    results[period_name][keyword] = {
                        'top': pd.DataFrame(),
                        'rising': pd.DataFrame()
                    }
        
        return results
    
    def fetch_all_data(self):
        """
        Fetch all Google Trends data.
        
        Returns:
            dict: Dictionary containing all fetched data
        """
        try:
            self.logger.info("Starting to fetch all Google Trends data")
            
            # Fetch trending searches for different time periods
            daily_trends = self.fetch_trending_searches("daily")
            weekly_trends = self.fetch_trending_searches("weekly")
            monthly_trends = self.fetch_trending_searches("monthly")
            
            # Fetch stock market related trends
            stock_trends = self.fetch_stock_market_trends()
            
            # Fetch related queries for stock market keywords
            related_queries = self.fetch_related_queries()
            
            return {
                "trending_searches": {
                    "daily": daily_trends,
                    "weekly": weekly_trends,
                    "monthly": monthly_trends
                },
                "stock_trends": stock_trends,
                "related_queries": related_queries
            }
        
        except Exception as e:
            self.logger.error(f"Error fetching all data: {str(e)}")
            return None
