class RuleExecutor(object):
    def __init__(self, rule_input):
        """

        :param rule_input:  The Input entity on which the Rule will be applied.
        """
        self.rule_input = rule_input

    def execute(self, rules):
        """

        :param rules: List of Rule objects to be executed
        :return:    (bool, str, list)
                    i.e (Rule Execution Status, Rule Execution Status Reason, Overall Rule Execution Status)
        """
        rule_execution_status = []
        for rule in rules:
            rule_id, status, status_reason = rule.execute(self.rule_input)
            rule_execution_status.append((rule_id, rule.rule_description, status, status_reason))
            if not status:
                return False, "Fail", rule_execution_status
        return True, "Pass", rule_execution_status
