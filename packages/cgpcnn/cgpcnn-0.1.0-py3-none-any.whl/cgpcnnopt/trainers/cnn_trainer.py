import time
import torch
import torch.optim as optim
from enum import Enum
import os
import mlflow
import mlflow.pytorch
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


class OptimizerType(Enum):
    ADAM = 'Adam'
    SGD = 'SGD'
    RMSPROP = 'RMSprop'


class CNNTrainer:
    def __init__(self, train_loader, test_loader, val_loader, verbose, mlflow_enabled, experiment_name, logger, channel, imgSize, batchsize, result_folder_path, ml_flow_folder_path):
        self.verbose = verbose
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.mlflow_enabled = mlflow_enabled
        self.experiment_name = experiment_name
        self.logger = logger
        self.channel = channel
        self.imgSize = imgSize
        self.batchsize = batchsize
        self.result_folder_path = result_folder_path
        self.ml_flow_folder_path = ml_flow_folder_path

        if self.mlflow_enabled:
            self.init_mlflow()

    def train(self, model, learning_rate, optimizer_type, criterion, early_stopping, patience, epochs):
        model = model.to(self.device)
        model.train()

        best_loss = float('inf')
        patience_counter = 0

        criterion = criterion.to(self.device)
        optimizer = self.configure_optimizer(model, learning_rate, optimizer_type)

        input = torch.FloatTensor(self.batchsize, self.channel, self.imgSize, self.imgSize).to(self.device)
        label = torch.LongTensor(self.batchsize).to(self.device)

        history = []

        if self.verbose:
            self.logger.info(f"Training for {epochs} epochs.")

        start_train = time.time()

        for epoch in range(epochs):
            running_loss = 0.0

            for batch_idx, (data, target) in enumerate(self.train_loader):
                data, target = data.to(self.device), target.to(self.device)

                input.resize_as_(data).copy_(data)
                label.resize_as_(target).copy_(target)

                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

            avg_loss = running_loss / len(self.train_loader)
            history.append(avg_loss)

            if early_stopping:
                if avg_loss < best_loss:
                    best_loss = avg_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= patience:
                        if self.verbose:
                            self.logger.info(f"Early stopping triggered at epoch {epoch + 1}")
                        break

        end_train = time.time()

        if self.verbose:
            self.logger.info(f"Training completed in {end_train - start_train:.2f} seconds.")

        return model, history

    def evaluate(self, model):
        correct = 0
        total = 0
        model.eval()

        start_eval = time.time()

        with torch.no_grad():
            for data, target in self.train_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()

        end_eval = time.time()
        accuracy = correct / total

        if self.verbose:
            self.logger.info(f"Evaluation completed in {end_eval - start_eval:.2f} seconds. Accuracy: {accuracy * 100:.2f}%")

        return accuracy

    def predict(self, model, images):
        model = model.to(self.device)
        model.eval()

        images = images.to(self.device)

        with torch.no_grad():
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

        return predicted.cpu().numpy()

    def __call__(self, model, learning_rate, optimizer_type, criterion, early_stopping, patience, epochs):
        trained_model, history = self.train(
            model=model,
            learning_rate=learning_rate,
            optimizer_type=optimizer_type,
            criterion=criterion,
            early_stopping=early_stopping,
            patience=patience,
            epochs=epochs
        )
        accuracy = self.evaluate(trained_model)

        return trained_model, accuracy, history

    def save_model_and_results(self, model, name):
        os.makedirs(self.result_folder_path, exist_ok=True)

        model_path = os.path.join(self.result_folder_path, f'{name}.pth')
        torch.save(model.state_dict(), model_path)
        self.logger.info(f"Model saved to {model_path}")

        if self.mlflow_enabled:
            mlflow.pytorch.log_model(model, self.ml_flow_folder_path)

        model.to(self.device)
        model.eval()

        all_preds = []
        all_targets = []
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)

                all_preds.extend(predicted.cpu().numpy())
                all_targets.extend(target.cpu().numpy())

                total += target.size(0)
                correct += (predicted == target).sum().item()

        accuracy = correct / total
        self.logger.info(f"Model accuracy: {accuracy * 100:.2f}%")

        cm = confusion_matrix(all_targets, all_preds)
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=self.test_loader.dataset.classes, yticklabels=self.test_loader.dataset.classes)
        title = f'Confusion Matrix for {name}\nAccuracy: {accuracy * 100:.2f}%'
        plt.title(title)
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(os.path.join(self.result_folder_path, 'confusion_matrix.png'))
        self.logger.info(f"Confusion matrix saved to {os.path.join(self.result_folder_path, 'confusion_matrix.png')}")
        plt.close()

    def init_mlflow(self) -> None:
        encoded_uri = f"file:///{self.ml_flow_folder_path}"
        mlflow.set_tracking_uri(encoded_uri)
        mlflow.set_experiment(self.experiment_name)
        self.logger.info(f"MLflow URI: {encoded_uri}")
        self.logger.info(f"MLflow configured with tracking URI: {self.ml_flow_folder_path} and experiment name: {self.experiment_name}")

    def configure_optimizer(self, model, learning_rate, optimizer_type):
        if optimizer_type == OptimizerType.ADAM:
            return optim.Adam(model.parameters(), lr=learning_rate, betas=(0.5, 0.999))
        elif optimizer_type == OptimizerType.SGD:
            return optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)
        elif optimizer_type == OptimizerType.RMSPROP:
            return optim.RMSprop(model.parameters(), lr=learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")
