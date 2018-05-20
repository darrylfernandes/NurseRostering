import abc


class Rule(abc):

    def __init__(self, rule_id):
        self.rule_id = rule_id

    @abc.abstractmethod
    def execute(self, rule_input):
        """

        :param rule_input: The Input entity on which the Rule will be applied.
        :rtype: Will return boolean i.e True/False
        """
        pass

