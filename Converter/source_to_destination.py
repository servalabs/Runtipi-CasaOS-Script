import json
import yaml
import re
import yaml
from datetime import datetime


def read_json_file(file_name):
    with open(file_name,'r') as file:
        return json.load(file)
    
def read_yaml_file(file_name):
    with open(file_name,'r') as file:
        return yaml.safe_load(file)
    
def create_config_data(json_data,ymal_data):
    LOCAL_DOMAIN = "${LOCAL_DOMAIN}"
    schema = "../schema.json"
    if(ymal_data["name"]):
        environment = ymal_data["name"]
    
    if(ymal_data["services"][environment]["image"]):
        image = ymal_data["services"][environment]["image"]
    if(ymal_data["services"][environment]["ports"]):
        ports = ymal_data["services"][environment]["ports"]
    if(yaml_data["name"]):
        name = yaml_data["name"]
    else:
        name = ""
    available = "true"
    exposable = "true"
    if yaml_data["x-casaos"]["port_map"]:
        port = yaml_data["x-casaos"]["port_map"]
    else : 
        port = ""
    if json_data["id"]:  
        id = json_data["id"]
    else:
        id = ""
    if json_data.get("version"):
        match = re.search(r'v\d+\.(\d+)\.\d+', json_data["version"])
        tipi_version = match.group(1) if match else ""
    else:
        tipi_version = ""
    if json_data["version"]:    
        version = json_data["version"]
    else:
        version = ""
    if yaml_data["x-casaos"]["category"]:    
        categories = yaml_data["x-casaos"]["category"]
    else:
        categories = ""
    if  yaml_data["x-casaos"]["description"]["en_us"]:
        description = yaml_data["x-casaos"]["description"]["en_us"]
    else:
        description = ""
    if yaml_data["x-casaos"]["tagline"]["en_us"]:
        short_desc = yaml_data["x-casaos"]["tagline"]["en_us"]
    else:
        short_desc = ""
    if yaml_data["x-casaos"]["author"]:
        author = yaml_data["x-casaos"]["author"]
    else:
        author = ""
    source = "https://github.com/anse-app/anse"
    website = "https://anse.app"
    form_fields = []
    if yaml_data["x-casaos"]["architectures"]:
        supported_architectures = yaml_data["x-casaos"]["architectures"]
    else:
        supported_architectures = ""
    created_at = int(datetime.now().timestamp() * 1000)
    updated_at = int(datetime.now().timestamp() * 1000)
    
    final_data = {
        "$schema" : schema,
        "name" : name,
        "available" : available,
        "exposable" : exposable,
        "port" : port,
        "id" : id,
        "tipi_version" : tipi_version,
        "version" : version,
        "categories" : categories,
        "description" : description,
        "short_desc" : short_desc,
        "author" : author,
        "source" : source,
        "website" : website,
        "form_fields" : form_fields,
        "supported_architectures" : supported_architectures,
        "created_at" : created_at,
        "updated_at" : updated_at
    }
    
    docker_data = {
        "version" : "3.7",
        "services" : {
            f"{id}" : {
                "image" : image,
                "restart" : "unless-stopped",
                "container_name" : id,
                "environment" : environment,
                "ports" : ports,
                "networks" : "tipi_main_network",
                "labels" : {
                    "traefik.enable" : "true",
                    f"traefik.http.middlewares.{id}-web-redirect.redirectscheme.scheme" : "https",
                    f"traefik.http.services.{id}.loadbalancer.server.port" : port,
                    f"traefik.http.routers.{id}-insecure.rule" : "Host(`${APP_DOMAIN}`)",
                    f"traefik.http.routers.{id}-insecure.entrypoints" : "web",
                    f"traefik.http.routers.{id}-insecure.service" : id,
                    f"traefik.http.routers.{id}-insecure.middlewares" : f"{id}-web-redirect",
                    f"traefik.http.routers.{id}.rule" : "Host(`${APP_DOMAIN}`)",
                    f"traefik.http.routers.{id}.entrypoints" : "websecure",
                    f"traefik.http.routers.{id}.service" : "id",
                    f"traefik.http.routers.{id}.tls.certresolver" : "myresolver",
                    f"traefik.http.routers.{id}-local-insecure.rule" : f"Host(`{id}.{LOCAL_DOMAIN}`)",
                    f"traefik.http.routers.{id}-local-insecure.entrypoints" : "web",
                    f"traefik.http.routers.{id}-local-insecure.service" : id,
                    f"traefik.http.routers.{id}-local-insecure.middlewares" : f"{id}-web-redirect",
                    f"raefik.http.routers.{id}-local.rule" : f"Host(`{id}.{LOCAL_DOMAIN}`)",
                    f"raefik.http.routers.{id}-local.entrypoints" : "websecure",
                    f"raefik.http.routers.{id}-local.service" : id,
                    f"raefik.http.routers.{id}-local.tls" : "true",
                    f"untipi.managed" : "true"
                }
            }
        }
    }

    return final_data , docker_data

def write_data_into_destination(final_data,docker_file,file_path):
    with open(file_path,"w") as file:
        json.dump(final_data,file)
        
    with open(docker_file,"w") as file:
        yaml.safe_dump(docker_data,file,default_flow_style=False)
        
    
    

json_data = read_json_file('/Users/princepatel/Downloads/Syntax Converter/App1 (Source, CasaOS)/config.json')
yaml_data = read_yaml_file('/Users/princepatel/Downloads/Syntax Converter/App1 (Source, CasaOS)/docker-compose.yml')
final_data , docker_data = create_config_data(json_data,yaml_data)
output_file_path = "/Users/princepatel/Downloads/Syntax Converter/App1 (Runtipi, Destination)/config1.json"
output_docker_file = "/Users/princepatel/Downloads/Syntax Converter/App1 (Runtipi, Destination)/docker-compose1.yml"
write_data_into_destination(final_data,output_docker_file,output_file_path)
print(f"Output JSON has been written to {output_file_path}")







