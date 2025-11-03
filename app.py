"""
AI Tutoring Bot - Flask Web Application
Machine Learning va Python o'rgatuvchi chatbot
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from bot_logic import AITutor
import os
from datetime import datetime

# Flask ilovasini yaratish
app = Flask(__name__)
CORS(app)  # CORS'ni yoqish (frontend uchun)

# Bot instance yaratish
# Har bir session uchun o'z tutor'i bo'lishi kerak
tutors = {}

def get_tutor(session_id):
    """
    Session ID bo'yicha tutor olish yoki yaratish
    """
    if session_id not in tutors:
        tutors[session_id] = AITutor()
    return tutors[session_id]


@app.route('/')
def home():
    """
    Asosiy sahifa
    """
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chatbot API endpoint
    Foydalanuvchi xabarini qabul qilib, javob beradi
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Xabar bo\'sh bo\'lishi mumkin emas'
            }), 400
        
        # Tutor olish
        tutor = get_tutor(session_id)
        
        # Xabarni qayta ishlash
        response = tutor.process_message(user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/quiz/check', methods=['POST'])
def check_quiz():
    """
    Test javobini tekshirish
    """
    try:
        data = request.json
        quiz = data.get('quiz')
        user_answer = data.get('answer')
        session_id = data.get('session_id', 'default')
        
        if not quiz or not user_answer:
            return jsonify({
                'success': False,
                'error': 'Quiz yoki javob topilmadi'
            }), 400
        
        tutor = get_tutor(session_id)
        result = tutor.check_quiz_answer(quiz, user_answer)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/progress', methods=['GET'])
def get_progress():
    """
    Foydalanuvchi progressini olish
    """
    try:
        session_id = request.args.get('session_id', 'default')
        tutor = get_tutor(session_id)
        progress = tutor.get_progress()
        
        return jsonify({
            'success': True,
            'progress': progress
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """
    Sessionni qayta boshlash
    """
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in tutors:
            del tutors[session_id]
        
        return jsonify({
            'success': True,
            'message': 'Session qayta boshlandi'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Server ishlayotganini tekshirish
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(tutors)
    })


# Error handlers
@app.errorhandler(404)
def not_found(e):
    """
    404 xatosi
    """
    return jsonify({
        'success': False,
        'error': 'Sahifa topilmadi'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """
    500 xatosi
    """
    return jsonify({
        'success': False,
        'error': 'Server xatosi'
    }), 500


if __name__ == '__main__':
    # Development rejimida ishga tushirish
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║   🤖 AI Tutoring Bot - ML Teacher                ║
    ║   Machine Learning va Python o'rgatuvchi bot     ║
    ║                                                   ║
    ║   Server ishga tushdi!                           ║
    ║   URL: http://localhost:5000                     ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Debug rejimida ishga tushirish
    app.run(
        host='0.0.0.0',  # Barcha IP manzillardan kirish mumkin
        port=5000,
        debug=True  # Development uchun
    )
