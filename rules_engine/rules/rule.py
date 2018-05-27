from abc import ABC, abstractmethod
import traceback


class RuleException(Exception):
    pass


def wrap_rule_exception(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (RuleException, TypeError, Exception):
            parent_rule_id = kwargs['parent_rule'].rule_id if kwargs.get('parent_rule') else None
            parent_rule_description = kwargs['parent_rule'].rule_description if kwargs.get('parent_rule') else None
            return args[0].rule_id, args[0].rule_description, False, \
                "Exception occurred during the execution of the Rule Id {} :- {}"\
                .format(args[0].rule_id, traceback.format_exc()), parent_rule_id, parent_rule_description, []
    return wrapper


class Rule(ABC):

    def __init__(self, rule_id, rule_description, conditional_rules=None):
        """

        :param rule_id: Unique Rule Id
        :param rule_description: Provides the textual description of the Rule
        :param conditional_rules: List of pre-conditions to be satisfied prior to execution of this Rule
        """
        self.rule_id = rule_id
        self.rule_description = rule_description
        self.conditional_rules = conditional_rules

    @abstractmethod
    @wrap_rule_exception
    def execute(self, rule_input):
        """

        :param rule_input: The Input entity on which the Rule will be applied.
        :rtype: Should return a tuple i.e (str, boolean, str, str/NoneType)
                eg: (R456, True, "Pass", R123)  or (R124, False, "Failure reason", None)
        """
        pass



