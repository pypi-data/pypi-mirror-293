# src/uml_generator/class_diagrams/__init__.py

from uml_generator.class_diagrams.types.languages import LANGUAGES
from uml_generator.class_diagrams.core.diagram_drawer import DiagramDrawer
from uml_generator.class_diagrams.core.project_analyzer import ProjectAnalyzer
from uml_generator.class_diagrams.converters.diagram_converter import DiagramConverter

def generate_class_uml(project_directory, language_type, output_file):
    """
    Main function to analyze a project and generate a UML diagram.

    This function takes a directory path, a programming language type, and an output file path as input.
    It analyzes the project located in the specified project directory, generates a UML diagram, converts it 
    to PlantUML code, and saves the drawn diagram to the specified output file.

    :param project_directory: The directory path of the project to analyze.
    :type directory: str
    :param language_type: The type of programming language used in the project (e.g., JAVA, CPP).
    :type language_type: str
    :param output_file: The file path where the UML diagram should be saved.
    :type output_file: str
    """
    # Create an instance of ProjectAnalyzer using the provided directory and language type
    analyzer = ProjectAnalyzer(project_directory, language_type)

    # Analyze the project and obtain the corresponding UML diagram
    uml_diagram = analyzer.analyze()

    # Convert the UML diagram to PlantUML code format
    uml_code = DiagramConverter.convert_diagram(uml_diagram)

    # Draw the UML diagram and save it to the specified output file
    DiagramDrawer.draw_diagram(uml_code, output_file)


__all__ = ['generate_class_uml', 'LANGUAGES']
