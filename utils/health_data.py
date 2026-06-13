"""
Indian healthcare data: food nutrition, Ayurvedic info,
common medications, and health tips.
"""

# Indian food nutrition database (per 100g unless noted)
INDIAN_FOODS = {
    "Dal (masoor, cooked)": {"calories": 116, "protein": 9.0, "carbs": 20.0, "fat": 0.4},
    "Dal (chana, cooked)": {"calories": 164, "protein": 8.9, "carbs": 27.0, "fat": 2.6},
    "Dal (moong, cooked)": {"calories": 105, "protein": 7.0, "carbs": 19.0, "fat": 0.4},
    "Chapati / Roti (1 piece)": {"calories": 71, "protein": 2.5, "carbs": 15.0, "fat": 0.4},
    "Rice (cooked, 1 cup)": {"calories": 206, "protein": 4.3, "carbs": 44.5, "fat": 0.4},
    "Idli (1 piece)": {"calories": 39, "protein": 1.9, "carbs": 8.0, "fat": 0.1},
    "Dosa (plain, 1 medium)": {"calories": 168, "protein": 3.9, "carbs": 26.0, "fat": 5.6},
    "Upma (1 cup)": {"calories": 250, "protein": 5.0, "carbs": 37.0, "fat": 8.0},
    "Poha (1 cup)": {"calories": 270, "protein": 5.5, "carbs": 53.0, "fat": 3.9},
    "Paneer (100g)": {"calories": 265, "protein": 18.3, "carbs": 1.2, "fat": 20.8},
    "Curd / Dahi (1 cup)": {"calories": 149, "protein": 8.5, "carbs": 11.4, "fat": 8.0},
    "Lassi (1 glass)": {"calories": 150, "protein": 6.0, "carbs": 18.0, "fat": 5.5},
    "Sambar (1 cup)": {"calories": 95, "protein": 4.5, "carbs": 15.0, "fat": 2.0},
    "Aloo Sabzi (1 cup)": {"calories": 195, "protein": 3.5, "carbs": 28.0, "fat": 8.0},
    "Palak Sabzi (1 cup)": {"calories": 100, "protein": 4.0, "carbs": 8.0, "fat": 6.0},
    "Rajma (cooked, 1 cup)": {"calories": 225, "protein": 15.3, "carbs": 40.0, "fat": 0.9},
    "Chole (1 cup)": {"calories": 270, "protein": 14.5, "carbs": 45.0, "fat": 4.3},
    "Chicken Curry (1 serving)": {"calories": 300, "protein": 28.0, "carbs": 7.0, "fat": 18.0},
    "Fish Curry (1 serving)": {"calories": 220, "protein": 23.0, "carbs": 5.0, "fat": 12.0},
    "Egg (boiled, 1 large)": {"calories": 77, "protein": 6.3, "carbs": 0.6, "fat": 5.3},
    "Banana (1 medium)": {"calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
    "Mango (1 cup)": {"calories": 99, "protein": 1.4, "carbs": 24.7, "fat": 0.6},
    "Guava (1 medium)": {"calories": 68, "protein": 2.6, "carbs": 14.3, "fat": 1.0},
    "Papaya (1 cup)": {"calories": 55, "protein": 0.9, "carbs": 14.0, "fat": 0.2},
    "Buttermilk / Chaas (1 glass)": {"calories": 40, "protein": 3.0, "carbs": 4.9, "fat": 0.9},
    "Khichdi (1 cup)": {"calories": 220, "protein": 7.5, "carbs": 38.0, "fat": 4.5},
    "Biryani (1 cup)": {"calories": 290, "protein": 11.0, "carbs": 38.0, "fat": 10.0},
    "Paratha (1 piece)": {"calories": 126, "protein": 3.0, "carbs": 16.0, "fat": 5.7},
    "Coconut Chutney (2 tbsp)": {"calories": 60, "protein": 0.7, "carbs": 3.0, "fat": 5.5},
    "Green Tea (1 cup)": {"calories": 2, "protein": 0.0, "carbs": 0.0, "fat": 0.0},
    "Masala Chai (with milk, 1 cup)": {"calories": 60, "protein": 2.0, "carbs": 8.0, "fat": 2.0},
}

# Common Indian medications with info
COMMON_MEDICATIONS = {
    "Paracetamol / Crocin": {
        "uses": "Fever, mild to moderate pain",
        "common_dose": "500mg–1000mg every 4–6 hours",
        "max_daily": "4000mg",
        "warnings": "Do not exceed max dose. Avoid alcohol. Caution in liver disease.",
        "brand_names": "Crocin, Calpol, Dolo 650"
    },
    "Ibuprofen / Brufen": {
        "uses": "Pain, inflammation, fever",
        "common_dose": "200mg–400mg every 6–8 hours",
        "max_daily": "1200mg (OTC), 3200mg (prescription)",
        "warnings": "Take with food. Avoid with kidney problems or blood thinners.",
        "brand_names": "Brufen, Combiflam (with paracetamol)"
    },
    "Metformin": {
        "uses": "Type 2 Diabetes – reduces blood sugar",
        "common_dose": "500mg–2000mg daily (with meals)",
        "max_daily": "2550mg",
        "warnings": "Take with food to reduce GI side effects. Monitor kidney function.",
        "brand_names": "Glucophage, Glycomet, Obimet"
    },
    "Amlodipine": {
        "uses": "High blood pressure, angina",
        "common_dose": "5mg–10mg once daily",
        "max_daily": "10mg",
        "warnings": "Do not stop abruptly. May cause ankle swelling.",
        "brand_names": "Amlopress, Stamlo, Amlokind"
    },
    "Atorvastatin": {
        "uses": "High cholesterol (LDL reduction)",
        "common_dose": "10mg–80mg once daily (evening)",
        "max_daily": "80mg",
        "warnings": "Report muscle pain. Avoid grapefruit juice.",
        "brand_names": "Atorlip, Lipitor, Tonact"
    },
    "Pantoprazole / Omeprazole": {
        "uses": "Acidity, GERD, ulcers",
        "common_dose": "40mg once daily before breakfast",
        "max_daily": "80mg",
        "warnings": "Long-term use may affect B12 and magnesium levels.",
        "brand_names": "Pan 40, Pantop, Omez"
    },
    "Azithromycin": {
        "uses": "Bacterial infections (respiratory, ENT)",
        "common_dose": "500mg once daily for 3–5 days",
        "max_daily": "500mg",
        "warnings": "Complete the course. May cause QT prolongation.",
        "brand_names": "Azithral, Zithromax, Azee"
    },
    "Cetirizine": {
        "uses": "Allergies, hay fever, urticaria",
        "common_dose": "10mg once daily",
        "max_daily": "10mg",
        "warnings": "May cause drowsiness. Avoid alcohol.",
        "brand_names": "Cetzine, Alerid, Zyrtec"
    },
    "Aspirin (low dose)": {
        "uses": "Blood thinner for heart disease prevention",
        "common_dose": "75mg–150mg once daily",
        "max_daily": "150mg (cardiac dose)",
        "warnings": "Do not give to children. Risk of bleeding.",
        "brand_names": "Ecosprin, Aspicot, Loprin"
    },
    "Insulin (various)": {
        "uses": "Diabetes management",
        "common_dose": "As prescribed by doctor",
        "max_daily": "Doctor-defined",
        "warnings": "Monitor blood sugar regularly. Risk of hypoglycemia.",
        "brand_names": "Actrapid, Mixtard, Lantus, Basalog"
    },
}

# Ayurvedic remedies info
AYURVEDIC_INFO = {
    "Ashwagandha": {
        "benefits": "Reduces stress and anxiety, improves energy and immunity, supports thyroid function",
        "traditional_use": "Rasayana (rejuvenating herb), adaptogen",
        "typical_dose": "300–500mg root extract daily",
        "caution": "Avoid in pregnancy. May interact with thyroid and immunosuppressant medications."
    },
    "Triphala": {
        "benefits": "Digestive health, gentle laxative, antioxidant, eye health",
        "traditional_use": "Daily detox and bowel regulation",
        "typical_dose": "1 tsp powder at bedtime with warm water",
        "caution": "May cause loose stools in high doses. Avoid in diarrhea."
    },
    "Turmeric / Haldi": {
        "benefits": "Anti-inflammatory, antioxidant, joint health, immunity booster",
        "traditional_use": "Golden milk (haldi doodh), wound healing",
        "typical_dose": "500–1000mg curcumin extract or 1 tsp daily in food",
        "caution": "High doses may thin blood. Take with black pepper for absorption."
    },
    "Tulsi (Holy Basil)": {
        "benefits": "Respiratory health, stress relief, antimicrobial, blood sugar support",
        "traditional_use": "Kadha (herbal decoction) for colds and fever",
        "typical_dose": "2–3 cups of tulsi tea daily",
        "caution": "May interact with blood thinners. Avoid large amounts in pregnancy."
    },
    "Neem": {
        "benefits": "Blood purifier, skin health, anti-diabetic, anti-bacterial",
        "traditional_use": "Neem leaves juice for diabetes; bark for teeth",
        "typical_dose": "Neem juice: 20–30ml daily or as prescribed",
        "caution": "Bitter taste; high doses may be toxic. Not for children or pregnant women."
    },
    "Giloy (Guduchi)": {
        "benefits": "Immunity booster, antipyretic, anti-inflammatory, useful in dengue recovery",
        "traditional_use": "Fever management, immunity (especially post-viral)",
        "typical_dose": "Juice: 20–30ml twice daily or tablet form",
        "caution": "May lower blood sugar. Monitor if on diabetes medications."
    },
}

# Health tips in Indian context
HEALTH_TIPS = [
    " Start your day with a glass of warm water with lemon – aids digestion",
    "🥗 Include dals and legumes daily – excellent plant-based protein for Indian diets",
    " Aim for 8,000–10,000 steps daily – even a post-dinner walk (sair) helps digestion",
    " Drink 8–10 glasses of water daily; increase in summer months",
    "🧘 Practice yoga or pranayama for 20 minutes daily for stress and respiratory health",
    " Add haldi (turmeric) and jeera (cumin) to cooking – natural anti-inflammatories",
    " Sleep 7–8 hours; avoid heavy meals 2 hours before bedtime",
    " Eat seasonal Indian fruits – amla, jamun, papaya are rich in vitamins",
    "🫀 Monitor blood pressure regularly, especially if family history of hypertension",
    "🩺 Get a full body checkup annually after age 30 – includes blood sugar, lipids",
    " Replace white rice with brown rice or millets (ragi, jowar) for better glycemic control",
    "☀️ Get 15–20 min of morning sunlight daily for Vitamin D (common deficiency in India)",
]

def get_bmi_info(weight_kg, height_cm):
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        category, color = "Underweight", ""
    elif bmi < 23:
        category, color = "Normal (Asian standard)", "🟢"
    elif bmi < 27.5:
        category, color = "Overweight", "🟡"
    else:
        category, color = "Obese", ""
    return round(bmi, 1), category, color

def get_water_target(weight_kg):
    """Recommended daily water in ml"""
    return int(weight_kg * 35)

def get_calorie_target(weight_kg, height_cm, age, gender, activity="moderate"):
    """Mifflin-St Jeor equation"""
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    multipliers = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    return int(bmr * multipliers.get(activity, 1.55))

MEDICATION_TIMES = ["Morning (8 AM)", "Afternoon (1 PM)", "Evening (6 PM)", "Night (10 PM)", "Before meals", "After meals", "With breakfast", "At bedtime"]
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
INDIAN_STATES = ["Andhra Pradesh","Assam","Bihar","Chhattisgarh","Delhi","Goa","Gujarat",
                 "Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
                 "Maharashtra","Manipur","Meghalaya","Odisha","Punjab","Rajasthan","Tamil Nadu",
                 "Telangana","Uttar Pradesh","Uttarakhand","West Bengal","Other"]
COMMON_CONDITIONS = ["Diabetes (Type 2)","Hypertension","Hypothyroidism","Asthma","Heart Disease",
                     "Arthritis","PCOD/PCOS","Anemia","Vitamin D Deficiency","Obesity","None"]

