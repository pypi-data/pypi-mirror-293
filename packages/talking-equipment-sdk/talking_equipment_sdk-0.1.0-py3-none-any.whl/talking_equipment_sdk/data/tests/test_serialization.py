from unittest import TestCase

from talking_equipment_sdk import VoltageData, ThreePhaseVoltageData


class TestSerialization(TestCase):
    def setUp(self):
        self.voltage = VoltageData(23.4)
        self.three_phase_voltage = ThreePhaseVoltageData(34.5, 45.6, 56)

    def test_dump(self):
        self.assertEqual(self.voltage.model_dump()['value'], 23.4)
        self.assertEqual(self.three_phase_voltage.model_dump()['a']['value'], 34.5)

    def test_dump_json(self):
        self.assertTrue(isinstance(self.voltage.model_dump_json(), str))
        self.assertTrue(isinstance(self.three_phase_voltage.model_dump_json(), str))

    def test_value_dump(self):
        self.assertTrue(isinstance(self.voltage.value, float))
        self.assertTrue(isinstance(self.three_phase_voltage.value, str))

    def test_validate(self):
        three_phase_voltage_dict = self.three_phase_voltage.model_dump()
        new_three_phase_voltage =  ThreePhaseVoltageData.model_validate(three_phase_voltage_dict)

        self.assertEqual(new_three_phase_voltage.b.value, 45.6)

    def test_validate_json(self):
        three_phase_voltage_json_data = self.three_phase_voltage.value
        new_three_phase_voltage =  ThreePhaseVoltageData.model_validate_json(three_phase_voltage_json_data)

        self.assertEqual(new_three_phase_voltage.c.value, 56.0)

