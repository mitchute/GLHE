from loads.bins.dynamic_method import DynamicMethod
from loads.bins.static_method import StaticMethod

if __name__ == '__main__':

    d1 = DynamicMethod()
    d1.add_load(1)

    d2 = StaticMethod(min_bin_nums=[4, 4, 4], bin_widths=[1, 2, 4])
    d2.add_load(1)
    d2.add_load(2)
    d2.add_load(3)
    d2.add_load(4)
    d2.add_load(5)
    d2.add_load(6)
    d2.add_load(7)
    d2.add_load(8)
    d2.add_load(9)
    d2.add_load(10)
    d2.add_load(11)
    d2.add_load(12)
    d2.add_load(13)
    d2.add_load(14)
    d2.add_load(15)

