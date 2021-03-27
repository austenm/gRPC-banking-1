class Calculator():
    def __init__(self, name):
        self.name = name

    def plus(self, num1, num2):
        return num1 + num2

    def minus(self, num1, num2):
        return num1 - num2

    def calculate(self, num1, num2, op):
        if op == 'plus':
            answer = self.plus(num1, num2)
            return answer
        else:
            answer = self.minus(num1, num2)
            return answer


def main():
    c = Calculator('mycalc')

    print('Adding 10 and 15: ')
    plus_answer = c.calculate(10, 15, 'plus')
    print(plus_answer)

    print('Subtracting 31 from 100: ')
    minus_answer = c.calculate(100, 31, 'minus')
    print(minus_answer)


if __name__ == '__main__':
    main()
