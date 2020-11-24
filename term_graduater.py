from food import Food
import random

class Graduater:

    def __init__(self, offset: int):
        self.offset = offset

        self.T_n = Food(60, 0)
        self.T_s = Food(9, 0)
        self.T_w = Food(60, 0)
        self.P = Food(60, 0)
        for _, attr in self.__dict__.items():
            attr.x = random.randint(attr.l_i, attr.u_i+1)
        self.I = Food(min(self.T_w.x, 2*self.P.x), 0)
        self.I.x = random.randint(self.I.l_i, self.I.u_i)

    def _

if __name__ == "__main__":

    graduater = Graduater(3)
    print("")