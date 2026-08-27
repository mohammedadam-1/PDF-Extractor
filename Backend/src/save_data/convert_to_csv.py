import pandas as pd 
from src.extractor.extract_text import extract_text
from pathlib import Path
import io


class ConvertToCSV:
    def __init__(self):
        self.csv_file = None
        self.dataframe = None
        self.filename = None
        
    def create_csv(self, rows_list, filename):
        """Create a CSV file"""
        try:
            
            df = pd.DataFrame(rows_list)
            file_path = Path(filename)
            prefix = file_path.stem
            filename = prefix + ".csv"
            
            return df
        except Exception as e:
            print(e)
            
    def save_as_csv(self, rows_list, filename):
            """Save to CSV file format"""
            try:
                self.filename = filename
                self.dataframe = self.create_csv(rows_list=rows_list, filename=self.filename)
            except Exception as e:
                print(e)
        
       
    def convert_df_to_bytes(self):
        with io.BytesIO() as buffer:
            self.dataframe.to_csv(buffer, header=False, index=False, encoding='utf-8')
            return buffer.getvalue()
        
           
       
convert_to_csv = ConvertToCSV()            