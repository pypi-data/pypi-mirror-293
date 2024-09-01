# src/uml_generator/models/uml_diagram.py

class UMLDiagram:
    """
    Represents a UML diagram consisting of classes and their relationships.

    This class provides methods to add classes and relations to the diagram,
    retrieve all classes and relations, and convert the diagram to a dictionary 
    or string format for easy visualization or further processing.
    """

    def __init__(self):
        """
        Initializes an empty UMLDiagram instance.
        
        It initializes empty lists to store UML classes and relations.
        """
        self.classes = []
        self.relations = []

    def add_class(self, uml_class):
        """
        Adds a UMLClass instance to the diagram.

        :param uml_class: The UMLClass instance to add.
        :type uml_class: UMLClass
        """
        self.classes.append(uml_class)

    def add_relation(self, relation):
        """
        Adds a UMLRelation instance to the diagram.

        :param relation: The UMLRelation instance to add.
        :type relation: UMLRelation
        """
        self.relations.append(relation)

    def get_all_classes(self):
        """
        Retrieves all UMLClass instances in the diagram.

        :return: A list of all UMLClass instances.
        :rtype: list[UMLClass]
        """
        return self.classes

    def get_all_relations(self):
        """
        Retrieves all UMLRelation instances in the diagram.

        :return: A list of all UMLRelation instances.
        :rtype: list[UMLRelation]
        """
        return self.relations

    def to_dict(self):
        """
        Converts the UML diagram into a dictionary format.

        This dictionary contains lists of classes and relations, 
        where each class and relation is represented as a dictionary.

        :return: A dictionary representation of the UML diagram.
        :rtype: dict
        """
        return {
            'classes': [uml_class.to_dict() for uml_class in self.classes],
            'relations': [relation.__dict__ for relation in self.relations]
        }

    def __str__(self):
        """
        Returns a string representation of the UML diagram.

        The string includes all classes and their attributes, 
        as well as all relations between classes.

        :return: A formatted string representing the UML diagram.
        :rtype: str
        """
        class_strs = [str(uml_class) for uml_class in self.classes]
        relation_strs = [str(relation) for relation in self.relations]
        
        return "\n".join(class_strs + relation_strs)
