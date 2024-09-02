import unittest
from quantum_language_optimizer.core.quantum_circuit import SimpleQuantumCircuit
from quantum_language_optimizer.core.quantum_rnn import QuantumRNN

class TestQuantumRNN(unittest.TestCase):
    def setUp(self):
        self.qc_builder = SimpleQuantumCircuit(3)
        self.quantum_rnn = QuantumRNN(self.qc_builder)

    def test_forward(self):
        input_sequence = ['101', '110', '011']
        output = self.quantum_rnn.forward(input_sequence)
        self.assertEqual(len(output), 3)
        for result in output:
            self.assertIn('000', result)
            self.assertIn('111', result)

if __name__ == '__main__':
    unittest.main()
