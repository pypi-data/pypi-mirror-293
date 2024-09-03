import os
import pandas as pd
import numpy as np
from smartsheet_engine.engine import SmartsheetEngine

def main():
    raise NotImplementedError('Command-line interface coming soon!')

    #smartsheet_api_key = os.getenv('SMARTSHEET_API_KEY')
    #S = SmartsheetEngine(api_key=smartsheet_api_key)
    #test_grid = S.get_sheet('test_grid')
    #print(f'before\n-----')
    #print(test_grid.sheet_df)

    #append_df = pd.DataFrame({
    #    'number':       [4,5],
    #    'rating':       [None, None],
    #    'missing_col':  ['data', 'ignored'],
    #})
    #S.append_sheet_rows('test_grid', append_df)
    #test_grid = S.get_sheet('test_grid')
    #print(f'after\n------\n')
    #print(test_grid.sheet_df)

    #S.update_column_picklist('test_grid', 'rating', ['Lowest', 'Low', 'Medium', 'High', 'Highest'])
    #update_df = test_grid.sheet_df
    #conditions = [
    #    update_df['number'] == 1,
    #    update_df['number'] == 2,
    #    update_df['number'] == 3,
    #    update_df['number'] == 4,
    #    update_df['number'] == 5,
    #]
    #choices = [
    #    'Lowest',
    #    'Low',
    #    'Medium',
    #    'High',
    #    'Highest',
    #]
    #update_df['rating'] = np.select(conditions, choices)
    #S.update_sheet_rows('test_grid', update_df)
    #test_grid = S.get_sheet('test_grid')
    #print(f'after\n------\n')
    #print(test_grid.sheet_df)

    #df = S.get_sheet('test_grid').sheet_df
    #df = df[df['number'].isin([2,3])]
    #S.delete_sheet_rows('test_grid', df)
    #test_grid = S.get_sheet('test_grid')
    #print(f'after\n-----')
    #print(test_grid.sheet_df)