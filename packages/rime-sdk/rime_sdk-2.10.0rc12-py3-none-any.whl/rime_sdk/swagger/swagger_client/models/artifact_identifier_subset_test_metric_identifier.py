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

class ArtifactIdentifierSubsetTestMetricIdentifier(object):
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
        'test_batch_id': 'str',
        'metric': 'str',
        'feature_names': 'list[str]',
        'subset_name': 'str'
    }

    attribute_map = {
        'test_batch_id': 'testBatchId',
        'metric': 'metric',
        'feature_names': 'featureNames',
        'subset_name': 'subsetName'
    }

    def __init__(self, test_batch_id=None, metric=None, feature_names=None, subset_name=None):  # noqa: E501
        """ArtifactIdentifierSubsetTestMetricIdentifier - a model defined in Swagger"""  # noqa: E501
        self._test_batch_id = None
        self._metric = None
        self._feature_names = None
        self._subset_name = None
        self.discriminator = None
        if test_batch_id is not None:
            self.test_batch_id = test_batch_id
        if metric is not None:
            self.metric = metric
        if feature_names is not None:
            self.feature_names = feature_names
        if subset_name is not None:
            self.subset_name = subset_name

    @property
    def test_batch_id(self):
        """Gets the test_batch_id of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501

        Uniquely specifies a Test Batch.  # noqa: E501

        :return: The test_batch_id of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._test_batch_id

    @test_batch_id.setter
    def test_batch_id(self, test_batch_id):
        """Sets the test_batch_id of this ArtifactIdentifierSubsetTestMetricIdentifier.

        Uniquely specifies a Test Batch.  # noqa: E501

        :param test_batch_id: The test_batch_id of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :type: str
        """

        self._test_batch_id = test_batch_id

    @property
    def metric(self):
        """Gets the metric of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501

        The metric name.  # noqa: E501

        :return: The metric of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """Sets the metric of this ArtifactIdentifierSubsetTestMetricIdentifier.

        The metric name.  # noqa: E501

        :param metric: The metric of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :type: str
        """

        self._metric = metric

    @property
    def feature_names(self):
        """Gets the feature_names of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501

        Human-readable names of the features. Must be sorted lexicographically.  # noqa: E501

        :return: The feature_names of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :rtype: list[str]
        """
        return self._feature_names

    @feature_names.setter
    def feature_names(self, feature_names):
        """Sets the feature_names of this ArtifactIdentifierSubsetTestMetricIdentifier.

        Human-readable names of the features. Must be sorted lexicographically.  # noqa: E501

        :param feature_names: The feature_names of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :type: list[str]
        """

        self._feature_names = feature_names

    @property
    def subset_name(self):
        """Gets the subset_name of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501

        Human-readable name of the feature subset used for the `subset_name` field. This is used to display the subset name on the frontend.  # noqa: E501

        :return: The subset_name of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._subset_name

    @subset_name.setter
    def subset_name(self, subset_name):
        """Sets the subset_name of this ArtifactIdentifierSubsetTestMetricIdentifier.

        Human-readable name of the feature subset used for the `subset_name` field. This is used to display the subset name on the frontend.  # noqa: E501

        :param subset_name: The subset_name of this ArtifactIdentifierSubsetTestMetricIdentifier.  # noqa: E501
        :type: str
        """

        self._subset_name = subset_name

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
        if issubclass(ArtifactIdentifierSubsetTestMetricIdentifier, dict):
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
        if not isinstance(other, ArtifactIdentifierSubsetTestMetricIdentifier):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
