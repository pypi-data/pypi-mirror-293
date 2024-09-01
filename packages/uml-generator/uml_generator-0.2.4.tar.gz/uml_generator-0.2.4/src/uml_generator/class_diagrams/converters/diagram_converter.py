# src/uml_generator/class_diagrams/converters/diagram_converter.py

from uml_generator.class_diagrams.converters.class_converter import ClassConverter
from uml_generator.class_diagrams.converters.relation_converter import RelationConverter

class DiagramConverter:
    """
    DiagramConverter is responsible for converting a UMLDiagram object 
    into a complete PlantUML string representation.
    """

    @staticmethod
    def convert_diagram(uml_diagram):
        """
        Converts a UMLDiagram instance into a complete PlantUML diagram.

        :param uml_diagram: The UMLDiagram instance to convert.
        :type uml_diagram: UMLDiagram
        :return: A string representing the entire diagram in PlantUML format.
        :rtype: str
        """
        # Start the PlantUML diagram
        uml_lines = [
            "@startuml",
            "skinparam classFontSize 16",
            "skinparam classAttributeFontSize 14",
            "skinparam classPadding 2",
            "skinparam classMargin 5",
            "skinparam linetype ortho",
            "skinparam shadowing false"
        ]

        # Get all classes from the diagram
        uml_classes = uml_diagram.get_all_classes()

        # Convert each UMLClass to its PlantUML representation
        for i, uml_class in enumerate(uml_classes):
            class_str = ClassConverter.convert_class(uml_class)
            uml_lines.append(class_str)
            
            # Add a blank line after each class except the last one
            if i < len(uml_classes) - 1:
                uml_lines.append("")

        # Add a blank line between classes and relations for readability
        if uml_diagram.get_all_classes() and uml_diagram.get_all_relations():
            uml_lines.append("")

        # Convert each UMLRelation to its PlantUML representation
        for uml_relation in uml_diagram.get_all_relations():
            relation_str = RelationConverter.convert_relation(uml_relation)
            uml_lines.append(relation_str)

        # End the PlantUML diagram
        uml_lines.append("@enduml")

        # Join all lines with newlines
        return "\n".join(uml_lines)
