# src/uml_generator/class_diagrams/core/diagram_drawer.py

from plantuml import PlantUML

class DiagramDrawer:
    """
    DiagramDrawer is responsible for converting UML code into a visual diagram using PlantUML.
    It can either write the UML code to a file or process the code directly.
    """

    @staticmethod
    def draw_diagram(uml_code, output_file="uml"):
        """
        Converts the given UML code into a diagram and saves it as a .png file.

        :param uml_code: The UML code to convert into a diagram.
        :type uml_code: str
        :param output_file: The name for the output file (including the .png extension). Defaults to "uml.png".
        :type output_file: str
        """
        output_file += ".png"

        # Create a PlantUML object to process the UML code directly
        plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

        # Process the UML code to get the raw image data (PNG format)
        png_data = plantuml.processes(uml_code)

        # Write the PNG data to a file
        with open(output_file, 'wb') as file:
            file.write(png_data)
