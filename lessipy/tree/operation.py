from lessipy.tree.operand import Operand


class Operation(Operand):
    """An operator class for variable operation."""

    __slots__ = "lval", "rval", "_result"

    def __new__(cls, operation):
        if cls is not Operation:
            unit = operation[0].unify(operation[1])
            cls.lval, cls.rval = operation
            cls._result = None
            return cls
        lval = operation[0]
        rval = operation[2]
        operator = operation[1]
        if operator == "+":
            return Addition([lval, rval])
        elif operator == "-":
            return Subtraction([lval, rval])
        elif operator == "*":
            return Multiplication([lval, rval])
        elif operator == "/":
            return Division([lval, rval])
        raise ArithmeticError(repr(operator) + " is unsupported operation")


class Addition(Operation):
    """Do add."""
    
    @property
    def value(self):
        if self._result:
            return self._result
        self._result = self.lval.value + self.rval.value
        return self._result


class Subtraction(Operation):
    """Do subtract."""

    @property
    def value(self):
        if self._result:
            return self._result
        self._result = self.lval.value - self.rval.value
        return self._result


class Multiplication(Operation):
    """Do multiply."""

    @property
    def value(self):
        if self._result:
            return self._result
        self._result = self.lval.value * self.rval.value
        return self._result

class Division(Operation):
    """Do devide."""

    @property
    def value(self):
        if self._result:
            return self._result
        self._result = self.lval.value / self.rval.value
        return self._result
