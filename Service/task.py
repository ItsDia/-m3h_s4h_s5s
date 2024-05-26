# tasks.py
import json
from .models import Service

def import_service_data(json_file_path):
    with open(json_file_path, 'r') as file:
        # 读取 JSON 文件内容
        services_data = json.load(file)

    # 遍历 JSON 数据并导入到数据库
    for service_data in services_data:
        # 使用 get_or_create 避免重复记录
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults={'input_concepts': service_data['input_concepts'], 'output_concepts': service_data['output_concepts']}
        )
        if created:
            print(f"Service '{service.name}' created.")
        else:
            print(f"Service '{service.name}' already exists.")