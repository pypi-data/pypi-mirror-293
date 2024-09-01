# src/uml_generator/class_diagrams/models/uml_attribute.py

class UMLAttribute:
    """
    Represents an attribute (or field) of a UML class.

    Attributes:
        visibility (str): The visibility of the attribute, which can be 
                          'public', 'private', 'protected', or 'default' (package-private).
        is_static (bool): Indicates if the attribute is static, meaning it belongs to 
                          the class rather than any instance of the class.
        is_final (bool): Indicates if the attribute is final, meaning it cannot be reassigned 
                         after initialization.
        type (str): The data type of the attribute (e.g., 'int', 'String').
        name (str): The name of the attribute (e.g., 'orderId').
    """

    def __init__(self, visibility, is_static=False, is_final=False, type=None, name=None):
        """
        Initializes a UMLAttribute instance.

        :param visibility: The visibility modifier of the attribute.
        :type visibility: str
        :param is_static: Whether the attribute is static. Defaults to False.
        :type is_static: bool, optional
        :param is_final: Whether the attribute is final. Defaults to False.
        :type is_final: bool, optional
        :param type: The data type of the attribute.
        :type type: str, optional
        :param name: The name of the attribute.
        :type name: str, optional
        """
        self.visibility = visibility
        self.is_static = is_static
        self.is_final = is_final
        self.type = type
        self.name = name

    def __str__(self):
        """
        Returns a string representation of the UMLAttribute, 
        which is useful for debugging and logging purposes.

        :return: A string that represents the attribute in a human-readable form, 
                including its visibility, whether it is static or final, type, and name.
        :rtype: str
        """
        parts = [self.visibility]

        if self.is_static:
            parts.append('static')
        if self.is_final:
            parts.append('final')

        if self.type:
            parts.append(self.type)
        if self.name:
            parts.append(self.name)

        return ' '.join(parts)

    def to_dict(self):
        """
        Converts the UMLAttribute instance into a dictionary format, 
        which can be useful for serialization or conversion to other formats.

        :return: A dictionary containing the attribute's details.
        :rtype: dict
        """
        return {
            'visibility': self.visibility,
            'is_static': self.is_static,
            'is_final': self.is_final,
            'type': self.type,
            'name': self.name
        }
