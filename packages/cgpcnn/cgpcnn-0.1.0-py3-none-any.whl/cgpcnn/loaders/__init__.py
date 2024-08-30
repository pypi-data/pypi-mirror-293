# src/loaders/__init__.py

from .cifar10_loader import CIFAR10DataLoader
from .mnist_loader import MNISTDataLoader
from .image_net_loader import ImageNetDataLoader

__all__ = ['CIFAR10DataLoader', 'MNISTDataLoader', 'ImageNetDataLoader']