import sys
sys.path.append('.')
from fuzzy_engine import FuzzyFitSystem

engine = FuzzyFitSystem()
result = engine.evaluate(7.0, 3.0, 6.0, 4.0)
print("Evaluation result:", result)

membership = engine.get_membership_values(7.0, 3.0, 6.0, 4.0)
print("Membership values:", membership)

