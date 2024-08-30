import numpy as np
from torch import nn
from ..trainers import OptimizerType
from ..converters import CGP2CNN


class CNNEvaluation:
    def __init__(self, trainer, logger, verbose=True, epoch_num=25, batchsize=16, imgSize=32):
        self.epoch_num = epoch_num
        self.logger = logger
        self.batchsize = batchsize
        self.verbose = verbose
        self.imgSize = imgSize
        self.trainer = trainer

    def __call__(self, net_lists):
        evaluations = np.zeros(len(net_lists))
        for i in range(len(net_lists)):
            model = CGP2CNN(net_lists[i], 3, 10, 32)
            trained_model, accuracy, history = self.trainer(model, 0.01, OptimizerType.ADAM, nn.CrossEntropyLoss(), False, 5, self.epoch_num)
            evaluations[i] = accuracy
        return evaluations
