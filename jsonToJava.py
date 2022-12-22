#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Thayse Marques Solis"

import json
import sys

# Dicionário de classes que foram analisadas a partir do JSON
# A chave é o nome da classe e o valor é uma tupla com dois elementos: a lista de campos e um dicionário que relaciona o campo com seu tipo
analyzed_classes = {} 

# Flag que indica se algum dos campos de alguma classe é um ArrayList
uses_array_list = False

def get_class_atributes(class_name, objects):
    """
    Recebe um nome de classe e uma lista de objetos e gera uma tupla com uma lista de campos e um dicionário com os tipos dos campos
    """
    field_names = [] # nomes dos campos
    field_types = {} # tipos dos campos

    # Verifica se a classe já foi analisada (se já está em analyzed_classes)
    # Se sim, inicializa field_names e field_types com o que já foi analisado
    if class_name in analyzed_classes:
        (field_names, field_types) = analyzed_classes[class_name]

    # Para cada objeto
    for object in objects:
        # Para cada campo do objeto
        for field_name in object:
            # Lê o valor do campo do objeto
            field_value = object[field_name] 
            field_type = "?"
            # Se o valor do campo for uma String, define o tipo do campo como String
            if isinstance(field_value, str):
                field_type = "String"
            # Se o valor do campo for um float, define o tipo do campo como double    
            if isinstance(field_value, float):
                field_type = "double"
            # Se o valor do campo for um bool, define o tipo do campo como boolean
            if isinstance(field_value, bool):
                field_type = "boolean"
            # Se o valor do campo for uma lista, o campo será analisado de acordo com o tipo do primeiro elemento
            if isinstance(field_value, list):
                # Define a flag global uses_array_list como true
                global uses_array_list
                uses_array_list = True
                if isinstance(field_value[0], dict):
                    # Como o primeiro elemento da lista é um dicionário, trata-se de um objeto. Portanto, é preciso analisar para determinar seus campos
                    analyze_class(field_name, field_value)
                    # Quando uma classe possui um campo que contém objetos de outra classe, o tipo será ArrayList 
                    # e seu nome é transformado em letras minúsculas 
                        # o nome deveria ser pluralizado, mas como nem sempre o plural é regular, optou-se por manter o substantivo no singular
                    field_type = "ArrayList<" + field_name + ">"
                    field_name=field_name.lower()
                if isinstance(field_value[0], str):
                    field_type = "ArrayList<String>"
                if isinstance(field_value[0], float):
                    field_type = "ArrayList<Double>"
                if isinstance(field_value[0], bool):
                    field_type = "ArrayList<Boolean>"
            # Se o valor do campo for um dicionário, o campo será analisado como uma classe
            if isinstance(field_value, dict):
                analyze_class(field_name, [ field_value ])
                field_type = field_name
                field_name=field_name.lower()
                
            # Se o campo ainda não estiver na lista de campos da classe, ele é adicionado, assim como seu tipo
            if field_name not in field_names:
                field_names.append(field_name)
                field_types[field_name] = field_type
    # Retorna os nomes e tipos dos campos
    return (field_names, field_types)

def generate_java_class(class_name, field_names, field_types):
    """
    Recebe um nome de classe, lista de campos e dicionário de tipos e gera uma string com o código Java correspondente à classe
    """
    code = ""
    # Acrescenta "class", o nome da classe e "{"
    code += "class " + class_name + " {\n"
    # Itera pelos campos da classe
    for field_name in field_names:
        # Acrescenta uma marca de tabulação, o tipo do campo e o nome do campo
        code += "\t" + field_types[field_name] + " " + field_name + ";\n"
    # Acrescenta "}" 
    code += "}\n"
    return code

def analyze_class(class_name, objects):
    """
    Recebe um nome de classe e uma lista de objetos, analisa os objetos para determinar os campos e salva em analyzed_classes
    """
    # Determina os campos da classe e seus tipos 
    (field_names, field_types) = get_class_atributes(class_name, objects)
    # Salva os campos e tipos em analyzed_classes
    analyzed_classes[class_name]=(field_names, field_types)
        
def main():
    # Verifica a quantidade de argumentos
    if len(sys.argv)!=2:
        print("Uso: python3 jsonToJava.py <arquivo de entrada.json>")
        sys.exit(1)  # status 1 = erro

    # O arquivo de entrada é o segundo argumento
    input_file = sys.argv[1]

    # Abre o arquivo JSON
    with open(input_file, encoding='utf-8') as f:
        # Decodifica o JSON como um dicionário do Python. 
        # Os objetos JSON são tratados como dicionários no Python e os arrays do JSON são tratados como listas no Python.
        file_data = json.load(f)

    # Itera pelo JSON decodificado e analisa todas as classe
    for class_name in file_data:
        analyze_class(class_name, file_data[class_name])

    # Variável que armazena o código gerado    
    code = ""

    # Se necessário, adiciona a importação da classe ArrayList 
    if uses_array_list:
        code += "import java.util.ArrayList;\n"

    # Para cada classe analisada, adiciona o código java correspondente    
    for class_name in analyzed_classes:
        (field_names, field_types) = analyzed_classes[class_name]
        code += generate_java_class(class_name, field_names, field_types)
    
    # Adiciona a classe com o método main
    code +="""public class Program {
	public static void main (String args[]){
	}
}"""
    #print(code)

    # Salva o código gerado no arquivo Program.java
    with open("Program.java", 'w', encoding='utf-8') as file:
        file.write(code)

# Se este arquivo for invocado diretamente pela linha de comando, executa a função main
if __name__ == "__main__":
    main()