# src/uml_generator/class_diagrams/core/project_analyzer.py

import os
from uml_generator.class_diagrams.types.languages import LANGUAGES
from uml_generator.class_diagrams.models.uml_diagram import UMLDiagram
from uml_generator.class_diagrams.parsers.java_parser import JavaParser

class ProjectAnalyzer:
    """
    Analyzes all source files in a given directory and generates a comprehensive UML diagram.

    This class is responsible for parsing all source files in a specified directory
    and aggregating the results into a single UMLDiagram instance.
    """

    def __init__(self, directory_path, language_type):
        """
        Initializes the ProjectAnalyzer with the path to the directory to be analyzed and the programming language type.

        :param directory_path: The path to the directory containing source files.
        :type directory_path: str
        :param language_type: The programming language type (e.g., 'JAVA', 'CPP').
        :type language_type: str
        """
        self.directory_path = directory_path
        self.language_type = language_type

    def analyze(self):
        """
        Analyzes all source files in the specified directory and returns a UMLDiagram.

        This method iterates through all relevant files in the directory, parses each file
        using the appropriate parser, and aggregates the results into a single UMLDiagram.

        :return: A UMLDiagram containing the parsed UML classes from all source files.
        :rtype: UMLDiagram
        """
        # Create an empty UMLDiagram to hold the parsed classes
        diagram = UMLDiagram()

        # Get the appropriate parser class and file extension based on the language type
        parser_class = self._get_parser_class()
        file_extension = self._get_file_extension()

        # Iterate over all files in the directory
        for root, dirs, files in os.walk(self.directory_path):
            for file in files:
                # Check if the file has the appropriate extension for the language type
                if file.endswith(file_extension) and 'test' not in file.lower():
                    # Construct the full file path
                    file_path = os.path.join(root, file)

                    # Initialize the parser for the current file
                    parser = parser_class(file_path)

                    # Parse the file and get the list of UMLClass instances
                    uml_classes = parser.parse()

                    # Iterate over each UMLClass in the list and add it to the UMLDiagram
                    for uml_class in uml_classes:
                        diagram.add_class(uml_class)

        # After all classes are added, create relations within the diagram
        parser.create_relations(diagram)
        
        # Return the UMLDiagram containing all parsed classes
        return diagram

    def _get_parser_class(self):
        """
        Returns the appropriate parser class based on the language type.

        :return: The parser class (e.g., JavaParser, CPPParser).
        :rtype: class
        """
        if self.language_type == LANGUAGES.JAVA:
            return JavaParser
        else:
            raise ValueError(f"Unsupported language type: {self.language_type}")

    def _get_file_extension(self):
        """
        Returns the appropriate file extension for the given language type.

        :return: The file extension (e.g., '.java', '.cpp').
        :rtype: str
        """
        if self.language_type == LANGUAGES.JAVA:
            return ".java"
        else:
            raise ValueError(f"Unsupported language type: {self.language_type}")
