from rules.custom_rules import ConsecutiveDaysShiftRule, MorningShiftRule, DaysOffShiftRule, EveningShiftRule, \
    NightShiftRule
from rules_engine.rules.conditional_rules import And, Or

CONSECUTIVE_DAYS_SHIFT_RULE = ConsecutiveDaysShiftRule(1, 'Consecutive Days Shift Rule Check', conditional_rules=None)
DAYS_OFF_SHIFT_RULE = DaysOffShiftRule(2, 'Days Off Shift Rule', conditional_rules=None)
CAN_DO_SHIFT_RULE = And(3, 'Consecutive Days Shift Rule Check', CONSECUTIVE_DAYS_SHIFT_RULE, DAYS_OFF_SHIFT_RULE)
MORNING_SHIFT_RULE = MorningShiftRule(4, 'Morning Shift Rule Check', conditional_rules=None)
EVENING_SHIFT_RULE = EveningShiftRule(5, 'Evening Shift Rule Check', conditional_rules=None)
NIGHT_SHIFT_RULE = NightShiftRule(6, 'Night Shift Rule Check', conditional_rules=None)
