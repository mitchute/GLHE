from glhe.aggregation.static_method import StaticMethod
from glhe.aggregation.dynamic_method import DynamicMethod

if __name__ == '__main__':
    d1 = DynamicMethod()
    d1.add_load(1, 1)

    d2 = StaticMethod(min_bin_nums=[4, 4, 4], bin_widths=[1, 2, 4])
    d2.add_load(1, 1)
    d2.add_load(2, 1)
    d2.add_load(3, 1)
    d2.add_load(4, 1)
    d2.add_load(5, 1)
    d2.add_load(6, 1)
    d2.add_load(7, 1)
    d2.add_load(8, 1)
    d2.add_load(9, 1)
    d2.add_load(10, 1)
    d2.add_load(11, 1)
    d2.add_load(12, 1)
    d2.add_load(13, 1)
    d2.add_load(14, 1)
    d2.add_load(15, 1)
