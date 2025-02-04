import yaml

with open('/Users/princepatel/Downloads/Syntax Converter/App1 (Source, CasaOS)/docker-compose.yml','r') as file:
    data = yaml.safe_load(file)
    
print(data)