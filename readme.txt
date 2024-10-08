To run : python flask_final.py

you can test the values as :


# Example input for a pathological case
pathological_case = {
    'Baseline Value': 180,
    'Fetal Movement': 5,
    'Prolonged Decelerations': 4,
    'Mean Value of Short Term Variability': 1.5,
    'Mean Value of Long Term Variability': 10,
    'Histogram Min': 80,
    'Histogram Number of Peaks': 7,
    'Histogram Mean': 100,
    'Accelerations': 0,
    'Uterine Contractions': 5,
    'Abnormal Short Term Variability': 1,
    'Percentage of time with abnormal long-term variability': 50,
    'Histogram Width': 60,
    'Histogram Max': 190,
    'Histogram Number of Zeroes': 2,
    'Histogram Median': 90,
    'Light Decelerations': 5,
    'Severe Decelerations': 3,
    'Histogram Mode': 85,
    'Histogram Variance': 12.0,
    'Histogram Tendency': -2
}

suspect_case = {
    'Baseline Value': 130,  # Slightly above normal
    'Fetal Movement': 5,  # Reduced movement
    'Prolonged Decelerations': 1,  # Occasional decelerations
    'Mean Value of Short Term Variability': 4.0,  # Indicating possible stress
    'Mean Value of Long Term Variability': 30,  # Moderately abnormal
    'Histogram Min': 100,
    'Histogram Number of Peaks': 5,  # A bit irregular
    'Histogram Mean': 125,  # Slightly higher than normal
    'Accelerations': 0,  # Lack of accelerations
    'Uterine Contractions': 3,  # Mild increase
    'Abnormal Short Term Variability': 0.5,  # Abnormal
    'Percentage of time with abnormal long-term variability': 25,  # Elevated
    'Histogram Width': 50,
    'Histogram Max': 140,
    'Histogram Number of Zeroes': 0,
    'Histogram Median': 120,
    'Light Decelerations': 1,
    'Severe Decelerations': 0,
    'Histogram Mode': 120,
    'Histogram Variance': 10.0,  # Increased variability
    'Histogram Tendency': -1
}


normal_case = {
    'Baseline Value': 130,
    'Fetal Movement': 30,
    'Prolonged Decelerations': 0,
    'Mean Value of Short Term Variability': 6.5,
    'Mean Value of Long Term Variability': 30,
    'Histogram Min': 120,
    'Histogram Number of Peaks': 4,
    'Histogram Mean': 135,
    'Accelerations': 3,
    'Uterine Contractions': 2,
    'Abnormal Short Term Variability': 0,
    'Percentage of time with abnormal long-term variability': 10,
    'Histogram Width': 20,
    'Histogram Max': 150,
    'Histogram Number of Zeroes': 0,
    'Histogram Median': 135,
    'Light Decelerations': 1,
    'Severe Decelerations': 0,
    'Histogram Mode': 130,
    'Histogram Variance': 2.5,
    'Histogram Tendency': 0
}


High Risk
Age of the Person	40 years	
Body Temperature in Celsius	38.5°C	
Systolic BP in mmHg	150 mmHg	
Diastolic BP in mmHg	95 mmHg	
Heart Rate in Beats Per Minute	110 bpm	
Blood Glucose in mmol/L	9.0 mmol/L	

normal
Age of the Person	28 years	Within the ideal reproductive age range
Body Temperature in Celsius	36.8°C	Normal body temperature
Systolic BP in mmHg	110 mmHg	Healthy systolic blood pressure
Diastolic BP in mmHg	75 mmHg	Healthy diastolic blood pressure
Heart Rate in Beats Per Minute	70 bpm	Normal resting heart rate
Blood Glucose in mmol/L	4.8 mmol/L	Normal fasting blood glucose level
