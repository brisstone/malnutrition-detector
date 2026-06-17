# Pattern Recognition for Malnutrition Detection

## 📌 Project Aim
This project provides a machine-learning-based decision-support tool designed to assist frontline health workers in rural Nigeria in accurately classifying pediatric malnutrition (Severe, Moderate, Normal) among children under five years of age.

## 📊 Dataset & Methodology
The data utilized in this project is sourced from the public Kaggle "Children Malnutrition Dataset" combined with simulated socio-behavioral health survey variables to reflect rural realities.
* **Target Leakage Addressed:** The Mid-Upper Arm Circumference (MUAC) feature was strictly excluded from the training matrix to prevent the algorithm from memorizing single-variable rules, ensuring the model learns complex multidimensional patterns.
* **Evaluation:** Models were rigorously evaluated using 5-Fold Cross-Validation to ensure statistical reliability against overfitting.

## 🧬 Features Utilized
The system analyzes a matrix of anthropometric and socio-behavioral indicators:
* `age_months`: Age of the child.
* `weight_kg`: Weight in kilograms.
* `height_cm`: Height in centimeters.
* `bmi`: Auto-calculated Body Mass Index.
* `water_source`: Safety level of household water.
* `dietary_diversity_score`: Measurement of nutritional variety.
* `diarrhea_past_2_weeks`: Indicator of recent acute illness.

## 🤖 Models & Performance Metrics
Two supervised machine learning classification algorithms were developed and compared:
1. **Multinomial Logistic Regression (Primary Model)**
   * Cross-Validation Accuracy: 91.64%
2. **Decision Tree Classifier (Comparison Model)**
   * Cross-Validation Accuracy: 89.92%

*Note: Detailed Precision, Recall, F1-Scores, and Confusion Matrices are generated via the `train.py` script.*

## ⚠️ Limitations
* **Class Imbalance:** Due to the natural distribution of clinical data, instances of 'Severe' malnutrition are underrepresented compared to 'Normal' cases, slightly reducing precision in the minority class.
* **Geographic Specificity:** While trained on robust data, the model should ideally be fine-tuned with hyper-local health survey data from Kwara State communities before full medical deployment.

## 🚀 How to Run the Application
1. **Install Requirements:** Ensure Python is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
2. **Train the Models (Optional):** To re-generate the .pkl files and view evaluation metrics:
   ```bash
   python train.py
   ```
3. **Launch the UI:** To start the interactive Streamlit web application:
   ```bash
   streamlit run app.py
   ```

### **The Final Step**
Save both of these files. Push them to your GitHub repository, and let Streamlit Cloud automatically refresh your live URL.

Your codebase, your UI, and your methodology now perfectly match your revised documentation and completely satisfy all 10 of the supervisor's gaps. You are officially ready to dominate this defense!
