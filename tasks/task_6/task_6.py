import matplotlib.pyplot as plt
from matplotlib.pyplot import viridis
from polyseq.generators import *
from polyseq.transformers import *
from polyseq.visualization import *
from polyseq.filters import *

import itertools

def main():
    #---------------------------последовательности из 4.4----------------------------
    seq_4 = tuple(map(lambda p: tr_stretch_plane(p, cy=3), gen_reg_polygon_seq(n_sides=4, n_figs=6)))
    scales = tuple(map(lambda k: 1.5 ** k, itertools.count(1)))
    seq_4_1 = map(lambda p, coef: tr_homothety(tr_rotate(p, 45), center=(0, 0), k=coef), seq_4, scales)
    seq_4_2 = map(lambda p, coef: tr_homothety(tr_rotate(p, 225), center=(0, 0), k=coef), seq_4, scales)
    # -------------------------------------------------------------------------------


    seq_4_1_1 = filter(lambda p: flt_area_lt(p, 40), seq_4_1)
    seq_4_2_2 = filter(lambda p: flt_area_lt(p, 100), seq_4_2)  # формально 7 фигур, но две совпадают, поэтому визуально их 6
    ax1 = visualize(seq_4_1_1, start=0,stop=None)
    visualize(seq_4_2_2, start=0, stop=None, ax=ax1)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_6/filtered_4_4')
    plt.close()


    random.seed(42) # для воспроизводимости
    seq_6 = tuple(itertools.chain(map(lambda p: tr_translate(p, 15, 15),
                                    gen_reg_polygon_seq(n_sides=3, n_figs=1, l=5)),
                                gen_reg_polygon_seq(n_sides=4, n_figs=5, l=20,),
                                gen_random_polygon_seq(n_figs=7)))
    visualize(seq_6, start=0, stop=None)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_6/unfiltered_15_figs')
    plt.close()

    filtered = filter(lambda p: flt_shortest_side_lt(p, 3), seq)
    visualize(filtered, start=0, stop=None)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_6/filtered_4_figs')
    plt.close()


    seq_6_1 = tuple(map(lambda p: tr_stretch_plane(p, cy=10), gen_reg_polygon_seq(n_sides=4, n_figs = 30, l=1)))
    seq_6_2 = itertools.chain(seq_6_1, map(lambda p: tr_translate(p, 20.5, 5), seq_6_1))
    visualize(seq_6_2, 0, None)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_6/intersections')


if __name__ == '__main__':
    main()
