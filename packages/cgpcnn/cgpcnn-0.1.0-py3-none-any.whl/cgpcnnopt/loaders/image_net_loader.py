import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from ..utils import plot_images
import torchvision.datasets as datasets
import logging
import os
import numpy as np
from typing import Optional


class ImageNetDataLoader:
    def __init__(self, data_dir, scraper, batch_size, shuffle, random_seed, image_size, logger):
        self.data_dir: Optional[str] = data_dir
        self.train_loader: Optional[DataLoader] = None
        self.val_loader: Optional[DataLoader] = None
        self.test_loader: Optional[DataLoader] = None

        self.data_name = "ImageNet"

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.logger = logger or logging.getLogger(__name__)

        self.transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])

        self.scraper = scraper

    def display_sample_data(self, data: DataLoader, num_samples: int) -> None:
        """
        Displays sample images from a DataLoader.
        """
        images, labels = next(iter(data))

        images = images.numpy().transpose((0, 2, 3, 1))
        images = images * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])

        plot_images(images=images[:num_samples], cls_true=labels[:num_samples], label_names=data.dataset.classes, title="Sample ImageNet Images")

        self.logger.info("Sample data displayed successfully.")

    def describe_data(self) -> None:
        """
        Logs a description of the data, detailing the number of samples in each set.
        """
        self.logger.info("Data Description")
        self.logger.info("-----------------")
        if self.train_loader is not None:
            self.logger.info(f"Train Data: Number of samples: {len(self.train_loader.dataset)}")
        if self.val_loader is not None:
            self.logger.info(f"Validation Data: Number of samples: {len(self.val_loader.dataset)}")
        if self.test_loader is not None:
            self.logger.info(f"Test Data: Number of samples: {len(self.test_loader.dataset)}")

    def load_data(self):
        """
        Downloads and splits the data using ImageNetScraper, then loads it into DataLoader objects.
        """
        train_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'train'), transform=self.transform)
        val_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'valid'), transform=self.transform)
        test_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'test'), transform=self.transform)

        self.train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=self.shuffle)
        self.val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)
        self.test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        self.logger.info("Data loaded successfully.")

        return self.train_loader, self.val_loader, self.test_loader
