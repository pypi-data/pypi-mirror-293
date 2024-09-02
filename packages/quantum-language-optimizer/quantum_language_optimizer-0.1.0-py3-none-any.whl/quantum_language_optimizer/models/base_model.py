class BaseModel:
    """
    BaseModel serves as a template for all models in the quantum_language_optimizer package.
    It defines the common interface that all models should implement.
    """
    def __init__(self):
        pass

    def train(self, data):
        """
        Train the model with the provided data.

        Parameters:
        data (any): The data used for training the model.

        Raises:
        NotImplementedError: This method should be overridden by subclasses.
        """
        raise NotImplementedError("Train method not implemented.")

    def predict(self, input_data):
        """
        Predict the output for the given input data.

        Parameters:
        input_data (any): The input data for which predictions are to be made.

        Raises:
        NotImplementedError: This method should be overridden by subclasses.
        """
        raise NotImplementedError("Predict method not implemented.")
