"""Base normalizers. Other normalizers should inherit from one of those classes"""

import logging

from metanorm.errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class BaseMetadataNormalizer():
    """Base class for standard normalizers"""

    def __init__(self, parameter_names, harv_param_repetitive):
        """parameter_names: iterable"""
        self._parameter_names = parameter_names
        self._harv_param_repetitive = harv_param_repetitive
        self._next = None

    @property
    def next(self):
        """Get next normalizer"""
        return self._next

    @next.setter
    def next(self, normalizer):
        self._next = normalizer

    def normalize(self, raw_attributes, harv_parameters=None, harv_param_repetitive=None):
        """
        Loops through harv_parameters and checks if a method is available for each parameter.
        If so try it out. The 'raw_attributes' dictionary is then passed to the next normalizer, so
        that it can attempt to fill in any None value which might be left.
        """
        if not harv_parameters:
            harv_parameters = dict({(key, None) for key in self._parameter_names})

        if not harv_param_repetitive:
            harv_param_repetitive = dict({(key, None) for key in self._harv_param_repetitive})

        for param in harv_parameters.keys():
            if harv_parameters[param] is None:
                try:
                    # Maybe there is a cleaner way to implement this?
                    harv_parameters[param] = getattr(self, 'get_' + param)(raw_attributes)
                except AttributeError:
                    LOGGER.debug("%s: no method available for the '%s' parameter",
                                 self.__class__.__name__, param)

                if harv_parameters[param]:
                    LOGGER.debug("%s: found a value for the '%s' parameter",
                                 self.__class__.__name__, param)
                else:
                    LOGGER.debug("%s: value not found for the '%s' parameter",
                                 self.__class__.__name__, param)

        for param in harv_param_repetitive.keys():
            try:
                if harv_param_repetitive[param]==None:
                    harv_param_repetitive[param]=list()
                if getattr(self, 'get_' + param)(raw_attributes)!=None:
                    harv_param_repetitive[param].append(getattr(self, 'get_' + param)(raw_attributes)[0])
            except AttributeError:
                LOGGER.debug("%s: no method available for the '%s' parameter",
                             self.__class__.__name__, param)
            if harv_param_repetitive[param]:
                LOGGER.debug("%s: found a value for the '%s' parameter",
                             self.__class__.__name__, param)
            else:
                LOGGER.debug("%s: value not found for the '%s' parameter",
                             self.__class__.__name__, param)
        #adding (updating the normalized harvested parameters with the repetitive ones)
        harv_parameters.update(harv_param_repetitive)
        if self.next is None:
            return harv_parameters
        else:
            return self.next.normalize(raw_attributes, harv_parameters, harv_param_repetitive)


class BaseDefaultMetadataNormalizer(BaseMetadataNormalizer):
    """
    Base class for default normalizers. It raises an exception if any attempt to process an unknown
    parameter is made. All parameter methods defined in there must either succeed or raise a
    MetadataNormalizationError. It is strongly advised to return hard coded values in those methods.
    """

    def normalize(self, raw_attributes, harv_parameters=None, harv_param_repetitive=None):
        """
        Loops through harv_parameters and checks if a method is available for that parameter.
        If so use it,
        """
        if not harv_parameters:
            harv_parameters = dict({(key, None) for key in self._parameter_names})

        for param in harv_parameters.keys():
            if harv_parameters[param] is None:
                # Maybe there is a cleaner way to implement this?
                param_method = getattr(self, 'get_' + param, None)
                if callable(param_method):
                    harv_parameters[param] = param_method(raw_attributes)
                else:
                    raise MetadataNormalizationError(
                        f"Unable to find a value for the {param} parameter")

        return harv_parameters
