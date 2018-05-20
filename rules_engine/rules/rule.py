import abc


class Rule(abc):

    def __init__(self, rule_id):
        """

        :param rule_id: Unique Rule Id
        """
        self.rule_id = rule_id

    @abc.abstractmethod
    def execute(self, rule_input):
        """

        :param rule_input: The Input entity on which the Rule will be applied.
        :rtype: Should return a tuple i.e (boolean, str) eg: (True, "Pass")  or (False, "Failure reason")
        """
        pass

