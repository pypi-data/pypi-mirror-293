from collections import Counter
import pandas as pd
import re
import liwc
import codecs
import os

base_path = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto do diretório do script
input_file = os.path.join(base_path, 'dados', 'v2_LIWC2007_Portugues_win.dic')
output_file = os.path.join(base_path, 'dados', 'v2_LIWC2007_Portugues_win_utf8.dic')

with codecs.open(input_file, 'r', encoding='latin-1') as infile, \
     codecs.open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        outfile.write(line)

# Dicionário LIWC UTF8
parse, category_names = liwc.load_token_parser(output_file)


last_file_counts = {}


def tokenize(text):
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)


def detect_text_column(df):
    # Coluna com o maior número de strings longas é escolhida
    text_column = None
    max_avg_length = 0
    for col in df.columns:
        if df[col].dtype == 'object':  # Verifica se a coluna é do tipo texto
            avg_length = df[col].apply(lambda x: len(str(x))).mean()
            if avg_length > max_avg_length:
                max_avg_length = avg_length
                text_column = col
    return text_column


def analise_liwc(path):
    global last_file_counts  

    if not path.endswith('.csv'):
        return {"error": "O arquivo enviado não é um CSV"}
    
    df = pd.read_csv(path)

    # Detecta a coluna de texto
    text_column = detect_text_column(df)
    
    if text_column is None:
        return {"error": "Nenhuma coluna de texto foi detectada no CSV"}

    
    file_counts = Counter()

    
    for text in df[text_column]:
        text_tokens = tokenize(str(text))  
        
        text_counts = Counter(category for token in text_tokens for category in parse(token))
        
        file_counts.update(text_counts)

    # Atualiza o último arquivo processado
    last_file_counts = dict(file_counts)

    
    return last_file_counts

# Retorna as categorias do último arquivo analisado
# def get_liwc_categories():
#     global last_file_counts  

#     if not last_file_counts:
#         return {"error": "Nenhuma análise de arquivo foi feita ainda."}

    
#     return last_file_counts
