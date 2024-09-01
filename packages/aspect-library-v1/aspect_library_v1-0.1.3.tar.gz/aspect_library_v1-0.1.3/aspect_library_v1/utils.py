import pandas as pd

def concatenate_results(df_original, extracted_aspects):
    result_df = pd.concat([df_original, pd.DataFrame(extracted_aspects)], axis=1)
    return result_df[['Customer Comments', 'aspects', 'sentiment', 'confidence', 'position']]
