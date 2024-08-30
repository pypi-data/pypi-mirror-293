import matplotlib.pyplot as plt
import pydot
import matplotlib.animation as animation
from PIL import Image
import io


def plot_images(images, cls_true, cls_pred=None, title=None, label_names=None):
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    if title:
        fig.suptitle(title, size=20)

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i, :, :, :], interpolation='spline16')
        cls_true_name = label_names[int(cls_true[i])]
        xlabel = f"{cls_true_name} ({int(cls_true[i])})"
        if cls_pred is not None:
            cls_pred_name = label_names[int(cls_pred[i])]
            xlabel += f"\nPred: {cls_pred_name}"
        ax.set_xlabel(xlabel)
        ax.set_xticks([])
        ax.set_yticks([])

    plt.show()


def plot_graph(individual, rankdir='TB'):
    graph = pydot.Dot(graph_type='digraph', rankdir=rankdir)
    nodes = {}

    for i in range(individual.net_info.input_num):
        node = pydot.Node(f'input-{i}', label=f'Input {i}', shape='ellipse')
        nodes[i] = node
        graph.add_node(node)

    for idx in range(individual.net_info.node_num + individual.net_info.out_num):
        if individual.is_active[idx]:
            gene_info = individual.gene[idx]
            func_type = individual.net_info.func_type[gene_info[0]] if idx < individual.net_info.node_num else f'Output {idx - individual.net_info.node_num}'
            label = f"{func_type} (Node {idx})"
            node = pydot.Node(f'node-{idx}', label=label, shape='box')
            nodes[idx + individual.net_info.input_num] = node
            graph.add_node(node)

    for idx in range(individual.net_info.node_num + individual.net_info.out_num):
        if individual.is_active[idx]:
            for j in range(1, individual.net_info.max_in_num + 1):
                input_idx = individual.gene[idx][j]
                if input_idx >= 0:
                    edge = pydot.Edge(nodes[input_idx], nodes[idx + individual.net_info.input_num])
                    graph.add_edge(edge)

    png_str = graph.create(prog='dot', format='png')
    image = Image.open(io.BytesIO(png_str))

    return image


def plot_cartesian(individual):
    graph = pydot.Dot(graph_type='digraph')
    nodes = {}

    for i in range(individual.net_info.input_num):
        node = pydot.Node(f'input-{i}', shape='ellipse')
        node.set('pos', f'-1,{i:.2f}!')
        nodes[i] = node
        graph.add_node(node)

    for idx in range(individual.net_info.node_num):
        x = (idx // individual.net_info.rows)
        y = idx % individual.net_info.rows

        node_style = "filled" if individual.is_active[idx] else "filled"
        node_color = '#ff00cc' if individual.is_active[idx] else '#cccccc'
        node = pydot.Node(f'{idx}', label=f'{idx}', style=node_style, shape="circle", fillcolor=node_color)
        node.set('pos', f'{x},{y}!')
        node.set('fontsize', 10)
        nodes[idx + individual.net_info.input_num] = node
        graph.add_node(node)

    for idx in range(individual.net_info.out_num):
        out_idx = individual.net_info.node_num + idx
        node = pydot.Node(f'output-{idx}', label=f'output-{idx}', style="filled", shape="ellipse", fillcolor='#ccaadd')
        node.set('pos', f'{(individual.net_info.cols + 1)},{idx:.2f}!')
        nodes[out_idx + individual.net_info.input_num] = node
        graph.add_node(node)

        for con in range(individual.net_info.max_in_num):
            input_idx = individual.gene[out_idx][con + 1]
            if input_idx in nodes:
                graph.add_edge(pydot.Edge(nodes[input_idx], nodes[out_idx + individual.net_info.input_num]))

    for idx in range(individual.net_info.node_num):
        if individual.is_active[idx]:
            for con in range(individual.net_info.max_in_num):
                input_idx = individual.gene[idx][con + 1]
                if input_idx in nodes:
                    graph.add_edge(pydot.Edge(nodes[input_idx], nodes[idx + individual.net_info.input_num]))

    png_str = graph.create(prog='neato', format='png')
    image = Image.open(io.BytesIO(png_str))

    return image


def plot_combined(individual):
    graph_image = plot_graph(individual)
    cartesian_image = plot_cartesian(individual)

    fig, axs = plt.subplots(2, 1, figsize=(18, 12))

    axs[0].imshow(graph_image)
    axs[0].axis('off')
    axs[0].set_title("Graph Representation", fontsize=16)

    axs[1].imshow(cartesian_image)
    axs[1].axis('off')
    axs[1].set_title("Cartesian Grid Representation", fontsize=16)
    plt.tight_layout()

    fig.canvas.draw()
    combined_image = Image.frombytes('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba())

    plt.close(fig)

    return combined_image


class ImageAnimation:
    def __init__(self, image_list):
        self.image_list = image_list
        self.iterations = len(image_list)

        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.image_list[0], animated=True)

        self.ax.axis('off')
        self.anim = animation.FuncAnimation(
            self.fig, self._draw_frame, frames=self.iterations,
            init_func=self._init, interval=1000, blit=True)

    def _init(self):
        self.im.set_data(self.image_list[0])
        return self.im,

    def _draw_frame(self, framedata):
        self.im.set_data(self.image_list[framedata])
        return self.im,

    def save(self, filename):
        self.anim.save(filename, writer='pillow')
