"""Base normalizers. Other normalizers should inherit from one of those classes"""

import logging

from metanorm.errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class BaseMetadataNormalizer():
    """Base class for standard normalizers"""

    def __init__(self, output_parameter_names, output_cumulative_parameter_names):
        """parameter_names: iterable"""
        self._output_parameter_names = output_parameter_names
        self._output_cumulative_parameter_names = output_cumulative_parameter_names
        self._next = None

    @property
    def next(self):
        """Get next normalizer"""
        return self._next

    @next.setter
    def next(self, normalizer):
        self._next = normalizer

    def normalize(self, raw_attributes, output_parameter_names=None, output_cumulative_parameter_names=None):
        """
        Loops through output_parameter_names and checks if a method is available for each parameter.
        If so try it out. The 'raw_attributes' dictionary is then passed to the next normalizer, so
        that it can attempt to fill in any None value which might be left.
        """
        if not output_parameter_names:
            output_parameter_names = dict({(key, None) for key in self._output_parameter_names})

        if not output_cumulative_parameter_names:
            output_cumulative_parameter_names = {key: [] for key in self._output_cumulative_parameter_names}

        for param in output_parameter_names.keys():
            if output_parameter_names[param] is None:
                try:
                    # Maybe there is a cleaner way to implement this?
                    output_parameter_names[param] = getattr(self, 'get_' + param)(raw_attributes)
                except AttributeError:
                    LOGGER.debug("%s: no method available for the '%s' parameter",
                                 self.__class__.__name__, param)

                if output_parameter_names[param]:
                    LOGGER.debug("%s: found a value for the '%s' parameter",
                                 self.__class__.__name__, param)
                else:
                    LOGGER.debug("%s: value not found for the '%s' parameter",
                                 self.__class__.__name__, param)

        for param in output_cumulative_parameter_names.keys():
            try:
                if getattr(self, 'get_' + param)(raw_attributes) is not None:
                    output_cumulative_parameter_names[param].extend(getattr(self, 'get_' + param)(raw_attributes))
            except AttributeError:
                LOGGER.debug("%s: no method available for the '%s' parameter",
                             self.__class__.__name__, param)
            if output_cumulative_parameter_names[param]:
                LOGGER.debug("%s: found a value for the '%s' parameter",
                             self.__class__.__name__, param)
            else:
                LOGGER.debug("%s: value not found for the '%s' parameter",
                             self.__class__.__name__, param)

        if self.next is None:
            return output_parameter_names
        else:
            return self.next.normalize(raw_attributes, output_parameter_names, output_cumulative_parameter_names)


class BaseDefaultMetadataNormalizer(BaseMetadataNormalizer):
    """
    Base class for default normalizers. It raises an exception if any attempt to process an unknown
    parameter is made. All parameter methods defined in there must either succeed or raise a
    MetadataNormalizationError. It is strongly advised to return hard coded values in those methods.
    """

    def normalize(self, raw_attributes, output_parameter_names=None, output_cumulative_parameter_names=None):
        """
        Loops through output_parameter_names and checks if a method is available for that parameter.
        If so use it,
        """
        if not output_parameter_names:
            output_parameter_names = dict({(key, None) for key in self._output_parameter_names})

        for param in output_parameter_names.keys():
            if output_parameter_names[param] is None:
                # Maybe there is a cleaner way to implement this?
                param_method = getattr(self, 'get_' + param, None)
                if callable(param_method):
                    output_parameter_names[param] = param_method(raw_attributes)
                else:
                    raise MetadataNormalizationError(
                        f"Unable to find a value for the {param} parameter")
        #adding (updating the normalized harvested parameters with the repetitive ones)
        output_parameter_names.update(output_cumulative_parameter_names)
        return output_parameter_names
