from rules_engine.rules.rule import Rule, wrap_rule_exception


class And(Rule):
    def __init__(self, rule_id, rule_description, lhs, rhs):
        """

        :param rule_id: Unique Rule Id
        :param rule_description: Rule Description
        :param lhs: Left Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule1 is lhs rule)
        :param rhs: Right Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule2 is rhs rule)
        """
        super(And, self).__init__(rule_id, rule_description, conditional_rules=None)
        self.lhs = lhs
        self.rhs = rhs

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        parent_rule_id = parent_rule.rule_id if parent_rule else None
        parent_rule_description = parent_rule.rule_description if parent_rule else None

        if (self.lhs and isinstance(self.lhs, Rule)) and (self.rhs and isinstance(self.rhs, Rule)):
            lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason, lhs_parent_rule_id, \
                lhs_parent_rule_description, lhs_child_rules = self.lhs.execute(rule_input, parent_rule=self)
            rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason, rhs_parent_rule_id, \
                rhs_parent_rule_description, rhs_child_rules = self.rhs.execute(rule_input, parent_rule=self)
            overall_status = lhs_rule_status and rhs_rule_status
            if overall_status:
                return self.rule_id, self.rule_description, True, "Pass", \
                           parent_rule_id, parent_rule_description, \
                           [(lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason,
                             lhs_parent_rule_id, lhs_parent_rule_description, lhs_child_rules),
                            (rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason,
                             rhs_parent_rule_id, rhs_parent_rule_description, rhs_child_rules)]
            else:
                return self.rule_id, self.rule_description, False, "Fail", \
                       parent_rule_id, parent_rule_description, \
                       [(lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason,
                         lhs_parent_rule_id, lhs_parent_rule_description, lhs_child_rules),
                        (rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason,
                         rhs_parent_rule_id, rhs_parent_rule_description, rhs_child_rules)]
        else:
            return self.rule_id, self.rule_description, False, \
                   "The left-hand/right-hand side should be of type Rule. " \
                   "Kindly validate the Rule Config input for Rule Id {} and try again".format(self.rule_id), \
                   parent_rule_id, parent_rule_description, []


class Or(Rule):
    def __init__(self, rule_id, rule_description, lhs, rhs):
        """

        :param rule_id: Unique Rule Id
        :param rule_description: Rule Description
        :param lhs: Left Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule1 is lhs rule)
        :param rhs: Right Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule2 is rhs rule)
        """
        super(Or, self).__init__(rule_id, rule_description, conditional_rules=None)
        self.lhs = lhs
        self.rhs = rhs

    @wrap_rule_exception
    def execute(self, rule_input, parent_rule=None):
        parent_rule_id = parent_rule.rule_id if parent_rule else None
        parent_rule_description = parent_rule.rule_description if parent_rule else None

        if (self.lhs and isinstance(self.lhs, Rule)) and (self.rhs and isinstance(self.rhs, Rule)):
            lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason, lhs_parent_rule_id, \
                lhs_parent_rule_description, lhs_child_rules = self.lhs.execute(rule_input, parent_rule=self)
            rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason, rhs_parent_rule_id, \
                rhs_parent_rule_description, rhs_child_rules = self.rhs.execute(rule_input, parent_rule=self)
            overall_status = lhs_rule_status or rhs_rule_status
            if overall_status:
                return self.rule_id, self.rule_description, True, "Pass", \
                       parent_rule_id, parent_rule_description, \
                       [(lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason,
                         lhs_parent_rule_id, lhs_parent_rule_description, lhs_child_rules),
                        (rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason,
                         rhs_parent_rule_id, rhs_parent_rule_description, rhs_child_rules)]
            else:
                return self.rule_id, self.rule_description, False, "Fail", \
                       parent_rule_id, parent_rule_description, \
                       [(lhs_rule_id, lhs_rule_description, lhs_rule_status, lhs_rule_status_reason,
                         lhs_parent_rule_id, lhs_parent_rule_description, lhs_child_rules),
                        (rhs_rule_id, rhs_rule_description, rhs_rule_status, rhs_rule_status_reason,
                         rhs_parent_rule_id, rhs_parent_rule_description, rhs_child_rules)]
        else:
            return self.rule_id, self.rule_description, False, \
                   "The left-hand/right-hand side should be of type Rule. " \
                   "Kindly validate the Rule Config input for Rule Id {} and try again".format(self.rule_id), \
                   parent_rule_id, parent_rule_description, []


