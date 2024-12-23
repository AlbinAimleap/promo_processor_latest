from argparse import ArgumentParser
from promo_processor import PromoProcessor
from pathlib import Path
import pandas as pd
from datetime import datetime
from marianos import Marianos
from jewelosco import Jewelosco
from target import Target


class Processor:
    def __init__(self):
        self.args = self.parser()
        self.df = self.format_data(self.load_file())
    
    def parser(self):
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", help="File path")
        parser.add_argument("-o", "--output", help="Output directory", default="output")
        parser.add_argument("-s", "--site", help="Site Name", choices=['jewel', 'marianos', 'target'], required=True)        
        return parser.parse_args()
    
    def load_file(self):
        file = Path(self.args.file)
        if not file.exists():
            raise FileNotFoundError(f"File {file} not found")
        if file.suffix == ".json":
            return pd.read_json(file)
        elif file.suffix == ".csv":
            return pd.read_csv(file)
        elif file.suffix in (".xls", ".xlsx"):
            return pd.read_excel(file)
        raise ValueError("Invalid file format")
    
    def load_site(self):
        if self.args.site == "jewel":
            return Jewelosco(PromoProcessor, self.df)
        elif self.args.site == "marianos":
            return Marianos(PromoProcessor, self.df)
        elif self.args.site == "target":
            return Target(PromoProcessor, self.df)
        raise ValueError("Invalid site")
    
    def format_data(self, data):
        data['upc'] = data['upc'].astype(str).str.zfill(13)
        data.fillna(value="", inplace=True)
        return data.to_dict(orient='records')
    
    def process(self):
        output_dir = Path(self.args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        processed_data = self.load_site()
        processed_data.processor.to_json(Path(output_dir) / f"{processed_data.__class__.__name__}_{datetime.now().date()}.json")

def main():
    processor = Processor()
    processor.process()


if __name__ == "__main__":
    main()
    