import math


class VergiKimlik:

    @staticmethod
    def Dogrula(vkn):

        if len(vkn) != 10:


            return False
        x = [0 for _ in range(9)]
        y = [0 for _ in range(9)]

        for i in range(0, 9):
            x[i] = math.fmod((int.Parse(str(vkn[i])) + 9 - i), 10)

            y[i] = math.fmod((x[i] * int(2 ** (9 - i))), 9)

            if x[i] != 0 and y[i] == 0:
                y[i] = 9

        return (math.fmod((10 - (math.fmod(y.Sum(), 10))), 10)) == int.Parse(str(vkn[9]))
