# src/uml_generator/class_diagrams/converters/class_converter.py

class ClassConverter:
    """
    ClassConverter is responsible for converting UMLClass objects 
    into their PlantUML string representation.
    """

    @staticmethod
    def convert_class(uml_class):
        """
        Generates the PlantUML representation for a given UMLClass object.

        :param uml_class: The UMLClass instance to convert.
        :type uml_class: UMLClass
        :return: A string representing the class in PlantUML format.
        :rtype: str
        """
        class_type = "interface" if uml_class.is_interface else "class"
        abstract_modifier = "abstract " if uml_class.is_abstract else ""

        # Start with the class definition line
        class_def = f"{abstract_modifier}{class_type} {uml_class.name}"

        # Begin the class body
        result = [f"{class_def} {{"]

        # Add attributes
        for attribute in uml_class.attributes:
            result.append(f"    {ClassConverter.format_attribute(attribute)}")

        # Add a blank line between attributes and methods if both exist
        if uml_class.attributes and uml_class.methods:
            result.append("")

        # Add methods
        for method in uml_class.methods:
            result.append(f"    {ClassConverter.format_method(method)}")

        # End the class body
        result.append("}")

        # Join all lines with newlines
        return "\n".join(result)

    @staticmethod
    def format_attribute(attribute):
        """
        Formats a UMLAttribute into a PlantUML attribute string.

        :param attribute: The UMLAttribute instance to format.
        :type attribute: UMLAttribute
        :return: A string representing the attribute in PlantUML format.
        :rtype: str
        """
        visibility = ClassConverter.format_visibility(attribute.visibility)
        static_modifier = " {static}" if attribute.is_static else ""
        final_modifier = " {final}" if attribute.is_final else ""
        return f"{visibility} {attribute.type} {attribute.name}{static_modifier}{final_modifier}"

    @staticmethod
    def format_method(method):
        """
        Formats a UMLMethod into a PlantUML method string.

        :param method: The UMLMethod instance to format.
        :type method: UMLMethod
        :return: A string representing the method in PlantUML format.
        :rtype: str
        """
        visibility = ClassConverter.format_visibility(method.visibility)
        static_modifier = " {static}" if method.is_static else ""
        final_modifier = " {final}" if method.is_final else ""

        params = ", ".join([f"{param.type} {param.name}" for param in method.parameters])
        return_type = f"{method.return_type} " if method.return_type else ""
        return f"{visibility} {return_type}{method.name}({params}){static_modifier}{final_modifier}"

    @staticmethod
    def format_visibility(visibility):
        """
        Converts visibility into PlantUML format.

        :param visibility: The visibility string ('public', 'private', etc.).
        :type visibility: str
        :return: A string representing the visibility in PlantUML format.
        :rtype: str
        """
        if visibility == "public":
            return "+"
        elif visibility == "private":
            return "-"
        elif visibility == "protected":
            return "#"
        elif visibility == "package":
            return "~"
        return ""
