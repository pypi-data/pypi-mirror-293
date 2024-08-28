# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` for all the firewall methods and `rime-api-key` for all other methods.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RimeCreateFirewallRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'project_id': 'RimeUUID',
        'model_id': 'RimeUUID',
        'bin_size': 'str',
        'ref_data_id': 'str',
        'scheduled_ct_parameters': 'CreateFirewallRequestScheduledCTParameters'
    }

    attribute_map = {
        'project_id': 'projectId',
        'model_id': 'modelId',
        'bin_size': 'binSize',
        'ref_data_id': 'refDataId',
        'scheduled_ct_parameters': 'scheduledCtParameters'
    }

    def __init__(self, project_id=None, model_id=None, bin_size=None, ref_data_id=None, scheduled_ct_parameters=None):  # noqa: E501
        """RimeCreateFirewallRequest - a model defined in Swagger"""  # noqa: E501
        self._project_id = None
        self._model_id = None
        self._bin_size = None
        self._ref_data_id = None
        self._scheduled_ct_parameters = None
        self.discriminator = None
        if project_id is not None:
            self.project_id = project_id
        if model_id is not None:
            self.model_id = model_id
        self.bin_size = bin_size
        self.ref_data_id = ref_data_id
        if scheduled_ct_parameters is not None:
            self.scheduled_ct_parameters = scheduled_ct_parameters

    @property
    def project_id(self):
        """Gets the project_id of this RimeCreateFirewallRequest.  # noqa: E501


        :return: The project_id of this RimeCreateFirewallRequest.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this RimeCreateFirewallRequest.


        :param project_id: The project_id of this RimeCreateFirewallRequest.  # noqa: E501
        :type: RimeUUID
        """

        self._project_id = project_id

    @property
    def model_id(self):
        """Gets the model_id of this RimeCreateFirewallRequest.  # noqa: E501


        :return: The model_id of this RimeCreateFirewallRequest.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this RimeCreateFirewallRequest.


        :param model_id: The model_id of this RimeCreateFirewallRequest.  # noqa: E501
        :type: RimeUUID
        """

        self._model_id = model_id

    @property
    def bin_size(self):
        """Gets the bin_size of this RimeCreateFirewallRequest.  # noqa: E501

        Duration of each bin size of continuous tests.  # noqa: E501

        :return: The bin_size of this RimeCreateFirewallRequest.  # noqa: E501
        :rtype: str
        """
        return self._bin_size

    @bin_size.setter
    def bin_size(self, bin_size):
        """Sets the bin_size of this RimeCreateFirewallRequest.

        Duration of each bin size of continuous tests.  # noqa: E501

        :param bin_size: The bin_size of this RimeCreateFirewallRequest.  # noqa: E501
        :type: str
        """
        if bin_size is None:
            raise ValueError("Invalid value for `bin_size`, must not be `None`")  # noqa: E501

        self._bin_size = bin_size

    @property
    def ref_data_id(self):
        """Gets the ref_data_id of this RimeCreateFirewallRequest.  # noqa: E501

        Uniquely specifies a reference data set.  # noqa: E501

        :return: The ref_data_id of this RimeCreateFirewallRequest.  # noqa: E501
        :rtype: str
        """
        return self._ref_data_id

    @ref_data_id.setter
    def ref_data_id(self, ref_data_id):
        """Sets the ref_data_id of this RimeCreateFirewallRequest.

        Uniquely specifies a reference data set.  # noqa: E501

        :param ref_data_id: The ref_data_id of this RimeCreateFirewallRequest.  # noqa: E501
        :type: str
        """
        if ref_data_id is None:
            raise ValueError("Invalid value for `ref_data_id`, must not be `None`")  # noqa: E501

        self._ref_data_id = ref_data_id

    @property
    def scheduled_ct_parameters(self):
        """Gets the scheduled_ct_parameters of this RimeCreateFirewallRequest.  # noqa: E501


        :return: The scheduled_ct_parameters of this RimeCreateFirewallRequest.  # noqa: E501
        :rtype: CreateFirewallRequestScheduledCTParameters
        """
        return self._scheduled_ct_parameters

    @scheduled_ct_parameters.setter
    def scheduled_ct_parameters(self, scheduled_ct_parameters):
        """Sets the scheduled_ct_parameters of this RimeCreateFirewallRequest.


        :param scheduled_ct_parameters: The scheduled_ct_parameters of this RimeCreateFirewallRequest.  # noqa: E501
        :type: CreateFirewallRequestScheduledCTParameters
        """

        self._scheduled_ct_parameters = scheduled_ct_parameters

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RimeCreateFirewallRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RimeCreateFirewallRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
