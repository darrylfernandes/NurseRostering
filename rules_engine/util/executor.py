class RuleExecutor(object):
    def __init__(self, rule_input):
        """

        :param rule_input:  The Input entity on which the Rule will be applied.
        """
        self.rule_input = rule_input

    def execute(self, rules):
        """

        :param rules: List of Rule objects to be executed
        :return: (bool, str) i.e (Rule Execution Status, Rule Execution Status Reason)
        """
        for rule in rules:
            status, status_reason = rule.execute(self.rule_input)
            if not status:
                return status, status_reason
        return True, "Pass"
