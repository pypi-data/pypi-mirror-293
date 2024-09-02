
class Visitor:
    def visit_literal(self, expr):
        ...    
    def visit_grouping(self, expr):
        ...
    def visit_unary(self,expr):
        ...
    def visit_binary(self, expr):
        ...

class Expr:
    def accept(self, visitor):
        ...
    
class Literal(Expr):
    def __init__(self, value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_literal(self)
        
class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)
    
class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)