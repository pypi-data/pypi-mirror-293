# src/uml_generator/parsers/java_parser.py

import re
from uml_generator.models.uml_class import UMLClass
from uml_generator.models.uml_method import UMLMethod
from uml_generator.parsers.base_parser import BaseParser
from uml_generator.models.uml_relation import UMLRelation
from uml_generator.models.uml_attribute import UMLAttribute
from uml_generator.models.uml_parameter import UMLParameter
from uml_generator.types.relations import EXTENDS, IMPLEMENTS, ASSOCIATION

class JavaParser(BaseParser):
    """
    A parser for Java files that extracts UML class representations from the source code.
    """

    def __init__(self, filepath):
        """
        Initializes the JavaParser with the path to the Java file to be parsed.

        :param filepath: The path to the Java file.
        :type filepath: str
        """
        super().__init__(filepath)

    def parse(self):
        """
        Parses the Java file and returns a list of UMLClass instances representing the parsed classes.

        This method reads the entire Java file, parses each class or interface header,
        attributes, and methods, and then compiles them into UMLClass instances.

        :return: A list of UMLClass instances representing the parsed classes.
        :rtype: List[UMLClass]
        """
        # Open and read the entire content of the Java file
        with open(self.filepath, 'r') as file:
            java_code = file.read()

        # Define a regular expression pattern to match class or interface declarations
        pattern = r'\b(public|protected|private)?\s*(abstract|final|static)?\s*(class|interface)\s+(\w+)(\s+extends\s+\w+)?(\s+implements\s+[\w,\s]+)?'

        # Split the Java code into sections based on the class/interface declarations using the defined pattern
        class_splits = re.split(pattern, java_code)

        # Initialize an empty list to store the UMLClass instances
        uml_classes = []

        # Iterate over the split results to process each class or interface found
        for i in range(1, len(class_splits), 7):
            header_parts = []
            
            # Collect parts of the class or interface header (visibility, modifiers, type, name, inheritance, etc.)
            if class_splits[i]:
                header_parts.append(class_splits[i].strip())
            if class_splits[i + 1]:
                header_parts.append(class_splits[i + 1].strip())
            if class_splits[i + 2]:
                header_parts.append(class_splits[i + 2].strip())
            if class_splits[i + 3]:
                header_parts.append(class_splits[i + 3].strip())
            if class_splits[i + 4]:
                header_parts.append(class_splits[i + 4].strip())
            if class_splits[i + 5]:
                header_parts.append(class_splits[i + 5].strip())
            
            # Join all parts to form the full header of the class or interface
            header = ' '.join(header_parts)

            # Extract the body of the class or interface (the code that follows the header)
            body = class_splits[i + 6] or ""

            # Combine the header and body to get the full code of the class or interface
            class_code = header +  " " + body

            # Parse the header of the class or interface to create a UMLClass instance
            uml_class = self.parse_header(class_code)

            # Parse the attributes of the class and add them to the UMLClass instance
            self.parse_attributes(class_code, uml_class)

            # Parse the methods of the class and add them to the UMLClass instance
            self.parse_methods(class_code, uml_class)

            # Add the parsed UMLClass to the list
            uml_classes.append(uml_class)

        return uml_classes

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
        # Regex pattern to match the class or interface header
        header_match = re.search(
            r'((public|protected|private)?\s*(abstract\s+)?(class|interface)\s+\w+(?:\s+extends\s+[\w\s,]+)?(?:\s+implements\s+[\w\s,]+)?)\s*\{',
            java_code
        )

        # If no match is found, return None
        if not header_match:
            return None
        
        # Extract the full header string
        header = header_match.group(1)

        # Split the header into individual words
        class_matches = re.findall(r'\b\w+\b', header)

        # Initialize default values for the class attributes
        visibility = None or "package"
        is_abstract = False
        is_interface = False
        class_name = None
        superclasses = []
        interfaces = []

        # Flags to determine whether we are in the 'extends' or 'implements' part of the header
        in_extends = False
        in_implements = False

        # Iterate over each word in the header
        for i, word in enumerate(class_matches):
            if word in ["public", "protected", "private"]:
                # Set the visibility of the class or interface
                visibility = word
            
            elif word == "abstract":
                # Mark the class as abstract
                is_abstract = True

            elif word in ["class", "interface"]:
                # Determine if it is a class or an interface
                is_interface = (word == "interface")

                # The next word after 'class' or 'interface' is the class name
                class_name = class_matches[i + 1]

            elif word == "extends":
                # Entering the 'extends' section of the header
                in_extends = True
                in_implements = False

            elif word == "implements":
                # Entering the 'implements' section of the header
                in_extends = False
                in_implements = True

            elif in_extends:
                # Add the superclass to the list of superclasses
                superclasses.append(word)

            elif in_implements:
                # Add the interface to the list of implemented interfaces
                interfaces.append(word)

        # Return a UMLClass instance with the parsed values
        return UMLClass(visibility, is_abstract, is_interface, class_name, superclasses, interfaces)

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
        # First, remove methods from the Java code to avoid parsing method-local variables as attributes
        java_code_without_methods = JavaParser.remove_methods(java_code)

        # Regex pattern to match Java attributes, including those with initial values
        attribute_pattern = re.compile(
            r'((public|protected|private)?\s*(static\s+)?(final\s+)?([\w<>]+)\s+(\w+)\s*(=\s*[^;]+)?\s*;)'
        )

        # Iterate over all matches of the pattern in the Java code
        for match in attribute_pattern.finditer(java_code_without_methods):
            # Skip matches that contain 'return', 'throw' and "throws"
            if "return" in match.group(0) or "throws" in match.group(0) or "throw" in match.group(0):
                continue

            # Extract the visibility of the attribute, defaulting to 'package' if none is specified
            visibility = match.group(2) or "package"

            # Determine if the attribute is static
            is_static = bool(match.group(3))

            # Determine if the attribute is final
            is_final = bool(match.group(4))

            # Extract the type of the attribute (e.g., int, String)
            type_ = match.group(5)

            # If the type is generic (e.g., List<Order>), extract only the inner type
            if '<' in type_ and '>' in type_:
                type_ = re.search(r'<(\w+)>', type_).group(1)

            # Extract the name of the attribute
            name = match.group(6)

            # Create a UMLAttribute instance and add it to the UMLClass
            uml_class.add_attribute(UMLAttribute(visibility, is_static, is_final, type_, name))

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
        # Regex pattern to match Java methods, including handling of annotations and complex method signatures
        method_pattern = re.compile(
            r'\b(public|protected|private)?\s*(static\s+)?(final\s+)?([\w<>[\]]+\s+)?(\w+)\s*\(([^)]*)\)\s*(throws\s+[\w\s,<>\[\]]+(\s*,\s*[\w\s,<>\[\]]+)*)?\s*\{',
            re.DOTALL
        )

        # Iterate over all matches of the pattern in the Java code
        for match in method_pattern.finditer(java_code):
            visibility = match.group(1) or "package"
            is_static = bool(match.group(2))
            is_final = bool(match.group(3))
            return_type = match.group(4).strip() if match.group(4) else None
            name = match.group(5)

            # Validate that the name is not a control structure (like if, for, while, etc.)
            if name in ["if", "for", "while", "switch", "catch", "else"]:
                continue  # Skip this iteration if the "method" is actually a control structure

            # Extract the parameters as a string
            parameters_str = match.group(6).strip()

            # Initialize a list to hold UMLParameter instances
            parameters = []

            # If there are parameters, split them and create UMLParameter instances
            if parameters_str:
                for param in parameters_str.split(','):
                    param = param.strip()
                    param_type, param_name = param.rsplit(' ', 1)
                    parameters.append(UMLParameter(name=param_name, type=param_type))

            # Create a UMLMethod instance and add it to the UMLClass
            uml_class.add_method(UMLMethod(visibility, is_static, is_final, return_type, name, parameters))

    def create_relations(self, uml_diagram):
        """
        Creates UML relationships (associations, inheritance, implementation) between classes based on their attributes.

        This method iterates through all classes in the UML diagram and examines their attributes to determine
        if they reference other classes within the diagram. Depending on the context and naming conventions,
        it creates appropriate UMLRelation instances and adds them to the diagram.

        :param uml_diagram: The UML diagram containing the classes to analyze.
        :type uml_diagram: UMLDiagram
        """
        # Retrieve the set of all class names in the diagram for quick lookup
        uml_classes = uml_diagram.get_all_classes()
        class_names = {cls.name for cls in uml_classes}

        # Iterate over all classes in the diagram
        for cls in uml_classes:
            # Check for superclass relationships
            for superclass in cls.superclasses:
                # Create a UMLRelation for the 'extends' relationship
                uml_diagram.add_relation(UMLRelation(source=cls.name, target=superclass, relation_type=EXTENDS))
        
            # Check for interface implementation relationships
            for interface in cls.interfaces:
                # Create a UMLRelation for the 'implements' relationship
                uml_diagram.add_relation(UMLRelation(source=cls.name, target=interface, relation_type=IMPLEMENTS))

            # Create a list to store attributes to remove
            attributes_to_remove = []

            # Check for attribute-based associations
            for attribute in cls.attributes:
                # Extract the core type from the attribute type
                match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)<([a-zA-Z_][a-zA-Z0-9_]*)>', attribute.type)

                if match:
                    # If the attribute type is like List<Order>, extract Order
                    core_type = match.group(2)
                else:
                    # Otherwise, just use the attribute type itself
                    core_type = attribute.type

                # If the core type is the name of another class, create an association
                if core_type in class_names:
                    # Determine the multiplicity based on the attribute type
                    if any(keyword in attribute.type for keyword in ['List', 'Set', 'Map', '[]']):
                        multiplicity = "1..*"
                    else:
                        multiplicity = "1"

                    # Create the association relation
                    uml_diagram.add_relation(UMLRelation(cls.name, attribute.type, ASSOCIATION, multiplicity, attribute.name))

                    # Mark the attribute for removal
                    attributes_to_remove.append(attribute)

            # Remove the attributes that were converted to associations
            for attribute in attributes_to_remove:
                cls.attributes.remove(attribute)

    def remove_methods(java_code):
        """
        Removes methods from the Java code by identifying their headers and their corresponding bodies using brace counting.
        
        :param java_code: The Java code containing the class.
        :type java_code: str
        :return: Java code with methods removed.
        :rtype: str
        """
        # Split the Java code into lines for easier processing
        lines = java_code.splitlines()
        cleaned_code = []
        inside_method = False
        brace_count = 0

        # Regular expression pattern to identify method signatures
        method_pattern = re.compile(
            r'^\s*(public|protected|private)?\s*(static\s+)?(final\s+)?([\w<>[\]]+\s+)?(\w+)\s*\([^)]*\)\s*(throws\s+[\w\s,]+)?\s*\{',
            re.MULTILINE
        )

        # Iterate through each line of the code
        for line in lines:
            if inside_method:
                # Check for opening and closing braces and adjust the count
                brace_count += line.count('{')
                brace_count -= line.count('}')

                # If the brace count is zero, we've exited the method
                if brace_count == 0:
                    inside_method = False

                continue
            
            # If a method signature is found, start ignoring lines until we exit the method
            if method_pattern.search(line):
                inside_method = True
                brace_count = line.count('{') - line.count('}')
                continue
            
            # If not inside a method, keep the line
            cleaned_code.append(line)

        return '\n'.join(cleaned_code)
