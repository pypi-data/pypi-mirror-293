import torch
from torch.utils.data import DataLoader, Subset, random_split
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np
from typing import Optional
from ..utils import plot_images


class CIFAR10DataLoader:
    def __init__(self, data_dir, batch_size, shuffle, random_seed, logger):
        self.data_dir: Optional[str] = data_dir
        self.train_loader: Optional[DataLoader] = None
        self.val_loader: Optional[DataLoader] = None
        self.test_loader: Optional[DataLoader] = None

        self.data_name = "CIFAR-10"

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.logger = logger
        self.class_names = ['airplane',
                            'automobile',
                            'bird',
                            'cat',
                            'deer',
                            'dog',
                            'frog',
                            'horse',
                            'ship',
                            'truck']

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def display_sample_data(self, data: DataLoader, num_samples: int) -> None:
        images, labels = next(iter(data))

        images = images.numpy().transpose((0, 2, 3, 1))
        images = images * 0.5 + 0.5

        plot_images(images=images[:num_samples], cls_true=labels[:num_samples], label_names=self.class_names, title="Sample CIFAR-10 Images")

        self.logger.info("Sample data displayed successfully.")

    def describe_data(self) -> None:
        self.logger.info("Data Description")
        self.logger.info("-----------------")
        if self.train_loader is not None:
            self.logger.info(f"Train Data: Number of samples: {len(self.train_loader.dataset)}")
        if self.val_loader is not None:
            self.logger.info(f"Validation Data: Number of samples: {len(self.val_loader.dataset)}")
        if self.test_loader is not None:
            self.logger.info(f"Test Data: Number of samples: {len(self.test_loader.dataset)}")

    def load_data(self, split_train_val_proportion, train_size=None, test_size=None):
        if sum(split_train_val_proportion) != 1.0:
            raise ValueError("Proportions must sum to 1.0")

        np.random.seed(self.random_seed)

        train_dataset = datasets.CIFAR10(root=self.data_dir, train=True, download=True, transform=self.transform)
        test_dataset = datasets.CIFAR10(root=self.data_dir, train=False, download=True, transform=self.transform)

        train_size_full = int(split_train_val_proportion[0] * len(train_dataset))
        val_size = len(train_dataset) - train_size_full

        train_subset, val_subset = random_split(train_dataset, [train_size_full, val_size])

        if train_size is not None and train_size < train_size_full:
            train_indices = np.random.choice(len(train_subset), train_size, replace=False)
            train_subset = Subset(train_subset, train_indices)
            train_subset.dataset.classes = self.class_names

        if test_size is not None and test_size < len(test_dataset):
            test_indices = np.random.choice(len(test_dataset), test_size, replace=False)
            test_dataset = Subset(test_dataset, test_indices)
            test_dataset.dataset.classes = self.class_names

        self.train_loader = DataLoader(train_subset, batch_size=self.batch_size, shuffle=self.shuffle)
        self.val_loader = DataLoader(val_subset, batch_size=self.batch_size, shuffle=False)
        self.test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        self.logger.info("Data loaded successfully.")
