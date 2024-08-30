import numpy as np


class Individual:
    def __init__(self, net_info, init):
        self.net_info = net_info
        self.gene = np.zeros((self.net_info.node_num + self.net_info.out_num, self.net_info.max_in_num + 1), dtype=int)
        self.is_active = np.empty(self.net_info.node_num + self.net_info.out_num, dtype=bool)
        self.eval = None
        if init:
            print('Initializing with specific architectures...')
            self.init_gene_with_conv()
        else:
            self.init_gene()

    def init_gene_with_conv(self):
        arch = ['S_ConvBlock_64_3']
        input_layer_num = int(self.net_info.input_num / self.net_info.rows) + 1
        output_layer_num = int(self.net_info.out_num / self.net_info.rows) + 1
        layer_ids = [(self.net_info.cols - 1 - input_layer_num - output_layer_num + i) // len(arch) for i in range(len(arch))]
        prev_id, current_layer = 0, input_layer_num
        block_ids = []

        for i, idx in enumerate(layer_ids):
            current_layer += idx
            n = current_layer * self.net_info.rows + np.random.randint(self.net_info.rows)
            block_ids.append(n)
            self.gene[n][0] = self.net_info.func_type.index(arch[i])
            col = min(n // self.net_info.rows, self.net_info.cols)
            max_connect_id = col * self.net_info.rows + self.net_info.input_num
            min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)

            self.gene[n][1] = prev_id
            for j in range(1, self.net_info.max_in_num):
                self.gene[n][j + 1] = min_connect_id + np.random.randint(max_connect_id - min_connect_id)

            prev_id = n + self.net_info.input_num

        self.init_output_layer(block_ids, prev_id)
        self.init_intermediate_nodes(block_ids)

    def init_output_layer(self, block_ids, prev_id):
        n = self.net_info.node_num
        type_num = self.net_info.func_type_num if n < self.net_info.node_num else self.net_info.out_type_num
        self.gene[n][0] = np.random.randint(type_num)
        col = min(n // self.net_info.rows, self.net_info.cols)
        max_connect_id = col * self.net_info.rows + self.net_info.input_num
        min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)

        self.gene[n][1] = prev_id
        for i in range(1, self.net_info.max_in_num):
            self.gene[n][i + 1] = min_connect_id + np.random.randint(max_connect_id - min_connect_id)

        block_ids.append(n)

    def init_intermediate_nodes(self, block_ids):
        for n in range(self.net_info.node_num + self.net_info.out_num):
            if n in block_ids:
                continue

            type_num = self.net_info.func_type_num if n < self.net_info.node_num else self.net_info.out_type_num
            self.gene[n][0] = np.random.randint(type_num)
            col = min(n // self.net_info.rows, self.net_info.cols)
            max_connect_id = col * self.net_info.rows + self.net_info.input_num
            min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)

            for i in range(self.net_info.max_in_num):
                self.gene[n][i + 1] = min_connect_id + np.random.randint(max_connect_id - min_connect_id)

        self.check_active()

    def init_gene(self):
        for n in range(self.net_info.node_num + self.net_info.out_num):
            type_num = self.net_info.func_type_num if n < self.net_info.node_num else self.net_info.out_type_num
            self.gene[n][0] = np.random.randint(type_num)
            col = min(n // self.net_info.rows, self.net_info.cols)
            max_connect_id = col * self.net_info.rows + self.net_info.input_num
            min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)

            for i in range(self.net_info.max_in_num):
                self.gene[n][i + 1] = min_connect_id + np.random.randint(max_connect_id - min_connect_id)

        self.check_active()

    def __check_course_to_out(self, n):
        if not self.is_active[n]:
            self.is_active[n] = True
            t = self.gene[n][0]
            in_num = self.net_info.out_in_num[t] if n >= self.net_info.node_num else self.net_info.func_in_num[t]

            for i in range(in_num):
                if self.gene[n][i + 1] >= self.net_info.input_num:
                    self.__check_course_to_out(self.gene[n][i + 1] - self.net_info.input_num)

    def check_active(self):
        self.is_active[:] = False
        for n in range(self.net_info.out_num):
            self.__check_course_to_out(self.net_info.node_num + n)

    def check_pool(self):
        pool_num = sum(1 for n in range(self.net_info.node_num + self.net_info.out_num) if self.is_active[n] and self.gene[n][0] > 19)
        return pool_num == 0, pool_num

    def __mutate(self, current, min_int, max_int):
        mutated_gene = current
        while current == mutated_gene:
            mutated_gene = min_int + np.random.randint(max_int - min_int)
        return mutated_gene

    def mutation(self, mutation_rate=0.01):
        active_check = False
        for n in range(self.net_info.node_num + self.net_info.out_num):
            t = self.gene[n][0]
            type_num = self.net_info.func_type_num if n < self.net_info.node_num else self.net_info.out_type_num
            if np.random.rand() < mutation_rate and type_num > 1:
                self.gene[n][0] = self.__mutate(self.gene[n][0], 0, type_num)
                if self.is_active[n]:
                    active_check = True

            col = min(n // self.net_info.rows, self.net_info.cols)
            max_connect_id = col * self.net_info.rows + self.net_info.input_num
            min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)
            in_num = self.net_info.func_in_num[t] if n < self.net_info.node_num else self.net_info.out_in_num[t]

            for i in range(self.net_info.max_in_num):
                if np.random.rand() < mutation_rate and max_connect_id - min_connect_id > 1:
                    self.gene[n][i + 1] = self.__mutate(self.gene[n][i + 1], min_connect_id, max_connect_id)
                    if self.is_active[n] and i < in_num:
                        active_check = True

        self.check_active()
        return active_check

    def neutral_mutation(self, mutation_rate=0.01):
        for n in range(self.net_info.node_num + self.net_info.out_num):
            t = self.gene[n][0]
            type_num = self.net_info.func_type_num if n < self.net_info.node_num else self.net_info.out_type_num
            if not self.is_active[n] and np.random.rand() < mutation_rate and type_num > 1:
                self.gene[n][0] = self.__mutate(self.gene[n][0], 0, type_num)

            col = min(n // self.net_info.rows, self.net_info.cols)
            max_connect_id = col * self.net_info.rows + self.net_info.input_num
            min_connect_id = max(0, (col - self.net_info.level_back) * self.net_info.rows + self.net_info.input_num)
            in_num = self.net_info.func_in_num[t] if n < self.net_info.node_num else self.net_info.out_in_num[t]

            for i in range(self.net_info.max_in_num):
                if (not self.is_active[n] or i >= in_num) and np.random.rand() < mutation_rate and max_connect_id - min_connect_id > 1:
                    self.gene[n][i + 1] = self.__mutate(self.gene[n][i + 1], min_connect_id, max_connect_id)

        self.check_active()

    def count_active_node(self):
        return self.is_active.sum()

    def copy(self, source):
        self.net_info = source.net_info
        self.gene = source.gene.copy()
        self.is_active = source.is_active.copy()
        self.eval = source.eval

    def active_net_list(self):
        net_list = [["input", 0, 0]]
        active_cnt = np.arange(self.net_info.input_num + self.net_info.node_num + self.net_info.out_num)
        active_cnt[self.net_info.input_num:] = np.cumsum(self.is_active)

        for n, is_a in enumerate(self.is_active):
            if is_a:
                t = self.gene[n][0]
                type_str = self.net_info.func_type[t] if n < self.net_info.node_num else self.net_info.out_type[t]
                connections = [active_cnt[self.gene[n][i + 1]] for i in range(self.net_info.max_in_num)]
                net_list.append([type_str] + connections)
        return net_list
