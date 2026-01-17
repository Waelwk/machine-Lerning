import unittest

from energy_app import app, feature_columns


class EnergyAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_predict_returns_expected_load_type(self):
        sample_payload = {
            "Usage_kWh": 108.2,
            "Lagging_Current_Reactive.Power_kVarh": 0.0,
            "Leading_Current_Reactive_Power_kVarh": 0.0,
            "CO2(tCO2)": 0.53,
            "Lagging_Current_Power_Factor": 0.97,
            "Leading_Current_Power_Factor": 0.0,
            "NSM": 0,
            "WeekStatus": 0,
            "Day_of_week": "Sunday",
        }

        response = self.client.post("/api/energy/predict", json=sample_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("load_type"), "Light Load")
        self.assertTrue("confidence" in data)

    def test_predict_validates_missing_fields(self):
        response = self.client.post("/api/energy/predict", json={"Usage_kWh": 10})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Missing required fields", data["error"])
        self.assertIn("Day_of_week", data["error"])
        self.assertNotIn("Usage_kWh", data["error"])


if __name__ == "__main__":
    unittest.main()
