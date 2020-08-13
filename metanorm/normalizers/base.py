"""Base normalizers. Other normalizers should inherit from one of those classes"""

import logging

from metanorm.errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class BaseMetadataNormalizer():
    """Base class for standard normalizers"""

    def __init__(self, output_parameters_names=None, output_cumulative_parameters_names=None):
        """
        output_parameter_names and output_cumulative_parameter_names should contain the lists of
        desired parameters names to extract.
        """
        if output_parameters_names is None and output_cumulative_parameters_names is None:
            raise ValueError((
                "Either output_parameter_names or output_cumulative_parameter_names "
                "must be specified"
            ))
        self._output_parameters_names = output_parameters_names or []
        self._output_cumulative_parameters_names = output_cumulative_parameters_names or []
        self._next = None

    @property
    def next(self):
        """Get next normalizer"""
        return self._next

    @next.setter
    def next(self, normalizer):
        self._next = normalizer

    def normalize(self, raw_attributes, output_parameters=None, output_cumulative_parameters=None):
        """
        Loops through the desired output parameters and checks if a method is available for each
        parameter. If so, try it out. The 'raw_attributes' dictionary is then passed to the next
        normalizer, so that it can attempt to fill in the missing values.
        There are two types of parameters with slightly different behavior:
          - standard parameters: the first normalizer which finds a value "wins", so the order of
            the normalizers matters for this type.
          - cumulative parameters are lists to which each normalizer adds the values it finds,
            regardless of normalizers ordering.
        """
        if not output_parameters:
            output_parameters = {
                key: None for key in self._output_parameters_names}

        if not output_cumulative_parameters:
            output_cumulative_parameters = {key: []
                                            for key in self._output_cumulative_parameters_names}

        for param in output_parameters.keys():
            if output_parameters[param] is None:
                try:
                    # Maybe there is a cleaner way to implement this?
                    output_parameters[param] = getattr(self, 'get_' + param)(raw_attributes)
                except AttributeError:
                    LOGGER.debug("%s: no method available for the '%s' parameter",
                                 self.__class__.__name__, param)

                if output_parameters[param]:
                    LOGGER.debug("%s: found a value for the '%s' parameter",
                                 self.__class__.__name__, param)
                else:
                    LOGGER.debug("%s: value not found for the '%s' parameter",
                                 self.__class__.__name__, param)

        for param in output_cumulative_parameters.keys():
            previous_len = len(output_cumulative_parameters[param])
            try:
                new_members = getattr(self, 'get_' + param)(raw_attributes)
                for new_member in new_members:
                    if new_member not in output_cumulative_parameters[param]:
                        output_cumulative_parameters[param].append(new_member)
            except AttributeError:
                LOGGER.debug("%s: no method available for the '%s' parameter",
                             self.__class__.__name__, param)

            if previous_len < len(output_cumulative_parameters[param]):
                LOGGER.debug("%s: found a value for the '%s' parameter",
                             self.__class__.__name__, param)
            else:
                LOGGER.debug("%s: value not found for the '%s' parameter",
                             self.__class__.__name__, param)

        if self.next is None:
            # the second one that is written for return statement is only for testing purposes,
            # it have no role in a standard execution of the code
            return {**output_parameters, **output_cumulative_parameters}
        else:
            return self.next.normalize(
                raw_attributes, output_parameters, output_cumulative_parameters)


class BaseDefaultMetadataNormalizer(BaseMetadataNormalizer):
    """
    Base class for default normalizers. It raises an exception if any attempt to process an unknown
    parameter is made. All parameter methods defined in there must either succeed or raise a
    MetadataNormalizationError. It is strongly advised to return hard coded values in those methods.
    """

    def normalize(self, raw_attributes, output_parameters=None, output_cumulative_parameters=None):
        """
        Loops through output_parameters and checks if a method is available for that parameter.
        If so use it, if not raise a MetadataNormalizationError
        """
        if not output_parameters:
            output_parameters = dict({(key, None) for key in self._output_parameters_names})

        for param in output_parameters.keys():
            if output_parameters[param] is None:
                # Maybe there is a cleaner way to implement this?
                param_method = getattr(self, 'get_' + param, None)
                if callable(param_method):
                    output_parameters[param] = param_method(raw_attributes)
                else:
                    raise MetadataNormalizationError(
                        f"Unable to find a value for the {param} parameter")
        # updating the standard normalized parameters with the cumulative ones
        output_parameters.update(output_cumulative_parameters)
        return output_parameters
