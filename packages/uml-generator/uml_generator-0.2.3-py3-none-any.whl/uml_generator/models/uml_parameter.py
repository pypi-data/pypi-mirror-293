# src/uml_generator/models/uml_parameter.py

class UMLParameter:
    """
    Represents a parameter of a method in a UML class.

    Attributes:
        name (str): The name of the parameter (e.g., 'orderId').
        type (str): The data type of the parameter (e.g., 'int', 'String').
    """

    def __init__(self, name, type):
        """
        Initializes a UMLParameter instance.

        :param name: The name of the parameter.
        :type name: str
        :param type: The data type of the parameter.
        :type type: str
        """
        self.name = name
        self.type = type

    def __str__(self):
        """
        Returns a string representation of the UMLParameter, 
        which is useful for debugging and logging purposes.

        :return: A string that represents the parameter in a human-readable form, 
                 including its name and type.
        :rtype: str
        """
        return f"{self.type} {self.name}"

    def to_dict(self):
        """
        Converts the UMLParameter instance into a dictionary format, 
        which can be useful for serialization or conversion to other formats.

        :return: A dictionary containing the parameter's details.
        :rtype: dict
        """
        return {
            'name': self.name,
            'type': self.type
        }
