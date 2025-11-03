"""
ML Konseptlari va Darslar Bazasi
Bu modul Machine Learning konseptlarini va misollarini saqlaydi
"""

class MLConcepts:
    """
    Machine Learning konseptlari va tushuntirishlari
    """
    
    def __init__(self):
        # ML konseptlari bazasi
        self.concepts = {
            "supervised_learning": {
                "uz": "Nazorat ostidagi o'rganish",
                "description": """
                Supervised Learning - bu algoritmga to'g'ri javoblar bilan ma'lumot berib o'rgatish usuli.
                
                Misol: Uy narxini bashorat qilish
                - Ma'lumot: Uyning maydoni, xonalar soni, joylashuvi
                - Javob: Uyning narxi
                
                Algoritm bu ma'lumotlardan o'rganib, yangi uylarning narxini bashorat qila oladi.
                """,
                "types": ["Regression", "Classification"],
                "algorithms": ["Linear Regression", "Decision Trees", "Random Forest", "Neural Networks"]
            },
            
            "unsupervised_learning": {
                "uz": "Nazorat ostida bo'lmagan o'rganish",
                "description": """
                Unsupervised Learning - algoritmga faqat ma'lumot beriladi, to'g'ri javoblar yo'q.
                Algoritm o'zi ma'lumotlardagi naqsh va guruhlarni topadi.
                
                Misol: Mijozlarni guruhlash
                - Ma'lumot: Mijozlarning xarid tarixi
                - Vazifa: O'xshash mijozlarni guruhga ajratish
                
                Algoritm xarid xususiyatlariga qarab mijozlarni o'zi guruhlaydi.
                """,
                "types": ["Clustering", "Dimensionality Reduction"],
                "algorithms": ["K-Means", "PCA", "Hierarchical Clustering"]
            },
            
            "neural_networks": {
                "uz": "Neyron tarmoqlar",
                "description": """
                Neural Networks - bu insonning miyasi kabi ishlaydigan sun'iy tarmoq.
                
                Tarkibi:
                1. Input Layer (Kirish qatlami) - ma'lumot kiradi
                2. Hidden Layers (Yashirin qatlamlar) - hisoblashlar bo'ladi
                3. Output Layer (Chiqish qatlami) - natija chiqadi
                
                Har bir neyron raqamlarni qabul qiladi, hisoblaydi va keyingisiga uzatadi.
                """,
                "components": ["Neurons", "Weights", "Bias", "Activation Functions"],
                "applications": ["Image Recognition", "Speech Recognition", "Text Generation"]
            },
            
            "regression": {
                "uz": "Regressiya",
                "description": """
                Regression - raqamli qiymatni bashorat qilish.
                
                Misol: Haroratni bashorat qilish
                - Input: Sana, vaqt, namlik
                - Output: Harorat (masalan, 25.5°C)
                
                Linear Regression - eng oddiy turi:
                y = mx + b
                
                Bu yerda:
                - y - bashorat qilinadigan qiymat
                - x - ma'lum qiymat
                - m - og'irlik (weight)
                - b - siljish (bias)
                """,
                "types": ["Linear", "Polynomial", "Ridge", "Lasso"],
                "metrics": ["MSE", "RMSE", "MAE", "R²"]
            },
            
            "classification": {
                "uz": "Klassifikatsiya",
                "description": """
                Classification - ma'lumotni toifalarga ajratish.
                
                Misol: Email spam yoki yo'qligini aniqlash
                - Input: Email matni
                - Output: Spam yoki Not Spam
                
                Binary Classification - 2 toifa (ha/yo'q)
                Multi-class Classification - ko'p toifa (masalan, hayvonlar turi)
                """,
                "types": ["Binary", "Multi-class", "Multi-label"],
                "algorithms": ["Logistic Regression", "SVM", "Decision Trees", "Neural Networks"],
                "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"]
            },
            
            "overfitting": {
                "uz": "Haddan tashqari o'rganish",
                "description": """
                Overfitting - model train ma'lumotlarini juda yaxshi eslab qoladi, 
                lekin yangi ma'lumotlarda yomon ishlaydi.
                
                Misol: Imtihonga tayyorgarlik
                - Overfitting: Faqat namunalar javoblarini yodlash
                - Yaxshi model: Konseptlarni tushunish
                
                Yechim:
                1. Ko'proq ma'lumot to'plash
                2. Regularization ishlatish
                3. Cross-validation qilish
                4. Dropout (neural network uchun)
                """,
                "indicators": ["High training accuracy, low test accuracy", "Model too complex"],
                "solutions": ["More data", "Regularization", "Simpler model", "Dropout"]
            },
            
            "underfitting": {
                "uz": "Yetarli o'rganmaslik",
                "description": """
                Underfitting - model juda oddiy va ma'lumotlarni yaxshi o'rganmaydi.
                
                Misol: Murakkab matematika masalasini oddiy formula bilan yechmoqchi bo'lish
                
                Belgisi:
                - Train va test ikkalasida ham past accuracy
                
                Yechim:
                1. Murakkabroq model tanlash
                2. Ko'proq feature qo'shish
                3. Ko'proq o'rgatish (epoch)
                """,
                "indicators": ["Low accuracy on both train and test"],
                "solutions": ["More complex model", "More features", "More training"]
            },
            
            "feature_engineering": {
                "uz": "Xususiyatlarni yaratish",
                "description": """
                Feature Engineering - ma'lumotlardan foydali xususiyatlar yaratish.
                
                Misol: Vaqt ma'lumotidan feature yaratish
                - 2024-01-15 12:30 dan:
                  * yil = 2024
                  * oy = 1
                  * kun = 15
                  * soat = 12
                  * ish_kuni = ha
                  * dam_olish = yo'q
                
                Yaxshi feature'lar = yaxshi model!
                """,
                "techniques": ["Scaling", "Encoding", "Binning", "Polynomial Features"],
                "importance": "Very High - determines model success"
            }
        }
        
        # Python darslari
        self.python_lessons = {
            "basics": {
                "title": "Python Asoslari",
                "topics": ["Variables", "Data Types", "Operators", "Conditions", "Loops"],
                "code_example": """
# O'zgaruvchilar
name = "Ali"
age = 20
height = 1.75

# Shartlar
if age >= 18:
    print("Voyaga yetgan")
else:
    print("Voyaga yetmagan")

# Sikllar
for i in range(5):
    print(f"Raqam: {i}")
"""
            },
            
            "numpy": {
                "title": "NumPy - Raqamlar bilan ishlash",
                "topics": ["Arrays", "Operations", "Indexing", "Broadcasting"],
                "code_example": """
import numpy as np

# Array yaratish
arr = np.array([1, 2, 3, 4, 5])
print(arr)

# Matematika operatsiyalari
print(arr * 2)        # Har birini 2ga ko'paytirish
print(arr + 10)       # Har biriga 10 qo'shish
print(np.mean(arr))   # O'rtacha qiymat
print(np.sum(arr))    # Yig'indi
"""
            },
            
            "pandas": {
                "title": "Pandas - Ma'lumotlar bilan ishlash",
                "topics": ["DataFrame", "Reading Data", "Filtering", "Grouping"],
                "code_example": """
import pandas as pd

# DataFrame yaratish
data = {
    'Ism': ['Ali', 'Vali', 'Guli'],
    'Yosh': [20, 25, 22],
    'Ball': [85, 90, 88]
}
df = pd.DataFrame(data)

# Ma'lumotni ko'rish
print(df.head())

# Filterlash
talabalar = df[df['Ball'] > 85]
print(talabalar)

# O'rtacha ball
print(df['Ball'].mean())
"""
            },
            
            "sklearn_basics": {
                "title": "Scikit-learn - ML modellari",
                "topics": ["Model Training", "Prediction", "Evaluation"],
                "code_example": """
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

# Ma'lumot tayyorlash
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train va test ga bo'lish
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model yaratish va o'rgatish
model = LinearRegression()
model.fit(X_train, y_train)

# Bashorat qilish
prediction = model.predict(X_test)
print(f"Bashorat: {prediction}")
print(f"Haqiqiy: {y_test}")
"""
            }
        }
    
    def get_concept(self, concept_name):
        """
        Konsept haqida ma'lumot qaytarish
        """
        return self.concepts.get(concept_name.lower(), None)
    
    def get_python_lesson(self, lesson_name):
        """
        Python darsi haqida ma'lumot qaytarish
        """
        return self.python_lessons.get(lesson_name.lower(), None)
    
    def search_concept(self, keyword):
        """
        Kalit so'z bo'yicha konseptlarni qidirish
        """
        results = []
        keyword = keyword.lower()
        
        for concept_name, concept_data in self.concepts.items():
            if (keyword in concept_name.lower() or 
                keyword in concept_data.get('uz', '').lower() or
                keyword in concept_data.get('description', '').lower()):
                results.append({
                    'name': concept_name,
                    'uz_name': concept_data.get('uz'),
                    'description': concept_data.get('description')[:200] + "..."
                })
        
        return results
    
    def get_all_concepts_list(self):
        """
        Barcha konseptlar ro'yxatini qaytarish
        """
        return [
            {
                'name': name,
                'uz_name': data.get('uz'),
                'description': data.get('description', '')[:100] + "..."
            }
            for name, data in self.concepts.items()
        ]
    
    def get_quiz_question(self, topic):
        """
        Mavzu bo'yicha test savoli yaratish
        """
        quizzes = {
            "supervised_learning": {
                "question": "Supervised Learning nima?",
                "options": [
                    "Algoritmga to'g'ri javoblar bilan o'rgatish",
                    "Algoritm o'zi naqsh topadi",
                    "Faqat rasm bilan ishlash",
                    "Internet orqali o'rganish"
                ],
                "correct": 0,
                "explanation": "Supervised Learning - bu algoritmga to'g'ri javoblar (labels) bilan ma'lumot berib o'rgatish usuli."
            },
            "overfitting": {
                "question": "Overfitting qachon yuz beradi?",
                "options": [
                    "Model juda oddiy bo'lsa",
                    "Model train ma'lumotni juda yaxshi eslab qolsa",
                    "Ma'lumot juda ko'p bo'lsa",
                    "Kompyuter sekin ishlasa"
                ],
                "correct": 1,
                "explanation": "Overfitting - model train ma'lumotlarini juda yaxshi eslab qoladi, lekin yangi ma'lumotlarda yomon ishlaydi."
            }
        }
        
        return quizzes.get(topic, None)
