just_len = 60

import re
import collections


NUM     = r'(?P<NUM>\d+)'
PLUS    = r'(?P<PLUS>\+)'
MINUS   = r'(?P<MINUS>-)'
TIMES   = r'(?P<TIMES>\*)'
DIVIDE  = r'(?P<DIVIDE>/)'
POWER   =  r'(?P<POWER>\^)'
LPAREN  = r'(?P<LPAREN>\()'
RPAREN  = r'(?P<RPAREN>\))'
WS      = r'(?P<WS>\s+)'

master_pattern = re.compile('|'.join((NUM, PLUS, MINUS, TIMES, DIVIDE, POWER, LPAREN, RPAREN, WS)))
Token = collections.namedtuple('Token', ['type', 'value'])


def generate_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())

        if token.type != 'WS':
            yield token


class ExpressionEvaluator:

    def parse(self, text):
        self.tokens = generate_tokens(master_pattern, text)
        self.current_token = None
        self.next_token = None
        self._advance()

        return self.expr()

    def _advance(self):
        self.current_token, self.next_token = self.next_token, next(self.tokens, None)

    def _accept(self, token_type):

        if self.next_token and self.next_token.type == token_type:
            self._advance()
            return True
        else:
            return False

    def _expect(self, token_type):
        if not self._accept(token_type):
            raise SyntaxError('Error')

    def expr(self):

        expr_value = self.term()

        while self._accept('PLUS') or self._accept('MINUS'):

            op = self.current_token.type

            right = self.term()
            if op == 'PLUS':
                expr_value += right
            elif op == 'MINUS':
                expr_value -= right
            else:
                raise SyntaxError('Error')

        return expr_value

    def term(self):

        term_value = self.factor()

        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.current_token.type

            if op == 'TIMES':
                term_value *= self.factor()
            elif op == 'DIVIDE':
                term_value /= self.factor()
            else:
                raise SyntaxError('Error')

        return term_value

    def factor(self):
        value_factor = self.end()

        while self._accept('POWER'):
            op = self.current_token.type
            if op == 'POWER':
                value_factor **= self.end()
            else:
                raise SyntaxError('Error')
        return value_factor


    def end(self):
        if self._accept('NUM'):
            return int(self.current_token.value)
        elif self._accept('LPAREN'):
            expr_value = self.expr()
            self._expect('RPAREN')
            return expr_value
        else:
            raise SyntaxError('Error')


e = ExpressionEvaluator()
print('parse 2'.ljust(just_len),
      e.parse('2'))

print('parse 2 + 3'.ljust(just_len),
      e.parse('2 + 3'))
print('parse 2 + 3 * 4'.ljust(just_len),
      e.parse('2 + 3 * 4'))

print('parse 2 + 3 ^ 4'.ljust(just_len),
      e.parse('2 + 3 ^ 4'))


print('parse (2 + 3) * 4'.ljust(just_len),
      e.parse('(2 + 3) * 4'))

print('parse (2 + 3) ^ 4'.ljust(just_len),
      e.parse('(2 + 3) ^ 4'))
