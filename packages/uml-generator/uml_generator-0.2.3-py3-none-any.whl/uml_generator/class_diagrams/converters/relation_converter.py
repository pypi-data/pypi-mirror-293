# src/uml_generator/class_diagrams/converters/relation_converter.py

class RelationConverter:
    """
    RelationConverter is responsible for converting UMLRelation objects 
    into their PlantUML string representation.
    """

    @staticmethod
    def convert_relation(uml_relation):
        """
        Generates the PlantUML representation for a given UMLRelation object.

        :param uml_relation: The UMLRelation instance to convert.
        :type uml_relation: UMLRelation
        :return: A string representing the relation in PlantUML format.
        :rtype: str
        """
        # Determine the PlantUML symbol based on the relation type
        relation_symbol = RelationConverter.get_relation_symbol(uml_relation.relation_type)

        # Start building the PlantUML relation string with the source element
        relation_str = f"{uml_relation.source}"

        # Include the multiplicity in the relation string if it exists
        if uml_relation.multiplicity:
            relation_str += f" \"{uml_relation.multiplicity}\""

        # Add the relation symbol and the target element to the string
        relation_str += f" {relation_symbol} {uml_relation.target}"
    
        # Append the relation name to the string if it exists
        if uml_relation.name:
            relation_str += f" : {uml_relation.name}"

        return relation_str

    @staticmethod
    def get_relation_symbol(relation_type):
        """
        Maps a relation type to its corresponding PlantUML symbol.

        :param relation_type: The type of the UML relation ('extends', 'implements', 'association').
        :type relation_type: str
        :return: The corresponding PlantUML symbol for the relation.
        :rtype: str
        """
        if relation_type == 'extends':
            return '--|>'
        elif relation_type == 'implements':
            return '..|>'
        elif relation_type == 'association':
            return '-->'
        else:
            return '--' # Default to association if unknown type
