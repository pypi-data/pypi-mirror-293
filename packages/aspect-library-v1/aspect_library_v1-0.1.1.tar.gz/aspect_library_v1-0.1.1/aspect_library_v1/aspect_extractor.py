from pyabsa import ATEPCCheckpointManager
import pandas as pd
from .translator import translate_column

class AspectExtractor:
    def __init__(self, checkpoint='english', auto_device=False):
        self.aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
            checkpoint=checkpoint, 
            auto_device=auto_device
        )
    
    def extract(self, df, column_name='Customer Comments', target_language='en', source_language='auto'):
        # Translate the specified column
        translated_df = translate_column(df, column_name, target_language, source_language)
        
        # Perform aspect extraction on the translated text
        examples = list(translated_df['comments'])
        atepc_result = self.aspect_extractor.extract_aspect(
            inference_source=examples,
            pred_sentiment=True
        )
        
        # Concatenate the results with the original DataFrame
        result_df = pd.concat([translated_df, pd.DataFrame(atepc_result)], axis=1)
        return result_df
