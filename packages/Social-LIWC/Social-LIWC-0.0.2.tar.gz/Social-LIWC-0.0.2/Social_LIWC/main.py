#imports necessários
from collections import Counter
import pandas as pd
import re
import liwc
# import codecs
import os
import unicodedata
import string
import re

# Remove acentos de um texto
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Remove pontuação de um texto
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

# Carrega o dicionário LIWC a partir de um arquivo
def load_dictionary(file_name):
    categories = {}
    phrases = {}

    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Ignora linhas de comentário
            if line.startswith("%") and line.endswith("%"):
                continue

            # Processa categorias e frases
            if "\t" in line:
                try:
                    code, category = line.split("\t", 1)
                    categories[code] = category
                except ValueError:
                    print(f"Erro ao processar a linha: {line}")
                    continue
            else:
                parts = line.rsplit(" ", 1)
                if len(parts) == 2:
                    phrase, codes = parts
                    normalized_phrase = remove_accents(remove_punctuation(phrase.lower()))
                    codes_list = codes.split("\t")
                    phrases[normalized_phrase] = codes_list

    return phrases, categories

# Consulta o dicionário em busca de frases específicas
def lookup_dictionary(phrases, categories, text):
    normalized_text = remove_accents(remove_punctuation(text.lower().strip()))
    words = normalized_text.split()
    found_phrases = []

    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            snippet = " ".join(words[i:j])

            # Verifica se o trecho tem mais de uma palavra antes de processar
            if len(snippet.split()) > 1 and snippet in phrases:
                codes = phrases[snippet]
                found_categories = [categories.get(code) for code in codes]
                found_phrases.append((snippet, found_categories))

    return found_phrases

def tokenize(text):
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

# Inicializa o LIWC a partir do arquivo .dic
def init_liwc_from_dic(file_path):
    liwc = {}
    category_names = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and not line.startswith('%'):  # Verifica se a linha não está em branco e não é um comentário
                parts = line.strip().split('\t')
                if len(parts) > 1:  # Verifica se a linha tem pelo menos duas partes
                    code = parts[0]
                    categories = tuple(parts[1:])  # Converte para tupla
                    liwc[code] = categories
                    category_names[code] = categories
    return liwc, category_names

# Função para contar categorias
def count_categories(results):
    category_count = Counter()
    for _, associated_categories in results:
        for category in associated_categories:
            if category:  # Verifica se a categoria não é None
                category_count[category] += 1
    return category_count

#caminho do dicionário liwc - v3
base_path = os.path.abspath(os.path.dirname(__file__)) # Caminho absoluto do diretório do script
file_path = os.path.join(base_path, 'dados', 'v3_LIWC2007_Portugues_win.dic')


# Carrega o dicionário
phrases, categories = load_dictionary(file_path)

# Inicializa o contador total de categories
total_counts = Counter()

def detect_text_column(df: pd.DataFrame):
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

# Inicializa o LIWC
parse, category_names = init_liwc_from_dic(file_path)

#categorizando frases
def phrases_categorizer(df: pd.DataFrame):
    text_column = detect_text_column(df)
    if text_column is None:
        print("Nenhuma coluna de texto foi detectada no arquivo")
    else:
        for phrase in df[text_column]:
            processed_text = phrase.split()
            print(f"Processando: {processed_text}")


            # Consulta o dicionário
            result = lookup_dictionary(phrases, categories, phrase)

            if result:
                for word, categories_associadas in result:
                    print(f"palavra/frase encontrada: '{word}'")
                    print(f"Categorias: {', '.join(filter(None, categories_associadas))}")


                    # Contagem das categories encontradas nesta linha
                    counting = count_categories(result)

                    # Atualiza o contador total
                    total_counts.update(counting)
            else:
                print("palavra ou frase não encontrada no dicionário.")

        print("\nResumo da contagem de categorias para frases e ou expressões")

        # for category, couty in total_counts.items():
        #     print(f"{category}: {couty}")
        print(total_counts)
    

#categorizando as palavras
def words_categorizer(df: pd.DataFrame):
    text_column = detect_text_column(df)
    if text_column is None:
        print("Nenhuma coluna de texto foi detectada no arquivo")
    else:
        for word in df[text_column]:
            processed_text = word.split()
            print(f"Processando: {processed_text}")

            # Normaliza o texto do usuário
            normalized_word = remove_accents(remove_punctuation(word.lower().strip()))

            # Tokeniza e conta categorias para textos de uma única palavra/frase
            text_tokens = tokenize(normalized_word)
            text_counts = Counter()

            for token in text_tokens:
                if token in parse:
                    for code in parse[token]:
                        if code in category_names:
                            category = category_names[code][0]  # Pegando o nome da categoria (primeiro item da tupla)
                            text_counts[category] += 1


            # Atualiza o contador total
            total_counts.update(text_counts)

            print(f"Contagens desta linha: {text_counts}")

            print("\nResumo da contagem de categorias para palavras:")

            for category, couty in total_counts.items():
                print(f"{category}: {couty}")
            


def analise_social_liwc(df: pd.DataFrame): 
    parse, _ = liwc.load_token_parser(file_path)
    if not isinstance(df, pd.DataFrame):
        return {"error": "O input não é um DataFrame válido"}

    # Detecta a coluna de texto
    text_column = detect_text_column(df)
    
    if text_column is None:
        return {"error": "Nenhuma coluna de texto foi detectada no CSV"}

    
    file_counts = Counter()

    
    for text in df[text_column]:
        text_tokens = tokenize(str(text))  
        
        text_counts = Counter(category for token in text_tokens for category in parse(token))
        
        file_counts.update(text_counts)
    
    return dict(file_counts)

