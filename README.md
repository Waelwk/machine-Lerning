# machine-Learning

Steel industry energy consumption backend using a bagging-based RandomForest model. The Flask API exposes `/api/energy/predict` for Angular (or any) frontends to request a load type prediction.

## Quick start
1. Install dependencies: `pip install -r requirements.txt`
2. Start the energy API: `python energy_app.py`
3. Request a prediction (example payload):
   ```json
   {
     "Usage_kWh": 108.2,
     "Lagging_Current_Reactive.Power_kVarh": 0.0,
     "Leading_Current_Reactive_Power_kVarh": 0.0,
     "CO2(tCO2)": 0.53,
     "Lagging_Current_Power_Factor": 0.97,
     "Leading_Current_Power_Factor": 0.0,
     "NSM": 0,
     "WeekStatus": 0,
     "Day_of_week": "Sunday"
   }
   ```

## Tests
Run `python -m unittest test_energy_app.py` to validate the prediction endpoint.
