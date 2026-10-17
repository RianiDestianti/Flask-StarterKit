import re

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class ValidationErrors:
    def __init__(self):
        self.errors = {}

    def add(self, field, message):
        self.errors.setdefault(field, []).append(message)

    def all(self):
        return self.errors


class Validator:
    """
    Validator dengan gaya validatorjs:

        validation = Validator(body, { 'email' : 'required|email', 'password' : 'required|min:6' })
        if validation.fails():
            validation.errors.all()

    Rule: required, email, min, max, numeric, string, in
    """

    def __init__(self, body, rules):
        self.body   = body or {}
        self.rules  = rules
        self.errors = ValidationErrors()

    def fails(self):
        return not self.passes()

    def passes(self):
        self.errors = ValidationErrors()

        for field, rule in self.rules.items():
            value = self.body.get(field)
            items = [item for item in rule.split('|') if item]
            label = field.replace('_', ' ')

            if self._is_empty(value):
                if 'required' in items:
                    self.errors.add(field, f"The {label} field is required.")
                continue

            numeric = 'numeric' in items or (isinstance(value, (int, float)) and not isinstance(value, bool))

            for item in items:
                name, _, param = item.partition(':')

                if name == 'email' and not EMAIL_REGEX.match(str(value)):
                    self.errors.add(field, f"The {label} format is invalid.")

                elif name == 'numeric' and not self._is_number(value):
                    self.errors.add(field, f"The {label} must be a number.")

                elif name == 'string' and not isinstance(value, str):
                    self.errors.add(field, f"The {label} must be a string.")

                elif name == 'in' and str(value) not in param.split(','):
                    self.errors.add(field, f"The selected {label} is invalid.")

                elif name == 'min':
                    if numeric and self._is_number(value) and float(value) < float(param):
                        self.errors.add(field, f"The {label} must be at least {param}.")
                    elif not numeric and len(str(value)) < int(param):
                        self.errors.add(field, f"The {label} must be at least {param} characters.")

                elif name == 'max':
                    if numeric and self._is_number(value) and float(value) > float(param):
                        self.errors.add(field, f"The {label} may not be greater than {param}.")
                    elif not numeric and len(str(value)) > int(param):
                        self.errors.add(field, f"The {label} may not be greater than {param} characters.")

        return not self.errors.all()

    @staticmethod
    def _is_empty(value):
        return value is None or value == [] or (isinstance(value, str) and value.strip() == '')

    @staticmethod
    def _is_number(value):
        try:
            float(value)
            return not isinstance(value, bool)
        except (TypeError, ValueError):
            return False
