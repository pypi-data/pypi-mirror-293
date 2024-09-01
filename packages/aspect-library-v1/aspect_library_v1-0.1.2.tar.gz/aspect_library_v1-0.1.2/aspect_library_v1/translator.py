import os
from unlimited_machine_translator.translator import machine_translator_df
from deep_translator import GoogleTranslator
import pandas as pd

def translate_column(df, column_name, target_language='en', source_language='auto'):
    translated_data = machine_translator_df(
        data_set=df,
        column_name=column_name,
        target_language=target_language,
        source_language=source_language,
        Translator=GoogleTranslator,
        current_wd=os.getcwd()
    )
    translated_column_name = f'{column_name}_{target_language}'
    translated_data = translated_data.rename(columns={translated_column_name: 'comments'})
    return translated_data
