# src/uml_generator/class_diagrams/models/uml_class.py

class UMLClass:
    """
    Represents a UML class, which can include attributes, methods, superclasses and interfaces.

    Attributes:
        visibility (str): The visibility of the class, which can be 
                          'public', 'private', 'protected', or 'default' (package-private).
        is_abstract (bool): Indicates if the class is abstract, meaning it cannot be 
                            instantiated and may contain abstract methods.
        is_interface (bool): Indicates if the class is an interface, meaning it only
                             declares methods that must be implemented by any class that 
                             implements the interface.
        name (str): The name of the UML class (e.g., 'Order').
        superclasses (list): A list of strings representing the classes that 
                             this class inherits from.
        interfaces (list): A list of strings representing the interfaces that 
                             this class implements.
        attributes (list): A list of UMLAttribute instances representing the attributes 
                           (fields) of the class.
        methods (list): A list of UMLMethod instances representing the methods of the class.
    """

    def __init__(self, visibility, is_abstract=False, is_interface=False, name=None, superclasses=None, interfaces=None):
        """
        Initializes a UMLClass instance.

        :param visibility: The visibility of the class.
        :type visibility: str
        :param is_abstract: Whether the class is abstract. Defaults to False.
        :type is_abstract: bool, optional
        :param is_interface: Whether the class is an interface. Defaults to False.
        :type is_interface: bool, optional
        :param name: The name of the UML class.
        :type name: str
        :param superclasses: A list of classes this class inherits from.
        :type superclasses: list of str, optional
        :param interfaces: A list of interfaces this class implements.
        :type interfaces: list of str, optional
        """
        self.visibility = visibility
        self.is_abstract = is_abstract
        self.is_interface = is_interface
        self.name = name
        self.superclasses = superclasses if superclasses is not None else []
        self.interfaces = interfaces if interfaces is not None else []
        self.attributes = []
        self.methods = []

    def add_attribute(self, attribute):
        """
        Adds an attribute to the UML class.

        :param attribute: An instance of UMLAttribute representing an attribute of the class.
        :type attribute: UMLAttribute
        """
        self.attributes.append(attribute)

    def add_method(self, method):
        """
        Adds a method to the UML class.

        :param method: An instance of UMLMethod representing a method of the class.
        :type method: UMLMethod
        """
        self.methods.append(method)

    def __str__(self):
        """
        Returns a string representation of the UMLClass, 
        which is useful for debugging and logging purposes.

        :return: A string that represents the class in a human-readable form, 
                including its name, visibility, and its attributes and methods.
        :rtype: str
        """
        class_type = "interface" if self.is_interface else "class"
        abstract_modifier = "abstract " if self.is_abstract else ""

        visibility_and_modifiers = f"{self.visibility} {abstract_modifier}{class_type} {self.name}".strip()

        parts = [visibility_and_modifiers]

        if self.superclasses:
            parts.append(f"extends {', '.join(self.superclasses)}")
        
        if self.interfaces:
            parts.append(f"implements {', '.join(self.interfaces)}")

        header = " ".join(parts).strip()
        parts = [header + " {"]

        for attribute in self.attributes:
            parts.append(f"    {attribute}")

        if self.attributes and self.methods:
            parts.append("")

        for method in self.methods:
            parts.append(f"    {method}")

        parts.append("}")
        
        return "\n".join(parts)

    def to_dict(self):
        """
        Converts the UMLClass instance into a dictionary format, 
        which can be useful for serialization or conversion to other formats.

        :return: A dictionary containing the class's details.
        :rtype: dict
        """
        return {
            'visibility': self.visibility,
            'is_abstract': self.is_abstract,
            'is_interface': self.is_interface,
            'name': self.name,
            'superclasses': self.superclasses,
            'interfaces': self.interfaces,
            'attributes': [attr.to_dict() for attr in self.attributes],
            'methods': [method.to_dict() for method in self.methods]
        }
