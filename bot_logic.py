"""
Bot Logic - AI Tutoring Bot asosiy mantiqiy qismi
Bu modul foydalanuvchi savollariga javob berish logikasini boshqaradi
"""

import re
from ml_concepts import MLConcepts

class AITutor:
    """
    AI Tutor - Machine Learning va Python o'rgatuvchi bot
    """
    
    def __init__(self):
        self.concepts = MLConcepts()
        self.conversation_history = []
        self.current_topic = None
        self.user_progress = {
            'topics_learned': [],
            'quizzes_completed': 0,
            'correct_answers': 0
        }
        
        # Greeting javoblari
        self.greetings = [
            "salom", "assalomu alaykum", "hello", "hi", "hey"
        ]
        
        # Mavzular ro'yxati
        self.topics = {
            "ml": ["machine learning", "mashina o'rganishi", "ml"],
            "supervised": ["supervised learning", "nazorat ostida", "supervised"],
            "unsupervised": ["unsupervised", "nazorat ostida bo'lmagan"],
            "neural": ["neural network", "neyron tarmoq", "neural"],
            "regression": ["regression", "regressiya"],
            "classification": ["classification", "klassifikatsiya"],
            "python": ["python", "coding", "dasturlash"],
            "numpy": ["numpy", "array"],
            "pandas": ["pandas", "dataframe", "data"]
        }
    
    def process_message(self, user_message):
        """
        Foydalanuvchi xabarini qayta ishlash va javob berish
        
        Args:
            user_message (str): Foydalanuvchi xabari
        
        Returns:
            dict: Javob va qo'shimcha ma'lumotlar
        """
        # Xabarni tozalash
        message = user_message.lower().strip()
        
        # Conversation history ga qo'shish
        self.conversation_history.append({
            'user': user_message,
            'timestamp': self._get_timestamp()
        })
        
        # Salomlashuvni tekshirish
        if any(greeting in message for greeting in self.greetings):
            return self._greeting_response()
        
        # Yordam so'rovi
        if any(word in message for word in ["yordam", "help", "nima qila olasan"]):
            return self._help_response()
        
        # Mavzular ro'yxatini so'rash
        if any(word in message for word in ["mavzular", "topics", "ro'yxat"]):
            return self._topics_list_response()
        
        # Konsept qidirish
        for topic_key, keywords in self.topics.items():
            if any(keyword in message for keyword in keywords):
                return self._concept_response(topic_key)
        
        # Misol so'rash
        if any(word in message for word in ["misol", "example", "kod", "code"]):
            return self._example_response()
        
        # Test so'rash
        if any(word in message for word in ["test", "quiz", "savol"]):
            return self._quiz_response()
        
        # Tushunarsiz xabar uchun
        return self._default_response(message)
    
    def _greeting_response(self):
        """
        Salomlashish javobini qaytarish
        """
        return {
            'type': 'greeting',
            'message': """
🤖 Assalomu alaykum! Men AI Tutoring Bot - sizning Machine Learning va Python o'qituvchingizman!

Men sizga quyidagilar bilan yordam bera olaman:
✅ Machine Learning konseptlarini tushuntirish
✅ Python kodlarini o'rgatish
✅ Misollar va vizualizatsiya
✅ Testlar orqali bilimingizni tekshirish

Boshlash uchun "mavzular" deb yozing yoki biror mavzu nomini ayting!
            """,
            'suggestions': [
                "Mavzular ro'yxati",
                "Machine Learning nima?",
                "Python misollari",
                "Test olish"
            ]
        }
    
    def _help_response(self):
        """
        Yordam javobini qaytarish
        """
        return {
            'type': 'help',
            'message': """
📚 **Yordam va Ko'rsatmalar**

**Men qanday yordam bera olaman:**

1️⃣ **Konseptlarni tushuntirish:**
   - "Supervised Learning nima?"
   - "Neural Network tushuntir"
   - "Overfitting haqida"

2️⃣ **Python kodlari:**
   - "NumPy misoli"
   - "Pandas kod"
   - "Python asoslari"

3️⃣ **Testlar:**
   - "Test ol"
   - "Savol ber"

4️⃣ **Mavzular:**
   - "Mavzular ro'yxati"
   - "Nima o'rganishim mumkin?"

**Maslahatlar:**
💡 Aniq savol bering
💡 Bitta mavzudan boshlang
💡 Kodni sinab ko'ring
💡 Testlar orqali bilimingizni tekshiring
            """,
            'suggestions': [
                "Mavzular",
                "Supervised Learning",
                "Python misoli",
                "Test"
            ]
        }
    
    def _topics_list_response(self):
        """
        Mavzular ro'yxatini qaytarish
        """
        concepts_list = self.concepts.get_all_concepts_list()
        
        message = "📖 **Machine Learning Mavzulari:**\n\n"
        
        for idx, concept in enumerate(concepts_list, 1):
            message += f"{idx}. **{concept['uz_name']}** ({concept['name']})\n"
            message += f"   {concept['description']}\n\n"
        
        message += "\n💻 **Python Darslari:**\n"
        message += "1. Python Asoslari\n"
        message += "2. NumPy\n"
        message += "3. Pandas\n"
        message += "4. Scikit-learn\n"
        
        return {
            'type': 'topics',
            'message': message,
            'concepts': concepts_list,
            'suggestions': [
                "Supervised Learning",
                "Neural Networks",
                "Python asoslari",
                "NumPy misoli"
            ]
        }
    
    def _concept_response(self, topic_key):
        """
        Konsept haqida batafsil javob
        """
        # Mavzu asosida konsept topish
        concept_map = {
            "ml": "supervised_learning",
            "supervised": "supervised_learning",
            "unsupervised": "unsupervised_learning",
            "neural": "neural_networks",
            "regression": "regression",
            "classification": "classification",
            "python": "basics",
            "numpy": "numpy",
            "pandas": "pandas"
        }
        
        concept_name = concept_map.get(topic_key)
        
        # ML konsept yoki Python darsmi?
        if concept_name in ["basics", "numpy", "pandas"]:
            lesson = self.concepts.get_python_lesson(concept_name)
            if lesson:
                message = f"# {lesson['title']}\n\n"
                message += f"**Mavzular:** {', '.join(lesson['topics'])}\n\n"
                message += "**Kod misoli:**\n```python\n"
                message += lesson['code_example']
                message += "\n```\n\n"
                message += "Ushbu kodni o'zingiz sinab ko'ring! 🚀"
                
                return {
                    'type': 'lesson',
                    'message': message,
                    'code': lesson['code_example'],
                    'suggestions': [
                        "Boshqa misol",
                        "Test ol",
                        "Keyingi mavzu"
                    ]
                }
        else:
            concept = self.concepts.get_concept(concept_name)
            if concept:
                self.current_topic = concept_name
                self.user_progress['topics_learned'].append(concept_name)
                
                message = f"# {concept['uz']} ({concept_name.replace('_', ' ').title()})\n\n"
                message += concept['description']
                
                if 'types' in concept:
                    message += f"\n\n**Turlari:**\n"
                    for t in concept['types']:
                        message += f"- {t}\n"
                
                if 'algorithms' in concept:
                    message += f"\n\n**Algoritmlar:**\n"
                    for alg in concept['algorithms']:
                        message += f"- {alg}\n"
                
                if 'solutions' in concept:
                    message += f"\n\n**Yechimlar:**\n"
                    for sol in concept['solutions']:
                        message += f"- {sol}\n"
                
                return {
                    'type': 'concept',
                    'message': message,
                    'concept': concept,
                    'suggestions': [
                        "Misol ko'rsat",
                        "Test ol",
                        "Boshqa mavzu"
                    ]
                }
        
        return self._default_response(topic_key)
    
    def _example_response(self):
        """
        Kod misoli berish
        """
        if self.current_topic:
            # Joriy mavzu bo'yicha misol
            examples = {
                "supervised_learning": """
# Supervised Learning misoli - Uy narxini bashorat qilish

from sklearn.linear_model import LinearRegression
import numpy as np

# Ma'lumotlar: [Maydon (m²)]
X = np.array([[50], [80], [100], [120], [150]])

# Javoblar: [Narx (million)]
y = np.array([30, 45, 55, 65, 80])

# Model yaratish
model = LinearRegression()
model.fit(X, y)

# Yangi uyning narxini bashorat qilish
yangi_uy = np.array([[90]])
narx = model.predict(yangi_uy)

print(f"90 m² uy narxi: {narx[0]:.2f} million")
                """,
                "classification": """
# Classification misoli - Email spam aniqlash

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# Email matnlari
emails = [
    "Siz yutdingiz 1 million dollar!",
    "Bugungi uchrashuv soat 3 da",
    "Bepul iPhone oling hozir!",
    "Hisobot tayyor, ko'rib chiqing"
]

# Labels: 1 = spam, 0 = normal
labels = [1, 0, 1, 0]

# Matnni raqamlarga aylantirish
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Model o'rgatish
model = MultinomialNB()
model.fit(X, labels)

# Yangi emailni tekshirish
test_email = ["Sizga bepul kompyuter!"]
test_X = vectorizer.transform(test_email)
result = model.predict(test_X)

print("Spam" if result[0] == 1 else "Normal")
                """
            }
            
            code = examples.get(self.current_topic, "# Misol topilmadi")
        else:
            # Umumiy misol
            code = """
# Python ML asoslari misoli

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Ma'lumot yaratish
X = np.random.rand(100, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# Train va test ga bo'lish
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model o'rgatish
model = LogisticRegression()
model.fit(X_train, y_train)

# Aniqlik
accuracy = model.score(X_test, y_test)
print(f"Aniqlik: {accuracy * 100:.2f}%")
            """
        
        return {
            'type': 'example',
            'message': "**Kod misoli:**\n```python\n" + code + "\n```\n\nBu kodni Python muhitida sinab ko'ring!",
            'code': code,
            'suggestions': [
                "Tushuntir",
                "Boshqa misol",
                "Test ol"
            ]
        }
    
    def _quiz_response(self):
        """
        Test savoli berish
        """
        if self.current_topic:
            quiz = self.concepts.get_quiz_question(self.current_topic)
            if quiz:
                message = f"**📝 Test savoli:**\n\n{quiz['question']}\n\n"
                for idx, option in enumerate(quiz['options'], 1):
                    message += f"{idx}. {option}\n"
                
                return {
                    'type': 'quiz',
                    'message': message,
                    'quiz': quiz,
                    'suggestions': ["1", "2", "3", "4"]
                }
        
        return {
            'type': 'quiz',
            'message': "Avval biror mavzu o'rganing, keyin test oling! 📚",
            'suggestions': ["Mavzular", "Supervised Learning"]
        }
    
    def _default_response(self, message):
        """
        Tushunarsiz xabar uchun javob
        """
        # Konsept qidirish
        results = self.concepts.search_concept(message)
        
        if results:
            response = "Men quyidagi mavzularni topdim:\n\n"
            for result in results[:3]:
                response += f"• **{result['uz_name']}** - {result['description']}\n\n"
            response += "\nQaysi birini batafsil tushuntirishimni xohlaysiz?"
            
            return {
                'type': 'search_results',
                'message': response,
                'results': results,
                'suggestions': [r['uz_name'] for r in results[:3]]
            }
        
        return {
            'type': 'unknown',
            'message': """
Kechirasiz, men bu savolni to'liq tushunmadim. 😅

Siz quyidagilarni sinab ko'ring:
• "mavzular" - barcha mavzularni ko'rish
• "yordam" - ko'rsatmalar olish
• Aniq savol bering (masalan: "Supervised Learning nima?")
            """,
            'suggestions': [
                "Mavzular",
                "Yordam",
                "Machine Learning nima?"
            ]
        }
    
    def check_quiz_answer(self, quiz, user_answer):
        """
        Test javobini tekshirish
        """
        try:
            answer_index = int(user_answer) - 1
            is_correct = answer_index == quiz['correct']
            
            self.user_progress['quizzes_completed'] += 1
            if is_correct:
                self.user_progress['correct_answers'] += 1
            
            response = "✅ To'g'ri!" if is_correct else "❌ Noto'g'ri."
            response += f"\n\n**Tushuntirish:** {quiz['explanation']}"
            
            return {
                'correct': is_correct,
                'message': response
            }
        except (ValueError, IndexError):
            return {
                'correct': False,
                'message': "Iltimos, 1-4 orasida raqam kiriting."
            }
    
    def get_progress(self):
        """
        Foydalanuvchi progressini olish
        """
        total_quizzes = self.user_progress['quizzes_completed']
        correct = self.user_progress['correct_answers']
        accuracy = (correct / total_quizzes * 100) if total_quizzes > 0 else 0
        
        return {
            'topics_learned': len(self.user_progress['topics_learned']),
            'quizzes_completed': total_quizzes,
            'correct_answers': correct,
            'accuracy': accuracy
        }
    
    def _get_timestamp(self):
        """
        Hozirgi vaqtni olish
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
