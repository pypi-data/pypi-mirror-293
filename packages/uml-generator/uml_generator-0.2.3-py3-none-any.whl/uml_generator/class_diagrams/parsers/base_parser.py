# src/uml_generator/class_diagrams/parsers/base_parser.py

from abc import ABC, abstractmethod

class BaseParser(ABC):
    """
    An abstract base class for parsers that extract UML class representations from source code.
    """

    def __init__(self, filepath):
        """
        Initializes the BaseParser with the path to the source file to be parsed.

        :param filepath: The path to the source file.
        :type filepath: str
        """
        self.filepath = filepath

    @abstractmethod
    def parse(self):
        """
        Parses the source file and returns a UMLDiagram containing all the UML classes 
        extracted from the file.

        :return: A UMLDiagram containing the parsed UML classes.
        :rtype: UMLDiagram
        """
        pass

    @abstractmethod
    def parse_header(self, java_code):
        """
        Parses the header of a Java class or interface and initializes a UMLClass instance.

        This method extracts the class name, visibility, whether the class is abstract or an 
        interface, as well as any superclasses or interfaces it extends or implements.

        :param java_code: The Java code containing the class or interface header.
        :type java_code: str
        :return: A UMLClass instance representing the parsed class or interface.
        :rtype: UMLClass
        """
        pass

    @abstractmethod
    def parse_attributes(self, java_code, uml_class):
        """
        Parses the attributes of a Java class and adds them to a UMLClass instance.

        This method identifies all the fields (attributes) in a class, including their visibility,
        type, name, and whether they are static or final. These attributes are then added to the 
        given UMLClass instance.

        :param java_code: The Java code containing the class attributes.
        :type java_code: str
        :param uml_class: The UMLClass instance to which the parsed attributes will be added.
        :type uml_class: UMLClass
        """
        pass

    @abstractmethod
    def parse_methods(self, java_code, uml_class):
        """
        Parses the methods of a Java class and adds them to a UMLClass instance.

        This method identifies all the methods in a class, including their visibility, return type,
        name, and parameters. It also detects whether the methods are static or final. These methods 
        are then added to the given UMLClass instance.

        :param java_code: The Java code containing the class methods.
        :type java_code: str
        :param uml_class: The UMLClass instance to which the parsed methods will be added.
        :type uml_class: UMLClass
        """
        pass        

    @abstractmethod
    def create_relations(self, uml_diagram):
        """
        Creates UML relationships (associations, inheritance, implementation) between classes based on their attributes.

        This method iterates through all classes in the UML diagram and examines their attributes to determine
        if they reference other classes within the diagram. Depending on the context and naming conventions,
        it creates appropriate UMLRelation instances and adds them to the diagram.

        :param uml_diagram: The UML diagram containing the classes to analyze.
        :type uml_diagram: UMLDiagram
        """
        pass
