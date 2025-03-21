import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging
from config import OUTPUT_DIR

class ExcelReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_report(self, data, include_charts=True):
        """
        Create Excel report from Google Trends data.
        
        Args:
            data (dict): Dictionary containing all Google Trends data
            include_charts (bool): Whether to include charts in the report
            
        Returns:
            str: Path to the created Excel file
        """
        try:
            self.logger.info("Creating Excel report")
            
            # Create timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_trends_report_{timestamp}.xlsx"
            file_path = os.path.join(OUTPUT_DIR, filename)
            
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # Add title format
                title_format = workbook.add_format({
                    'bold': True,
                    'font_size': 16,
                    'align': 'center',
                    'valign': 'vcenter',
                    'font_color': '#0366d6',
                    'border': 1
                })
                
                # Add header format
                header_format = workbook.add_format({
                    'bold': True,
                    'font_size': 12,
                    'align': 'center',
                    'valign': 'vcenter',
                    'bg_color': '#D9D9D9',
                    'border': 1
                })
                
                # Add date cell format
                date_format = workbook.add_format({
                    'num_format': 'yyyy-mm-dd',
                    'align': 'center'
                })
                
                # Create summary sheet
                self._create_summary_sheet(writer, data, title_format, header_format)
                
                # Create trending searches sheets
                self._create_trending_searches_sheets(writer, data, title_format, header_format)
                
                # Create stock market trends sheets
                self._create_stock_trends_sheets(writer, data, title_format, header_format, include_charts)
                
                # Create related queries sheets
                self._create_related_queries_sheets(writer, data, title_format, header_format)
            
            self.logger.info(f"Excel report created at {file_path}")
            return file_path
        
        except Exception as e:
            self.logger.error(f"Error creating Excel report: {str(e)}")
            return None
    
    def _create_summary_sheet(self, writer, data, title_format, header_format):
        """
        Create summary sheet with key findings.
        """
        try:
            summary_df = pd.DataFrame()
            worksheet = writer.book.add_worksheet('Summary')
            worksheet.set_column('A:A', 25)
            worksheet.set_column('B:B', 60)
            
            # Add title
            worksheet.merge_range('A1:B1', 'Google Trends Summary Report', title_format)
            worksheet.merge_range('A2:B2', f"Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}", writer.book.add_format({'align': 'center', 'italic': True}))
            
            # Add top daily searches
            row = 4
            worksheet.merge_range(f'A{row}:B{row}', 'Top 5 Daily Trending Searches', header_format)
            row += 1
            
            if 'trending_searches' in data and 'daily' in data['trending_searches']:
                daily_trends = data['trending_searches']['daily']
                if not daily_trends.empty and len(daily_trends) > 0:
                    for i in range(min(5, len(daily_trends))):
                        worksheet.write(f'A{row}', f"#{daily_trends.iloc[i]['Rank']}")
                        worksheet.write(f'B{row}', daily_trends.iloc[i]['Search Term'])
                        row += 1
            
            # Add top stock market trends
            row += 2
            worksheet.merge_range(f'A{row}:B{row}', 'Top Stock Market Trends', header_format)
            row += 1
            
            if 'stock_trends' in data and 'daily' in data['stock_trends']:
                stock_trends = data['stock_trends']['daily']
                if not stock_trends.empty and len(stock_trends.columns) > 0:
                    # Get the latest date
                    latest_date = stock_trends.index[-1]
                    # Get values for the latest date
                    latest_values = stock_trends.loc[latest_date]
                    # Sort by value descending
                    sorted_terms = latest_values.sort_values(ascending=False)
                    
                    for i, (term, value) in enumerate(sorted_terms.items()):
                        if i < 5:  # Top 5
                            worksheet.write(f'A{row}', term)
                            worksheet.write(f'B{row}', f"Interest score: {value}")
                            row += 1
            
            # Add insights
            row += 2
            worksheet.merge_range(f'A{row}:B{row}', 'Insights and Observations', header_format)
            row += 1
            
            # Add some basic insights
            insights = [
                "This report shows trending searches and stock market related trends from Google Trends.",
                "Daily trending searches show what people are searching for right now.",
                "Stock market trends show relative interest in trading and investment topics.",
                "Check individual sheets for more detailed data and charts.",
                "For stock market topics, look at related queries to find emerging themes."
            ]
            
            for insight in insights:
                worksheet.merge_range(f'A{row}:B{row}', insight, writer.book.add_format({'text_wrap': True}))
                row += 1
        
        except Exception as e:
            self.logger.error(f"Error creating summary sheet: {str(e)}")
    
    def _create_trending_searches_sheets(self, writer, data, title_format, header_format):
        """
        Create sheets for trending searches.
        """
        try:
            for period in ['daily', 'weekly', 'monthly']:
                if 'trending_searches' in data and period in data['trending_searches']:
                    trending_df = data['trending_searches'][period]
                    
                    if not trending_df.empty:
                        # Write to Excel
                        sheet_name = f"{period.capitalize()} Trends"
                        trending_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                        
                        # Get the xlsxwriter worksheet object
                        worksheet = writer.sheets[sheet_name]
                        
                        # Add title
                        worksheet.merge_range('A1:D1', f"{period.capitalize()} Trending Searches", title_format)
                        
                        # Make the columns wider for better visibility
                        worksheet.set_column('A:A', 10)  # Rank
                        worksheet.set_column('B:B', 50)  # Search Term
                        worksheet.set_column('C:C', 15)  # Period
                        worksheet.set_column('D:D', 15)  # Date
                        
                        # Format the header row
                        for col_num, value in enumerate(trending_df.columns.values):
                            worksheet.write(1, col_num, value, header_format)
        
        except Exception as e:
            self.logger.error(f"Error creating trending searches sheets: {str(e)}")
    
    def _create_stock_trends_sheets(self, writer, data, title_format, header_format, include_charts):
        """
        Create sheets for stock market trends.
        """
        try:
            for period in ['daily', 'weekly', 'monthly']:
                if 'stock_trends' in data and period in data['stock_trends']:
                    stock_df = data['stock_trends'][period]
                    
                    if not stock_df.empty and len(stock_df.columns) > 0:
                        # Write to Excel
                        sheet_name = f"Stock Trends {period.capitalize()}"
                        stock_df.to_excel(writer, sheet_name=sheet_name, startrow=1)
                        
                        # Get the xlsxwriter worksheet object
                        worksheet = writer.sheets[sheet_name]
                        
                        # Add title
                        worksheet.merge_range(f'A1:{chr(65+len(stock_df.columns))}1', f"Stock Market Search Trends - {period.capitalize()}", title_format)
                        
                        # Make the columns wider for better visibility
                        worksheet.set_column('A:A', 20)  # Date index
                        for i in range(len(stock_df.columns)):
                            worksheet.set_column(f'{chr(66+i)}:{chr(66+i)}', 15)  # Other columns
                        
                        # Format the header row
                        worksheet.write(1, 0, 'Date', header_format)
                        for col_num, value in enumerate(stock_df.columns.values):
                            worksheet.write(1, col_num+1, value, header_format)
                        
                        # Add chart if requested
                        if include_charts and len(stock_df) > 1:
                            self._add_stock_trends_chart(writer, worksheet, stock_df, sheet_name, period)
        
        except Exception as e:
            self.logger.error(f"Error creating stock trends sheets: {str(e)}")
    
    def _add_stock_trends_chart(self, writer, worksheet, stock_df, sheet_name, period):
        """
        Add chart for stock trends.
        """
        try:
            # Create a line chart
            chart = writer.book.add_chart({'type': 'line'})
            
            # Get the number of rows in the data
            num_rows = len(stock_df) + 2  # +2 for the header and title
            
            # Configure the chart
            chart.set_title({'name': f'Stock Market Search Interest - {period.capitalize()}'})
            chart.set_x_axis({'name': 'Date', 'position_axis': 'on_tick'})
            chart.set_y_axis({'name': 'Search Interest', 'major_gridlines': {'visible': True}})
            chart.set_legend({'position': 'bottom'})
            
            # Add up to 5 series to the chart to avoid clutter
            for i, term in enumerate(stock_df.columns[:5]):  # Limit to first 5 columns
                chart.add_series({
                    'name':       [sheet_name, 1, i+1],
                    'categories': [sheet_name, 2, 0, num_rows-1, 0],  # x-axis data (date)
                    'values':     [sheet_name, 2, i+1, num_rows-1, i+1],  # y-axis data (values)
                    'line':       {'width': 2.25}
                })
            
            # Insert the chart into the worksheet
            chart.set_size({'width': 720, 'height': 400})
            worksheet.insert_chart(f'A{num_rows+2}', chart)
        
        except Exception as e:
            self.logger.error(f"Error adding stock trends chart: {str(e)}")
    
    def _create_related_queries_sheets(self, writer, data, title_format, header_format):
        """
        Create sheets for related queries.
        """
        try:
            if 'related_queries' in data:
                related_queries = data['related_queries']
                
                for period in related_queries.keys():
                    # Create a sheet with all top related queries
                    sheet_name = f"Related Queries {period.capitalize()}"
                    worksheet = writer.book.add_worksheet(sheet_name)
                    
                    # Add title
                    worksheet.merge_range('A1:C1', f"Related Queries - {period.capitalize()}", title_format)
                    
                    # Set column widths
                    worksheet.set_column('A:A', 25)  # Keyword
                    worksheet.set_column('B:B', 40)  # Query
                    worksheet.set_column('C:C', 15)  # Value
                    
                    # Add headers
                    row = 3
                    worksheet.write('A2', 'Keyword', header_format)
                    worksheet.write('B2', 'Related Query', header_format)
                    worksheet.write('C2', 'Value', header_format)
                    
                    # Add data
                    for keyword, queries in related_queries[period].items():
                        # Add top queries
                        top_df = queries['top']
                        if isinstance(top_df, pd.DataFrame) and not top_df.empty:
                            for i, (_, query_row) in enumerate(top_df.iterrows()):
                                worksheet.write(f'A{row}', keyword)
                                worksheet.write(f'B{row}', query_row['query'])
                                worksheet.write(f'C{row}', query_row['value'])
                                row += 1
                    
                    # Create a sheet with all rising related queries
                    sheet_name = f"Rising Queries {period.capitalize()}"
                    worksheet = writer.book.add_worksheet(sheet_name)
                    
                    # Add title
                    worksheet.merge_range('A1:C1', f"Rising Related Queries - {period.capitalize()}", title_format)
                    
                    # Set column widths
                    worksheet.set_column('A:A', 25)  # Keyword
                    worksheet.set_column('B:B', 40)  # Query
                    worksheet.set_column('C:C', 15)  # Value
                    
                    # Add headers
                    row = 3
                    worksheet.write('A2', 'Keyword', header_format)
                    worksheet.write('B2', 'Rising Query', header_format)
                    worksheet.write('C2', 'Value', header_format)
                    
                    # Add data
                    for keyword, queries in related_queries[period].items():
                        # Add rising queries
                        rising_df = queries['rising']
                        if isinstance(rising_df, pd.DataFrame) and not rising_df.empty:
                            for i, (_, query_row) in enumerate(rising_df.iterrows()):
                                worksheet.write(f'A{row}', keyword)
                                worksheet.write(f'B{row}', query_row['query'])
                                worksheet.write(f'C{row}', query_row['value'])
                                row += 1
        
        except Exception as e:
            self.logger.error(f"Error creating related queries sheets: {str(e)}")
