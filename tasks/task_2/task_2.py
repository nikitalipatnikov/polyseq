import matplotlib.pyplot as plt
from polyseq.generators import *
from polyseq.visualization import *
import itertools

def main():
    square_seq = gen_reg_polygon_seq(n_sides=4, step=2, l=4)
    triang_seq = map(lambda p: tr_translate(p, dx=0, dy=7), gen_reg_polygon_seq(n_sides=3, n_figs=11, step=0.3, l=5))
    hex_seq = map(lambda p: tr_translate(p, dx=0, dy=-8), gen_reg_polygon_seq(n_sides=6, n_figs=10, l=3))
    dodec_seq = gen_reg_polygon_seq(n_sides=12, step=10, l=80)
    random_seq = gen_random_polygon_seq(n_figs=6)

    ax = visualize(square_seq, 0, 11) # инициализируем новые Figure и Axes, остальное далее рисуем там же, передавая ax=ax
    visualize(triang_seq, 0, 11, ax=ax, cmap='viridis', alpha=0.5)
    visualize(hex_seq, 0, 10, ax=ax, fill=False, cmap='seismic')
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_2/fig1')
    plt.close()

    visualize(dodec_seq, 0, 3, grid=True, alpha=1.0, edgecolor='royalblue', facecolor='cornflowerblue')
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_2/fig2')
    plt.close()

    visualize(random_seq, 0, 5)
    plt.savefig('/Users/nikitalipatnikov/PycharmProjects/polyseq/tasks/task_2/fig3')

if __name__ == '__main__':
    main()