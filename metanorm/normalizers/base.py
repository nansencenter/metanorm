"""Base normalizers. Other normalizers should inherit from one of those classes"""

import logging

from metanorm.errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class BaseMetadataNormalizer():
    """Base class for standard normalizers"""

    def __init__(self, parameter_names):
        """parameter_names: iterable"""
        self._parameter_names = parameter_names
        self._next = None

    @property
    def next(self):
        """Get next normalizer"""
        return self._next

    @next.setter
    def next(self, normalizer):
        self._next = normalizer

    def normalize(self, raw_attributes, parameters=None):
        """
        Loops through parameters and checks if a method is available for each parameter.
        If so try it out. The 'raw_attributes' dictionary is then passed to the next normalizer, so
        that it can attempt to fill in any None value which might be left.
        """
        if not parameters:
            parameters = dict({(key, None) for key in self._parameter_names})

        for param in parameters.keys():
            if parameters[param] is None:
                try:
                    # Maybe there is a cleaner way to implement this?
                    parameters[param] = getattr(self, 'get_' + param)(raw_attributes)
                except AttributeError:
                    LOGGER.debug("%s: no method available for the '%s' parameter",
                                 self.__class__.__name__, param)

                if parameters[param]:
                    LOGGER.debug("%s: found a value for the '%s' parameter",
                                 self.__class__.__name__, param)
                else:
                    LOGGER.debug("%s: value not found for the '%s' parameter",
                                 self.__class__.__name__, param)

        if self.next is None:
            return parameters
        else:
            return self.next.normalize(raw_attributes, parameters)


class BaseDefaultMetadataNormalizer(BaseMetadataNormalizer):
    """
    Base class for default normalizers. It raises an exception if any attempt to process an unknown
    parameter is made. All parameter methods defined in there must either succeed or raise a
    MetadataNormalizationError. It is strongly advised to return hard coded values in those methods.
    """

    def normalize(self, raw_attributes, parameters=None):
        """
        Loops through parameters and checks if a method is available for that parameter.
        If so use it,
        """
        if not parameters:
            parameters = dict({(key, None) for key in self._parameter_names})

        for param in parameters.keys():
            if parameters[param] is None:
                # Maybe there is a cleaner way to implement this?
                param_method = getattr(self, 'get_' + param, None)
                if callable(param_method):
                    parameters[param] = param_method(raw_attributes)
                else:
                    raise MetadataNormalizationError(
                        f"Unable to find a value for the {param} parameter")

        return parameters
