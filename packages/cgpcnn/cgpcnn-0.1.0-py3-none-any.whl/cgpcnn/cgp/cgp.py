import time
import numpy as np
import math
import matplotlib.pyplot as plt
from ..cgp.individual import Individual
import os


class CGP:
    def __init__(self, net_info, eval_func, lam, imgSize, verbose, logger, result_folder_path):
        self.lam = lam
        self.pop = [Individual(net_info, False) for _ in range(1 + self.lam)]
        self.eval_func = eval_func
        self.num_gen = 0
        self.num_eval = 0
        self.max_pool_num = int(math.log2(imgSize) - 2)
        self.logger = logger
        self.best_accuracy = -float('inf')
        self.verbose = verbose
        self.result_folder_path = result_folder_path
        self.history = []

        os.makedirs(self.result_folder_path, exist_ok=True)

    def _evaluation(self, pop, eval_flag):
        net_lists = [pop[i].active_net_list() for i in np.where(eval_flag)[0]]
        fp = self.eval_func(net_lists)
        for i, j in enumerate(np.where(eval_flag)[0]):
            pop[j].eval = fp[i]
        return np.array([ind.eval for ind in pop])

    def modified_evolution(self, max_eval, mutation_rate):
        start_time = time.time()
        eval_flag = np.empty(self.lam)
        active_num = self.pop[0].count_active_node()
        _, pool_num = self.pop[0].check_pool()

        while active_num < self.pop[0].net_info.min_active_num or pool_num > self.max_pool_num:
            self.pop[0].mutation(1.0)
            active_num = self.pop[0].count_active_node()
            _, pool_num = self.pop[0].check_pool()

        evaluations = self._evaluation([self.pop[0]], np.array([True]))
        self.history.append(evaluations[evaluations.argmax()])

        while self.num_gen < max_eval:
            self.num_gen += 1
            for i in range(self.lam):
                eval_flag[i] = False
                self.pop[i + 1].copy(self.pop[0])
                active_num = self.pop[i + 1].count_active_node()
                _, pool_num = self.pop[i + 1].check_pool()
                while not eval_flag[i] or active_num < self.pop[i + 1].net_info.min_active_num or pool_num > self.max_pool_num:
                    self.pop[i + 1].copy(self.pop[0])
                    eval_flag[i] = self.pop[i + 1].mutation(mutation_rate)
                    active_num = self.pop[i + 1].count_active_node()
                    _, pool_num = self.pop[i + 1].check_pool()

            evaluations = self._evaluation(self.pop[1:], eval_flag=eval_flag)
            best_arg = evaluations.argmax()
            best_accuracy = evaluations[best_arg]

            if best_accuracy > self.best_accuracy:
                self.best_accuracy = best_accuracy
                self.best_model = self.pop[best_arg + 1]

            if evaluations[best_arg] > self.pop[0].eval:
                self.pop[0].copy(self.pop[best_arg + 1])
            else:
                self.pop[0].neutral_mutation(mutation_rate)

            self.history.append(self.best_accuracy)

            if self.verbose:
                self.logger.info(f'Generation {self.num_gen}: Best Model Accuracy = {best_accuracy:.4f} History: {self.history}')
                plt.plot(self.history)
                plt.xlabel('Generations')
                plt.ylabel('Best Fitness')
                plt.savefig(os.path.join(self.result_folder_path, f'generation_fitness_plot.png'))

        if self.verbose:
            total_time = time.time() - start_time
            self.logger.info(f'Total Evolution Time: {total_time:.2f} seconds')

        return self.best_model, self.best_accuracy, self.history
