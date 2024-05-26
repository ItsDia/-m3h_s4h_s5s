import json
class Service:
    def __init__(self, name, cost, input_concepts, output_concepts):
        self.name = name
        self.cost = cost
        self.input_concepts = input_concepts
        self.output_concepts = output_concepts

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_input_concept_set(self):
        return self.input_concepts

    def get_output_concept_set(self):
        return self.output_concepts
    
    def __str__(self):
        return f"Service(name={self.name}, cost={self.cost}, input_concepts={self.input_concepts}, output_concepts={self.output_concepts})"


class Concept:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Concept(name={self.name})"


class PlanningGraph:
    def __init__(self):
        self.goal_set = set()
        self.p_levels = []
        self.a_levels = []

    def add_goal(self, concept):
        self.goal_set.add(concept)

    def get_goal_set(self):
        return self.goal_set

    def add_p_level(self, concepts):
        self.p_levels.append(set(concepts))

    def get_p_level(self, level):
        return self.p_levels[level] if level < len(self.p_levels) else set()

    def add_a_level(self, services):
        self.a_levels.append(set(services))

    def get_a_level(self, level):
        return self.a_levels[level] if level < len(self.a_levels) else set()
    
    def __str__(self):
        return f"PlanningGraph(goal_set={self.goal_set}, p_levels={self.p_levels}, a_levels={self.a_levels})"


def check_all_concepts_from_initial(concepts, initial_concepts):
    return all(cpt in initial_concepts for cpt in concepts)


def forward_expand(service_map, initial_concepts, goal_concepts):
    pg = PlanningGraph()
    pg.add_p_level(initial_concepts)
    pg.goal_set.update(goal_concepts)
    
    s = set(initial_concepts)  # concept set
    goal = set(goal_concepts)
    a = service_map  # current services
    a_temp = set()
    a_prev = set()

    while not s.issuperset(goal):
        a_curr = set()

        for k in a.keys():
            if s.issuperset(a[k].get_input_concept_set()):
                a_curr.add(a[k])

        a_temp.clear()
        a_temp.update(a_curr)
        pg.add_a_level(a_curr)

        for sv in a_curr:
            s.update(sv.get_output_concept_set())

        a_temp.difference_update(a_prev)
        a_prev.clear()
        a_prev.update(a_curr)
    
    return pg


def backward_search(pg, initial_concepts, goal_concepts):
    results = {
        "service": [],
        "links": []
    }
    service_mapping = {}
    current_concepts = set(goal_concepts)
    initial = set(initial_concepts)
    
    level = len(pg.a_levels) - 1

    while level >= 0:
        tmp_level_concepts = set()
        services = set()
        for cpt in current_concepts:
            for service in pg.get_a_level(level):
                if cpt in service.get_output_concept_set():
                    services.add(service)
                    tmp_level_concepts.update(service.get_input_concept_set())

        for serv in services:
            service_name_with_level = f"{serv.get_name()}-l{level}"
            results["service"].append({"name": service_name_with_level})
            service_mapping[(serv, level)] = service_name_with_level

        current_concepts.clear()
        current_concepts.update(tmp_level_concepts)
        current_concepts.difference_update(initial)
        results["service"] = list({v['name']:v for v in results["service"]}.values())  # Remove duplicates

        level -= 1

    # Create links
    for (service1, level1), name1 in service_mapping.items():
        if (service1, level1) in service_mapping:
            if level1 + 1 in range(len(pg.a_levels)):
                for (service2, level2), name2 in service_mapping.items():
                    if level2 == level1 + 1:
                        if any(c in service2.get_input_concept_set() for c in service1.get_output_concept_set()):
                            results["links"].append({
                                "source": name1,
                                "target": name2
                            })

    print("GraphPlan")
    print(results)
    return results


def create_sample_data():
    # Create example services and concepts for a larger graph
    c1 = Concept("C1")
    c2 = Concept("C2")
    c3 = Concept("C3")
    c4 = Concept("C4")
    c5 = Concept("C5")
    c6 = Concept("C6")
    c7 = Concept("C7")
    c8 = Concept("C8")
    c9 = Concept("C9")
    c10 = Concept("C10")

    s1 = Service("S1", 10, [c3, c4], [c1])
    s2 = Service("S2", 15, [c3], [c2])
    s3 = Service("S3", 20, [c4, c5], [c6])
    s4 = Service("S4", 25, [c1, c6], [c7])
    s5 = Service("S5", 30, [c2, c6], [c8])
    s6 = Service("S6", 35, [c7, c8], [c9])
    s7 = Service("S7", 40, [c9], [c10])

    initial_concepts = [c3, c4, c5]
    goal_concepts = [c10, c9]
    service_map = {
        s1.name: s1,
        s2.name: s2,
        s3.name: s3,
        s4.name: s4,
        s5.name: s5,
        s6.name: s6,
        s7.name: s7,
    }
    
    return initial_concepts, goal_concepts, service_map


# Create the sample data
initial_concepts, goal_concepts, service_map = create_sample_data()

# Execute the forward expansion to build the planning graph
pg = forward_expand(service_map, initial_concepts, goal_concepts)

# Execute the backward search to find the plan
backward_search(pg, initial_concepts, goal_concepts)

services_data = []

for service_name, service in service_map.items():
    # 获取输入和输出概念的集合，并转换为字符串
    input_concepts_set = service.get_input_concept_set()
    output_concepts_set = service.get_output_concept_set()

    input_concepts_str = ', '.join(concept.name for concept in input_concepts_set)
    output_concepts_str = ', '.join(concept.name for concept in output_concepts_set)

    # 创建字典并添加到列表中
    service_dict = {
        "name": service_name,
        "input_concepts": input_concepts_str,
        "output_concepts": output_concepts_str
    }
    services_data.append(service_dict)

# 将字典列表转换为JSON格式的字符串
json_data = json.dumps(services_data, indent=4)

# 打印JSON格式的数据
print(json_data)

with open('services.json', 'w') as f:
    json.dump(services_data, f, indent=4)