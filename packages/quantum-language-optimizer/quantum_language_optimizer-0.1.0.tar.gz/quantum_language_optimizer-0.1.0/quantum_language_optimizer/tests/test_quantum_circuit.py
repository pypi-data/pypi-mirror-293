import unittest
from quantum_language_optimizer.core.quantum_circuit import SimpleQuantumCircuit

class TestQuantumCircuit(unittest.TestCase):
    def setUp(self):
        self.qc_builder = SimpleQuantumCircuit(3)

    def test_initialize_state(self):
        self.qc_builder.initialize_state('101')
        expected_state = [1, 0, 1]
        self.assertEqual(self.qc_builder.state, expected_state)

    def test_apply_gates(self):
        self.qc_builder.apply_gates()
        expected_gates = ['H 0', 'CX 0 1', 'RX 3.14/4 2']
        self.assertEqual(self.qc_builder.gates, expected_gates)

    def test_execute_circuit(self):
        self.qc_builder.initialize_state('101')
        self.qc_builder.apply_gates()
        self.qc_builder.measure_state()
        result = self.qc_builder.execute_circuit()
        self.assertIn('000', result)
        self.assertIn('111', result)

if __name__ == '__main__':
    unittest.main()
