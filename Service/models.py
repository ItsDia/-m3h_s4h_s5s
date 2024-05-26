class Service:
    def __init__(self, name, cost, input_concepts, output_concepts, x=300, y=0):
        self.name = name
        self.cost = cost
        self.input_concepts = input_concepts
        self.output_concepts = output_concepts
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_input_concept_set(self):
        return self.input_concepts

    def get_output_concept_set(self):
        return self.output_concepts

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return f"Service(name={self.name}, cost={self.cost}, input_concepts={self.input_concepts}, output_concepts={self.output_concepts}, x={self.x}, y={self.y})"