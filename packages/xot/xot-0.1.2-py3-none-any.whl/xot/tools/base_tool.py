"""
This module defines the abstract base class for all tools.

It provides a common interface that all tool classes must implement.
"""

from abc import ABC, abstractmethod
from typing import Type, Dict


class BaseTool(ABC):
    """
    Abstract base class for all tools.

    This class defines the interface that all tool classes must implement.
    It includes methods for initialization, configuration, usage, and
    retrieving the tool's name.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize the tool.

        This method should be implemented by subclasses to set up any
        necessary initial state or configurations for the tool.
        """
        pass

    @abstractmethod
    def use(self, input_text: str) -> str:
        """
        Use the tool with the given input.

        Args:
            input_text (str): The input text for the tool.

        Returns:
            str: The output of the tool.
        """
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        Get the name of the tool.

        Returns:
            str: The name of the tool.
        """
        pass


class ToolRegistry:
    """
    A registry for managing tool classes.

    This class provides methods for registering tool classes, retrieving
    them by name, and listing all registered tools.
    """

    _registry: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register(cls, name: str):
        """
        A decorator for registering tool classes.

        Args:
            name (str): The unique name for the tool.

        Returns:
            callable: A decorator function that registers the tool class.

        Raises:
            ValueError: If a tool with the given name is already registered.
        """

        def decorator(tool_cls: Type[BaseTool]):
            if name in cls._registry:
                raise ValueError(f"Tool with name '{name}' is already registered")
            cls._registry[name] = tool_cls
            return tool_cls

        return decorator

    @classmethod
    def get_tool_class(cls, name: str) -> Type[BaseTool]:
        """
        Retrieve a tool class by its registered name.

        Args:
            name (str): The name of the tool to retrieve.

        Returns:
            Type[BaseTool]: The tool class.

        Raises:
            ValueError: If no tool is registered with the given name.
        """
        if name not in cls._registry:
            raise ValueError(f"No tool registered with name '{name}'")
        return cls._registry[name]

    @classmethod
    def list_tools(cls) -> Dict[str, Type[BaseTool]]:
        """
        Get a dictionary of all registered tools.

        Returns:
            Dict[str, Type[BaseTool]]: A dictionary mapping tool names to their classes.
        """
        return cls._registry.copy()


def get_tool_class(name: str) -> Type[BaseTool]:
    """
    A convenience function to get a tool class by name.

    Args:
        name (str): The name of the tool to retrieve.

    Returns:
        Type[BaseTool]: The tool class.

    Raises:
        ValueError: If no tool is registered with the given name.
    """
    return ToolRegistry.get_tool_class(name)
