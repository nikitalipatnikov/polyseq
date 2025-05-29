import matplotlib.pyplot as plt
from matplotlib.pyplot import viridis
from polyseq.generators import *
from polyseq.transformers import *
from polyseq.visualization import *

import itertools

def main():
    #-----три параллельных «ленты» из последовательностей полигонов, расположенных под острым углом к оси абсцисс-----
    seq1 = map(lambda p: tr_rotate(p, 38), gen_reg_polygon_seq(n_sides=4, step=0.75, l=3))
    seq_1_1, seq_1_2, seq_1_3 = itertools.tee(seq1, 3)

    ax1 = visualize(seq_1_1, 0, 10, edgecolor='indigo', fill=False)
    visualize(map(lambda p: tr_translate(p, dx=-4, dy=4), seq_1_2), 0, 10, ax=ax1, edgecolor='rebeccapurple', fill=False)
    visualize(map(lambda p: tr_translate(p, dx=4, dy=-4), seq_1_3), 0, 10, ax=ax1, edgecolor='mediumorchid', fill=False)
    ax1.grid(alpha=0.2)
    ax1.axhline(0, color='grey', linestyle='--', alpha=0.5)
    ax1.axvline(0, color='grey', linestyle='--', alpha=0.5)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_4/fig1')
    plt.close()

    #-----две пересекающихся «ленты» из последовательностей полигонов, пересекающихся не в начале координат-----
    seq_2_1, seq_2_2 = itertools.tee(gen_reg_polygon_seq(n_sides=4, l=5), 2)
    ax2 = visualize(map(lambda p: tr_rotate(tr_translate(p, dx=-10, dy=-20), 45), seq_2_1), 0, 15)
    visualize(map(lambda p: tr_rotate(tr_translate(p, dx=0, dy=0), -45), seq_2_2), 0, 10, ax=ax2)
    ax2.grid(alpha=0.2)
    ax2.axhline(0, color='grey', linestyle='--', alpha=0.5)
    ax2.axvline(0, color='grey', linestyle='--', alpha=0.5)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_4/fig2')
    plt.close()

    #-----две параллельных ленты треугольников, ориентированных симметрично друг к другу-----
    seq_3_1, seq_3_2 = itertools.tee(gen_reg_polygon_seq(n_sides=3), 2)
    ax3 = visualize(map(lambda p: tr_translate(p, dx=-6, dy=0.5), seq_3_1), 0, 7, fill=False)
    visualize(map(lambda p: tr_translate(tr_symmetry(p, axis=0), dx=-6, dy=2), seq_3_2), 0, 7, ax=ax3, fill=False)
    ax3.axhline(0, color='grey', linestyle='--', alpha=0.5)
    ax3.axvline(0, color='grey', linestyle='--', alpha=0.5)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_4/fig3')
    plt.close()

    #-----последовательность четырехугольников в разном масштабе, ограниченных двумя прямыми, пересекающимися в начале координат-----
    seq_4_1, seq_4_2 = itertools.tee(map(lambda p: tr_stretch_plane(p, cy=3), gen_reg_polygon_seq(n_sides=4)), 2)
    scales_1, scales_2 = itertools.tee(map(lambda k: 1.5**k, itertools.count(1)), 2)
    seq_4_1 = map(lambda p, coef: tr_homothety(tr_rotate(p, 45), center=(0,0), k=coef), seq_4_1, scales_1)
    seq_4_2 = map(lambda p, coef: tr_homothety(tr_rotate(p, 225), center=(0,0), k=coef), seq_4_2, scales_2)
    ax4 = visualize(map(lambda p: tr_translate(p, 3,3), seq_4_1), 0, 5)
    visualize(map(lambda p: tr_translate(p, -3,-3), seq_4_2), 0, 5, ax=ax4)
    ax4.grid(alpha=0.2)
    ax4.axhline(0, color='grey', linestyle='--', alpha=0.5)
    ax4.axvline(0, color='grey', linestyle='--', alpha=0.5)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_4/fig4')

if __name__ == '__main__':
    main()
