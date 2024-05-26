import random

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Service.form import ServiceNameForm
from Service.integrated_forward_backward_search_with_updated_backward_search import create_sample_data,forward_expand,backward_search
from Service.models import Service


def create_random_service(request):
    if request.method == 'POST':
        form = ServiceNameForm(request.POST)
        if form.is_valid():
            service_name = form.cleaned_data['service_name']

            # 随机生成成本
            cost = random.randint(1, 1000)  # 假设成本在1到1000之间

            # 创建服务实例
            initial_concepts, goal_concepts, service_map = create_sample_data()

            # 构建规划图
            pg = forward_expand(service_map, initial_concepts, goal_concepts)

            # 执行后向搜索
            backward_search(pg, initial_concepts, goal_concepts)

            # 从规划图中随机选择一个服务
            random_service = random.choice(list(service_map.values()))

            # 将概念集合转换为字符串
            input_concepts_str = ','.join([concept.name for concept in random_service.get_input_concept_set()])
            output_concepts_str = ','.join([concept.name for concept in random_service.get_output_concept_set()])
            # 创建服务实例
            service = Service.objects.create(
                name=service_name,
                cost=cost,
                input_concepts=input_concepts_str,
                output_concepts=output_concepts_str
            )

            # 可以在这里添加逻辑来填充 input_concepts 和 output_concepts

            return HttpResponse('恭喜生成成功')
    else:
        form = ServiceNameForm()

    return render(request, 'add_services.html', {'form': form})

def search(request):
    keywords = request.GET.get('keywords')
    if keywords:
        services = Service.objects.filter(name__icontains=keywords)
    else:
        return HttpResponse('没有')
    paginator = Paginator(services,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'templates/search_service.html', {'page_obj':page_obj})