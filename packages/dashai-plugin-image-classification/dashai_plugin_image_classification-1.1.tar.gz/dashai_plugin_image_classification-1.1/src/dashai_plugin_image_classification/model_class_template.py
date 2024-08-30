from DashAI.back.core.schema_fields import BaseSchema, schema_field
from DashAI.back.models.base_model import BaseModel
from DashAI.back.config_object import ConfigObject
import torch.utils.data
import datasets
from torchvision import transforms
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset


class MLPSchema(BaseSchema):
    epochs: schema_field(
        int_field(ge=1),
        placeholder=5,
        description ="The number of epochs to train the model"
    )

    learning_rate: schema_field(
        float_field(ge=0.001),
        placeholder=0.001,
        description ="The learning rate to train the model"
    )

    hidden_dims: schema_field(
        list_field(int_field(ge = 1)),
        placeholder=[1,2,3],
        description ="The hidden dims to train the model"
    )


# MLP Image Classifier class
# This class already fulfill the DashAI model's interface (methods and signatures)

class MLPClassifier(BaseModel, ConfigObject):
    SCHEMA = MLPSchema
    COMPATIBLE_COMPONENTS = ["ImageClassificationTask"]

    def __init__(self, epochs, learning_rate, hidden_dims, **kwargs):
        super().__init__(**kwargs)
        self.epochs = epochs
        self.hidden_dims = hidden_dims
        self.learning_rate = learning_rate
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def fit(self, x_train: datasets.Dataset, y_train: datasets.Dataset):
        # Adapt adn transform x_train and y_train datasets to Pytorch Dataset
        dataset = datasets.Dataset.from_dict(
            {
                "image": x_train["image"],
                "label": y_train["label"],
            }
        )
        image_dataset = TransformedImageDataset(dataset)
        train_loader = DataLoader(image_dataset, batch_size=32, shuffle=True)

        # Set model
        self.model = MLP(
            image_dataset.input_dim,
            image_dataset.output_dim,
            self.hidden_dims
        ).to(self.device)
        self.criteria = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.model = fit_model(
            self.model,
            train_loader,
            self.epochs,
            self.criteria,
            self.optimizer,
            self.device,
        )

    def predict(self, x_pred: datasets.Dataset):
        image_dataset = TransformedImageDataset(x_pred)
        test_loader = DataLoader(image_dataset, batch_size=32, shuffle=False)
        predicted = predict(self.model, test_loader, self.device)
        return predicted

    def predict_one_image(self, image):
        self.model.eval()
        image = image.to(self.device)
        output = self.model(image)
        _, predicted = torch.max(output, 1)
        return predicted

    def save(self, filename: str) -> None:
        """Save the model in the specified path."""
        torch.save(self.model, filename)

    @staticmethod
    def load(filename: str) -> None:
        """Load the model of the specified path."""
        model = torch.load(filename)
        return model

# This class helps to transform data to pytorch-compatible format
class TransformedImageDataset(torch.utils.data.Dataset):
    def __init__(self, dataset: datasets.Dataset):
        self.dataset = dataset
        self.transforms = transforms.Compose([
                transforms.Resize((30, 30)),
                transforms.ToTensor(),
            ])

        column_names = list(self.dataset.features.keys())
        self.image_col_name = column_names[0]
        self.tensor_shape = self.transforms(self.dataset[0][self.image_col_name]).shape
        self.input_dim = (self.tensor_shape[0] *
                          self.tensor_shape[1] *
                          self.tensor_shape[2])
        if len(column_names) > 1:
            self.label_col_name = column_names[1]
            self.output_dim = len(set(self.dataset[self.label_col_name]))
        else:
            self.label_col_name = None

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image = self.dataset[idx][self.image_col_name]
        image = self.transforms(image)
        if self.label_col_name is None:
            return image
        label = self.dataset[idx][self.label_col_name]
        return image, label

# Multi Layer Perceptron class
class MLP(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dims):
        super().__init__()
        self.hidden_layers = nn.ModuleList()
        previous_dim = input_dim

        for hidden_dim in hidden_dims:
            self.hidden_layers.append(nn.Linear(previous_dim, hidden_dim))
            previous_dim = hidden_dim

        self.output_layer = nn.Linear(previous_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, input: torch.Tensor):
        batch_size = input.shape[0]
        x = input.view(batch_size, -1)

        for layer in self.hidden_layers:
            x = self.relu(layer(x))

        x = self.output_layer(x)
        return x


# Auxiliary functions
def fit_model(
    model: nn.Module,
    train_loader: DataLoader,
    epochs: int,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    device: torch.device
):
    model.train()
    for epoch in range(epochs):
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")
    return model

def predict(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device,
):
    model.eval()
    probs_predicted = []
    with torch.no_grad():
        for images in dataloader:
            images = images.to(device)
            output_probs: torch.Tensor = model(images)
            probs_predicted += output_probs.tolist()
    return probs_predicted


"""
class ExampleModelClass(BaseModel, ConfigObject):

    SCHEMA = ExampleModelSchema
    COMPATIBLE_COMPONENTS = ["TaskName"]

    def __init__(self, **kwargs): # Params are passed when the model is initialized
        super().__init__(**kwargs)
        self.model = None

    def fit(self, x_train, y_train) -> None:
        """ Fit the model to the data

        Parameters
        ----------
        x_train : Datasets
            Input data.
        y_train : Datasets
            Output data.

        """
        raise NotImplementedError
    
    def predict(self, x_pred) -> list:
        """Make a prediction with the model.

        Parameters
        ----------
        x_pred : Union[Dataset, pd.DataFrame]
            Dataset with the input data columns.

        Returns
        -------
        array-like
            Array with the predicted probabilities values for x_pred
        """
        raise NotImplementedError

    def save(self, filename: str) -> None:
        """Store an instance of a model.

        filename (Str): Indicates where to store the model,
        if filename is None, this method returns a bytes array with the model.
        """
        raise NotImplementedError
    
    @staticmethod
    def load(self, filename: str):
        """Restores an instance of a model.

        filename (Str): Indicates where the model was stored.
        """
        raise NotImplementedError
"""