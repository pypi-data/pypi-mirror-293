from .quantum_circuit import AbstractQuantumCircuit

class QuantumRNN:
    def __init__(self, quantum_circuit_builder: AbstractQuantumCircuit):
        """
        Initialize the Quantum RNN.

        Parameters:
        quantum_circuit_builder (AbstractQuantumCircuit): Quantum circuit builder.
        """
        self.quantum_circuit_builder = quantum_circuit_builder

    def forward(self, input_sequence):
        """
        Forward propagation to process input sequence data.

        Parameters:
        input_sequence (list of str): Input sequence, where each element is a binary string.

        Returns:
        list of dict: Measurement results for each time step.
        """
        outputs = []
        for input_data in input_sequence:
            self.quantum_circuit_builder.initialize_state(input_data)
            self.quantum_circuit_builder.apply_gates()
            self.quantum_circuit_builder.measure_state()
            output = self.quantum_circuit_builder.execute_circuit()
            outputs.append(output)
        return outputs
