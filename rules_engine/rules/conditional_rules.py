from .rule import Rule


class And(Rule):
    def __init__(self, rule_id, lhs, rhs):
        """

        :param rule_id: Unique Rule Id
        :param lhs: Left Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule1 is lhs rule)
        :param rhs: Right Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule2 is rhs rule)
        """
        super(And, self).__init__(rule_id)
        self.lhs = lhs
        self.rhs = rhs

    def execute(self, rule_input):
        if (self.lhs and isinstance(self.lhs, Rule)) and (self.rhs and isinstance(self.rhs, Rule)):
            return self.lhs.execute(rule_input) and self.rhs.execute(rule_input), "Pass"
        else:
            return False, "The left-hand/right-hand side should be of type Rule. " \
                          "Kindly validate the Rule Config input for Rule Id {} and try again".format(self.rule_id)


class Or(Rule):
    def __init__(self, rule_id, lhs, rhs):
        """

        :param rule_id: Unique Rule Id
        :param lhs: Left Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule1 is lhs rule)
        :param rhs: Right Hand Side Rule in the AND operation eg:  (rule1 and rule2 where rule2 is rhs rule)
        """
        super(And, self).__init__(rule_id)
        self.lhs = lhs
        self.rhs = rhs

    def execute(self, rule_input):
        if (self.lhs and isinstance(self.lhs, Rule)) and (self.rhs and isinstance(self.rhs, Rule)):
            return self.lhs.execute(rule_input) or self.rhs.execute(rule_input), "Pass"
        else:
            return False, "The left-hand/right-hand side should be of type Rule. " \
                          "Kindly validate the Rule Config input for Rule Id {} and try again".format(self.rule_id)