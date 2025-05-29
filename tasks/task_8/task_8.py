from polyseq.generators import *
from polyseq.transformers import *
from polyseq.aggregates import *

import math
import itertools

def main():
    #-----расстояние до ближайшей точки-----
    seq_1 = map(lambda p: tr_translate(p, 4, 5), gen_reg_polygon_seq(n_sides=4, n_figs=5, l=2))
    dist = agr_origin_nearest(seq_1)

    assert math.isclose(dist, 5)

    #-----максимальная длина стороны-----
    seq_2 = itertools.chain(gen_reg_polygon_seq(n_sides=3, n_figs=1, l=1),
                            gen_reg_polygon_seq(n_sides=3, n_figs=1, l=2),
                            gen_reg_polygon_seq(n_sides=3, n_figs=1, l=3),
                            gen_reg_polygon_seq(n_sides=3, n_figs=1, l=4))
    max_side = agr_max_side(seq_2)

    assert math.isclose(max_side, 4)

    #-----минимальная площадь-----
    seq_3 = itertools.chain(gen_reg_polygon_seq(n_sides=4, n_figs=1, l=2),
                            gen_reg_polygon_seq(n_sides=4, n_figs=1, l=5),
                            gen_reg_polygon_seq(n_sides=4, n_figs=1, l=15),
                            gen_reg_polygon_seq(n_sides=4, n_figs=1, l=110))

    min_area = agr_min_area(seq_3)
    assert math.isclose(min_area, 4)

    #-----суммарный периметр-----
    seq4 = gen_reg_polygon_seq(n_sides=12, n_figs=2, l=2)
    agr_per = agr_perimeter(seq4)

    assert math.isclose(agr_per, 48)

    #-----суммарная площадь-----
    seq5 = gen_reg_polygon_seq(n_sides=4, n_figs=3, l=1)
    agr_ar = agr_area(seq5)

    assert math.isclose(agr_ar, 3)


if __name__ == '__main__':
    main()