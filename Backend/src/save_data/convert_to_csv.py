import pandas as pd 
from src.extractor.extract_text import extract_text
from pathlib import Path
class ConvertToCSV:
    def __init__(self):
        self.csv_file = None
        
    def create_csv(self, rows_list, filename) -> None:
        """Create a CSV file"""
        try:
            for row in rows_list:
                df = pd.DataFrame(rows_list)
                file_path = Path(filename)
                prefix = file_path.stem
                filename = prefix + ".csv"
                df.to_csv(filename, index=False, header=False)
        except Exception as e:
            print(e)
            
    def save_as_csv(self, rows_list, filename):
            """Save to CSV file format"""
            try:
                
                self.create_csv(rows_list=rows_list, filename=filename)
            except Exception as e:
                print(e)
        
       
       
convert_to_csv = ConvertToCSV()            