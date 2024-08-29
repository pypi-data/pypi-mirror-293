
class FibonacciGenerator:
    def __init__(self):
        self._cache = {}

    def _fib(self, n):
        return n if n < 2 else self._fib_value(n - 1) + self._fib_value(n - 2)

    def _fib_value(self, n):
        if n not in self._cache:
            self._cache[n] = self._fib(n)
        return self._cache[n]

    def generate(self, n):
        for i in range(n):
            yield self._fib_value(i)


#var generator = new FibonacciGenerator()
#        foreach (var digit in generator.Generate(15))
#        {
#            Console.WriteLine(digit)
#        }