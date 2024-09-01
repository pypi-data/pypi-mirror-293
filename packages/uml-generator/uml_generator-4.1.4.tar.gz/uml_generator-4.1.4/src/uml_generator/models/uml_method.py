# src/uml_generator/models/uml_method.py

class UMLMethod:
    """
    Represents a method of a UML class.

    Attributes:
        visibility (str): The visibility of the method, which can be 
                          'public', 'private', 'protected', or 'default' (package-private).
        is_static (bool): Indicates if the method is static, meaning it belongs to 
                          the class rather than any instance of the class.
        is_final (bool): Indicates if the method is final, meaning it cannot be overridden 
                         in a subclass.
        return_type (str): The return type of the method (e.g., 'int', 'void').
        name (str): The name of the method (e.g., 'getOrderId').
        parameters (list): A list of UMLParameter instances representing the parameters 
                           of the method.
    """

    def __init__(self, visibility, is_static=False, is_final=False, return_type=None, name=None, parameters=None):
        """
        Initializes a UMLMethod instance.

        :param visibility: The visibility modifier of the method.
        :type visibility: str
        :param is_static: Whether the method is static. Defaults to False.
        :type is_static: bool, optional
        :param is_final: Whether the method is final. Defaults to False.
        :type is_final: bool, optional
        :param return_type: The return type of the method.
        :type return_type: str, optional
        :param name: The name of the method.
        :type name: str, optional
        :param parameters: A list of UMLParameter instances representing the method parameters.
        :type parameters: list of UMLParameter, optional
        """
        self.visibility = visibility
        self.is_static = is_static
        self.is_final = is_final
        self.return_type = return_type
        self.name = name
        self.parameters = parameters if parameters is not None else []

    def __str__(self):
        """
        Returns a string representation of the UMLMethod, 
        which is useful for debugging and logging purposes.

        :return: A string that represents the method in a human-readable form, 
                including its visibility, whether it is static or final, return type, 
                name, and parameters.
        :rtype: str
        """
        parts = [self.visibility]

        if self.is_static:
            parts.append('static')
        if self.is_final:
            parts.append('final')

        if self.return_type:
            parts.append(self.return_type)

        if self.name:
            parts.append(f"{self.name}(")
        else:
            parts.append("(")

        params_str = ', '.join([str(param) for param in self.parameters])
        parts[-1] += params_str + ")"

        return ' '.join(parts).replace(" (", "(")

    def to_dict(self):
        """
        Converts the UMLMethod instance into a dictionary format, 
        which can be useful for serialization or conversion to other formats.

        :return: A dictionary containing the method's details.
        :rtype: dict
        """
        return {
            'visibility': self.visibility,
            'is_static': self.is_static,
            'is_final': self.is_final,
            'return_type': self.return_type,
            'name': self.name,
            'parameters': [param.to_dict() for param in self.parameters]
        }
