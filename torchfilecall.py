import torch
import torch.optim as optim
from transformers import VisionEncoderDecoderModel
import pickle


class TextRecognitionModel:
    class TrainingConfig:
        BATCH_SIZE: int = 28
        EPOCHS: int = 8
        LEARNING_RATE: float = 0.005

    MODEL_STATE_PATH = "model_state_dict.pkl"
    CHECKPOINT_PATH = "checkpoint.pth"

    def __init__(self, model_name='microsoft/trocr-large-handwritten'):
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=self.TrainingConfig.LEARNING_RATE,
            weight_decay=0.005
        )
        self.loss = self.TrainingConfig.LEARNING_RATE
        self.save_model()
        self.save_checkpoint()

    def save_model(self):
        model_state_dict = self.model.state_dict()
        with open(self.MODEL_STATE_PATH, "wb") as file:
            pickle.dump(model_state_dict, file)

    def save_checkpoint(self):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': self.loss
        }, self.CHECKPOINT_PATH)

    def load_model(self):
        with open(self.MODEL_STATE_PATH, "rb") as file:
            model_state_dict = pickle.load(file)
        self.model.load_state_dict(model_state_dict)
        self.model.eval()  # Set the model to evaluation mode

    def load_checkpoint(self):
        checkpoint = torch.load(self.CHECKPOINT_PATH)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.loss = checkpoint['loss']
        self.model.eval()  # Set the model to evaluation mode
