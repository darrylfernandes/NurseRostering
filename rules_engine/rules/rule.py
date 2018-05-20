import abc


class Rule(abc):

    def __init__(self, rule_id, rule_description):
        """

        :param rule_id: Unique Rule Id
        :param rule_description: Provides the textual description of the Rule
        """
        self.rule_id = rule_id
        self.rule_description = rule_description

    @abc.abstractmethod
    def execute(self, rule_input):
        """

        :param rule_input: The Input entity on which the Rule will be applied.
        :rtype: Should return a tuple i.e (str, boolean, str)
                eg: (rule_id, True, "Pass")  or (rule_id, False, "Failure reason")
        """
        pass

