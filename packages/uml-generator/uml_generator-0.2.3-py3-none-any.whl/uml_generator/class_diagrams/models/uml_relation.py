# src/uml_generator/class_diagrams/models/uml_relation.py

from uml_generator.class_diagrams.types.relations import EXTENDS, IMPLEMENTS, ASSOCIATION

class UMLRelation:
    """
    Represents a relationship between two UML classes.

    A UMLRelation can represent different types of relationships, including inheritance ('extends'),
    implementation ('implements'), and associations. Each relation contains information about the
    source class, target class, type of relation, multiplicity, and an optional name.
    """

    def __init__(self, source, target, relation_type, multiplicity=None, name=None):
        """
        Initializes a UMLRelation instance.

        :param source: The name of the source class in the relationship.
        :type source: str
        :param target: The name of the target class in the relationship.
        :type target: str
        :param relation_type: The type of the relationship ('extends', 'implements', 'association').
        :type relation_type: str
        :param multiplicity: The multiplicity of the relationship (e.g., '1', '1..*'). Optional for some relations.
        :type multiplicity: str, optional
        :param name: An optional name or label for the relationship.
        :type name: str, optional
        """
        self.source = source
        self.target = target
        self.relation_type = relation_type
        self.multiplicity = multiplicity
        self.name = name

    def __repr__(self):
        """
        Returns a string representation of the UMLRelation instance.

        The representation includes the source and target classes, the type of relationship,
        and optionally the multiplicity and name if they are provided.

        :return: A formatted string describing the UML relationship.
        :rtype: str
        """
        parts = [f"{self.source}"]

        relation_symbols = {
            EXTENDS: '--|>',
            IMPLEMENTS: '..|>',
            ASSOCIATION: '--'
        }
        symbol = relation_symbols.get(self.relation_type, '--')
        parts.append(f"{symbol}")

        parts.append(f"{self.target}")

        if self.multiplicity:
            parts.append(f"[{self.multiplicity}]")

        if self.name:
            parts.append(f'"{self.name}"')

        return ' '.join(parts)
