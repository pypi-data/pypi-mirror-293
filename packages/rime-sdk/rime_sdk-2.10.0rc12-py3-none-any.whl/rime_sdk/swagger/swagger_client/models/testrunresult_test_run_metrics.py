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

class TestrunresultTestRunMetrics(object):
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
        'model_perf': 'dict(str, TestRunMetricsModelPerfMetric)',
        'average_prediction': 'float',
        'num_inputs': 'str',
        'num_failing_inputs': 'str',
        'duration_millis': 'str',
        'severity_counts': 'RimeSeverityCounts',
        'summary_counts': 'TestrunresultResultSummaryCounts',
        'category_summary_metrics': 'list[TestRunMetricsCategorySummaryMetric]',
        'risk_scores': 'list[RiskscoreRiskScore]'
    }

    attribute_map = {
        'model_perf': 'modelPerf',
        'average_prediction': 'averagePrediction',
        'num_inputs': 'numInputs',
        'num_failing_inputs': 'numFailingInputs',
        'duration_millis': 'durationMillis',
        'severity_counts': 'severityCounts',
        'summary_counts': 'summaryCounts',
        'category_summary_metrics': 'categorySummaryMetrics',
        'risk_scores': 'riskScores'
    }

    def __init__(self, model_perf=None, average_prediction=None, num_inputs=None, num_failing_inputs=None, duration_millis=None, severity_counts=None, summary_counts=None, category_summary_metrics=None, risk_scores=None):  # noqa: E501
        """TestrunresultTestRunMetrics - a model defined in Swagger"""  # noqa: E501
        self._model_perf = None
        self._average_prediction = None
        self._num_inputs = None
        self._num_failing_inputs = None
        self._duration_millis = None
        self._severity_counts = None
        self._summary_counts = None
        self._category_summary_metrics = None
        self._risk_scores = None
        self.discriminator = None
        if model_perf is not None:
            self.model_perf = model_perf
        if average_prediction is not None:
            self.average_prediction = average_prediction
        if num_inputs is not None:
            self.num_inputs = num_inputs
        if num_failing_inputs is not None:
            self.num_failing_inputs = num_failing_inputs
        if duration_millis is not None:
            self.duration_millis = duration_millis
        if severity_counts is not None:
            self.severity_counts = severity_counts
        if summary_counts is not None:
            self.summary_counts = summary_counts
        if category_summary_metrics is not None:
            self.category_summary_metrics = category_summary_metrics
        if risk_scores is not None:
            self.risk_scores = risk_scores

    @property
    def model_perf(self):
        """Gets the model_perf of this TestrunresultTestRunMetrics.  # noqa: E501

        The model performance over the test run as computed using various metrics.  # noqa: E501

        :return: The model_perf of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: dict(str, TestRunMetricsModelPerfMetric)
        """
        return self._model_perf

    @model_perf.setter
    def model_perf(self, model_perf):
        """Sets the model_perf of this TestrunresultTestRunMetrics.

        The model performance over the test run as computed using various metrics.  # noqa: E501

        :param model_perf: The model_perf of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: dict(str, TestRunMetricsModelPerfMetric)
        """

        self._model_perf = model_perf

    @property
    def average_prediction(self):
        """Gets the average_prediction of this TestrunresultTestRunMetrics.  # noqa: E501

        The average prediction for the test run (only defined for a subset of tasks such as binary classification).  # noqa: E501

        :return: The average_prediction of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: float
        """
        return self._average_prediction

    @average_prediction.setter
    def average_prediction(self, average_prediction):
        """Sets the average_prediction of this TestrunresultTestRunMetrics.

        The average prediction for the test run (only defined for a subset of tasks such as binary classification).  # noqa: E501

        :param average_prediction: The average_prediction of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: float
        """

        self._average_prediction = average_prediction

    @property
    def num_inputs(self):
        """Gets the num_inputs of this TestrunresultTestRunMetrics.  # noqa: E501

        The number of inputs. For tabular data, an input is one row.  # noqa: E501

        :return: The num_inputs of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: str
        """
        return self._num_inputs

    @num_inputs.setter
    def num_inputs(self, num_inputs):
        """Sets the num_inputs of this TestrunresultTestRunMetrics.

        The number of inputs. For tabular data, an input is one row.  # noqa: E501

        :param num_inputs: The num_inputs of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: str
        """

        self._num_inputs = num_inputs

    @property
    def num_failing_inputs(self):
        """Gets the num_failing_inputs of this TestrunresultTestRunMetrics.  # noqa: E501

        The number of failing inputs.  # noqa: E501

        :return: The num_failing_inputs of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: str
        """
        return self._num_failing_inputs

    @num_failing_inputs.setter
    def num_failing_inputs(self, num_failing_inputs):
        """Sets the num_failing_inputs of this TestrunresultTestRunMetrics.

        The number of failing inputs.  # noqa: E501

        :param num_failing_inputs: The num_failing_inputs of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: str
        """

        self._num_failing_inputs = num_failing_inputs

    @property
    def duration_millis(self):
        """Gets the duration_millis of this TestrunresultTestRunMetrics.  # noqa: E501

        The duration of the test run in milliseconds.  # noqa: E501

        :return: The duration_millis of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: str
        """
        return self._duration_millis

    @duration_millis.setter
    def duration_millis(self, duration_millis):
        """Sets the duration_millis of this TestrunresultTestRunMetrics.

        The duration of the test run in milliseconds.  # noqa: E501

        :param duration_millis: The duration_millis of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: str
        """

        self._duration_millis = duration_millis

    @property
    def severity_counts(self):
        """Gets the severity_counts of this TestrunresultTestRunMetrics.  # noqa: E501


        :return: The severity_counts of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: RimeSeverityCounts
        """
        return self._severity_counts

    @severity_counts.setter
    def severity_counts(self, severity_counts):
        """Sets the severity_counts of this TestrunresultTestRunMetrics.


        :param severity_counts: The severity_counts of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: RimeSeverityCounts
        """

        self._severity_counts = severity_counts

    @property
    def summary_counts(self):
        """Gets the summary_counts of this TestrunresultTestRunMetrics.  # noqa: E501


        :return: The summary_counts of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: TestrunresultResultSummaryCounts
        """
        return self._summary_counts

    @summary_counts.setter
    def summary_counts(self, summary_counts):
        """Sets the summary_counts of this TestrunresultTestRunMetrics.


        :param summary_counts: The summary_counts of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: TestrunresultResultSummaryCounts
        """

        self._summary_counts = summary_counts

    @property
    def category_summary_metrics(self):
        """Gets the category_summary_metrics of this TestrunresultTestRunMetrics.  # noqa: E501

        The list of category summary metrics.  # noqa: E501

        :return: The category_summary_metrics of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: list[TestRunMetricsCategorySummaryMetric]
        """
        return self._category_summary_metrics

    @category_summary_metrics.setter
    def category_summary_metrics(self, category_summary_metrics):
        """Sets the category_summary_metrics of this TestrunresultTestRunMetrics.

        The list of category summary metrics.  # noqa: E501

        :param category_summary_metrics: The category_summary_metrics of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: list[TestRunMetricsCategorySummaryMetric]
        """

        self._category_summary_metrics = category_summary_metrics

    @property
    def risk_scores(self):
        """Gets the risk_scores of this TestrunresultTestRunMetrics.  # noqa: E501

        The list of risk scores.  # noqa: E501

        :return: The risk_scores of this TestrunresultTestRunMetrics.  # noqa: E501
        :rtype: list[RiskscoreRiskScore]
        """
        return self._risk_scores

    @risk_scores.setter
    def risk_scores(self, risk_scores):
        """Sets the risk_scores of this TestrunresultTestRunMetrics.

        The list of risk scores.  # noqa: E501

        :param risk_scores: The risk_scores of this TestrunresultTestRunMetrics.  # noqa: E501
        :type: list[RiskscoreRiskScore]
        """

        self._risk_scores = risk_scores

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
        if issubclass(TestrunresultTestRunMetrics, dict):
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
        if not isinstance(other, TestrunresultTestRunMetrics):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
