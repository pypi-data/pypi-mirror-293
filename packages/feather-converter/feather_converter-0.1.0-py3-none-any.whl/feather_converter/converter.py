import pandas as pd
import os

def convert_feather(filePath: str|None, outputPath: str|None):
    if(isinstance(filePath, str)):
        df = pd.read_feather(filePath)
        if(outputPath is None):
            base_name = os.path.basename(filePath).replace('.feather', '.csv')
            outputPath = os.path.join(os.getcwd(), base_name)
            df.to_csv(outputPath)
        else:
            df.to_csv(outputPath)
    else: 
        print("No file Provided")
