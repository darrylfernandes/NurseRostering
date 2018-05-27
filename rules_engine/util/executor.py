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
        rule_execution_trace = []
        overall_rule_execution_status = True
        overall_rule_execution_status_reason = 'Pass'
        for rule in rules:
            rule_id, rule_description, status, status_reason, parent_rule_id, parent_rule_description, \
                children_rule_trace = rule.execute(self.rule_input)
            rule_execution_trace.append((rule_id, rule_description, status, status_reason,
                                         parent_rule_id, parent_rule_description, children_rule_trace))
            if not status:
                overall_rule_execution_status = False
                overall_rule_execution_status_reason = 'Fail'

        return overall_rule_execution_status, overall_rule_execution_status_reason, rule_execution_trace
