from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
import tempfile
import json

app = Flask(__name__)
app.secret_key = 'survey_secret_key_2025'

# Excel file path
EXCEL_FILE = 'survey_responses.xlsx'

# Configure Gemini API
# You need to set your API key as an environment variable: GOOGLE_API_KEY
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Warning: GOOGLE_API_KEY environment variable not set")

# With the new generic approach, we don't need a complex question structure!
# Questions are now defined in the frontend JavaScript and sent to the API.

@app.route('/')
def survey():
    """Display the survey form"""
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit_survey():
    """Handle survey form submission"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        is_employed = request.form.get('is_employed')
        
        # Validate required fields
        if not name:
            flash('لطفاً نام و نام خانوادگی خود را وارد کنید.', 'error')
            return redirect(url_for('survey'))
        
        if not is_employed:
            flash('لطفاً به سوال اشتغال پاسخ دهید.', 'error')
            return redirect(url_for('survey'))
        
        # Prepare data to save
        response_data = {
            'نام و نام خانوادگی': name,
            'آیا شاغل هستید؟': 'بله' if is_employed == 'yes' else 'خیر',
            'شغل': '',
            'از سن': '',
            'تا سن': '',
            'تاریخ پاسخ': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # If employed, get additional information
        if is_employed == 'yes':
            job = request.form.get('job', '').strip()
            age_from = request.form.get('age_from', '').strip()
            age_to = request.form.get('age_to', '').strip()
            
            if not job:
                flash('لطفاً شغل خود را مشخص کنید.', 'error')
                return redirect(url_for('survey'))
            
            if not age_from or not age_to:
                flash('لطفاً محدوده سنی کار خود را مشخص کنید.', 'error')
                return redirect(url_for('survey'))
            
            try:
                age_from_int = int(age_from)
                age_to_int = int(age_to)
                if age_from_int > age_to_int:
                    flash('سن شروع نمی‌تواند بیشتر از سن پایان باشد.', 'error')
                    return redirect(url_for('survey'))
            except ValueError:
                flash('لطفاً سن‌ها را به صورت عددی وارد کنید.', 'error')
                return redirect(url_for('survey'))
            
            response_data['شغل'] = job
            response_data['از سن'] = age_from
            response_data['تا سن'] = age_to
        
        # Save to Excel
        save_to_excel(response_data)
        
        flash('پاسخ شما با موفقیت ثبت شد. متشکریم!', 'success')
        return redirect(url_for('survey'))
        
    except Exception as e:
        flash(f'خطا در ثبت پاسخ: {str(e)}', 'error')
        return redirect(url_for('survey'))

def save_to_excel(response_data):
    """Save response data to Excel file"""
    # Create DataFrame from response
    df_new = pd.DataFrame([response_data])
    
    # Check if file exists
    if os.path.exists(EXCEL_FILE):
        # Load existing data and append
        df_existing = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        # Create new file
        df_combined = df_new
    
    # Save to Excel
    df_combined.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

@app.route('/results')
def view_results():
    """View survey results (optional feature)"""
    try:
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            return f"<h2>نتایج نظرسنجی</h2><br>تعداد پاسخ‌ها: {len(df)}<br><br><a href='/'>بازگشت به نظرسنجی</a>"
        else:
            return "<h2>هنوز پاسخی ثبت نشده است</h2><br><a href='/'>بازگشت به نظرسنجی</a>"
    except Exception as e:
        return f"خطا در نمایش نتایج: {str(e)}"

# API endpoint removed - no longer needed with generic approach

@app.route('/process_voice', methods=['POST'])
def process_voice():
    """Process voice input using Gemini API"""
    try:
        if not GOOGLE_API_KEY:
            return jsonify({"error": "Google API key not configured"}), 500
        
        # Get audio file from request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        # Get question data from request
        question_text = request.form.get('question_text')
        question_type = request.form.get('question_type')  # text, number, radio, dropdown
        question_options = request.form.get('question_options', '')  # comma-separated options
        target_fields = request.form.get('target_fields')  # comma-separated field names
        
        if not question_text or not question_type or not target_fields:
            return jsonify({"error": "Missing question data"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            audio_file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Process with Gemini using generic approach
            result = process_audio_with_gemini_generic(
                temp_file_path, 
                question_text, 
                question_type, 
                question_options, 
                target_fields
            )
            return jsonify(result)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return jsonify({"error": f"Voice processing failed: {str(e)}"}), 500

def process_audio_with_gemini_generic(audio_file_path, question_text, question_type, question_options, target_fields):
    """Process audio file with Gemini API using generic approach"""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        audio_part = {
            "mime_type": 'audio/webm',
            "data": audio_data
        }
        
        # Create generic prompt
        prompt = create_generic_prompt(question_text, question_type, question_options, target_fields)
        
        # Generate response
        response = model.generate_content([prompt, audio_part])
        print(f"Gemini response: {response.text}")
        
        # Parse the response
        answer_text = response.text.strip()
        
        # Process answer based on question type
        processed_answer = process_generic_answer(answer_text, question_type, target_fields)
        
        return {"success": True, "answer": processed_answer}
            
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return {"success": False, "error": str(e)}

def create_generic_prompt(question_text, question_type, question_options, target_fields):
    """Create a generic prompt for any question type"""
    
    prompt = f"""
You are a Persian/Farsi language assistant. Listen to the audio and extract the answer to this question:

Question: {question_text}
"""
    
    # Add instructions based on question type
    if question_type == 'text':
        prompt += """
Instructions:
1. Listen to the Persian/Farsi audio
2. find one word answer to the question base on the audio  
3. Return the text word exactly as spoken (in Persian/Farsi)
4. If no clear answer found, return "null"
"""
    
    elif question_type == 'number':
        prompt += """
Instructions:
1. Listen to the Persian/Farsi audio
2. Extract any numerical value mentioned
3. Return ONLY the number (no text)
4. If no number found or unclear, return "null"
"""
    
    elif question_type in ['radio', 'dropdown']:
        if question_options:
            options = [opt.strip() for opt in question_options.split(',') if opt.strip()]
            options_str = ", ".join(options)
            prompt += f"""
Available Options: {options_str}

Instructions:
1. Listen to the Persian/Farsi audio
2. Identify which option the user selected
3. Return ONLY the exact option text from the available options
4. If unclear or no match found, return "null"
"""
        else:
            prompt += """
Instructions:
1. Listen to the Persian/Farsi audio
2. Extract the selected option
3. Return the option exactly as spoken
4. If unclear, return "null"
"""
    
    # Special handling for multiple fields (like age range)
    fields = [f.strip() for f in target_fields.split(',') if f.strip()]
    if len(fields) > 1:
        prompt += f"""

Note: This question expects multiple values for fields: {', '.join(fields)}
Return your answer in JSON format like: {{{', '.join([f'"{field}": "value"' for field in fields])}}}
"""
    
    prompt += "\n\nReturn only the answer, no additional text or explanation."
    
    return prompt

def process_generic_answer(answer_text, question_type, target_fields):
    """Process the answer based on question type"""
    if not answer_text or answer_text.lower().strip() in ['null','']:
        return "null"
    
    answer_text = answer_text.strip()
    
    # Handle multiple fields (like age range)
    fields = [f.strip() for f in target_fields.split(',') if f.strip()]
    if len(fields) > 1:
        try:
            # Try to parse JSON response
            if answer_text.startswith('{') and answer_text.endswith('}'):
                parsed_data = json.loads(answer_text)
                return parsed_data
        except json.JSONDecodeError:
            pass
        # Fallback: return null for all fields
        return {field: "null" for field in fields}
    
    # Single field - return the answer as-is
    return answer_text

# def create_survey_prompt():
#     """Create a structured prompt for Gemini based on survey questions (legacy function)"""
#     prompt = """
# You are a Persian/Farsi language survey assistant. Your task is to transcribe the provided audio and extract answers to survey questions.

# Survey Questions:
# """
    
#     for key, question_data in QUESTIONS_STRUCTURE.items():
#         prompt += f"\n{question_data['field_name']}: {question_data['question']}"
#         if question_data['type'] == 'radio' and 'options' in question_data:
#             options_str = ", ".join(question_data['options'])
#             prompt += f" (Options: {options_str})"
#         elif question_data['type'] == 'number':
#             prompt += " (Number expected)"
#         prompt += "\n"
    
#     prompt += """
# Instructions:
# 1. Transcribe the audio content in Persian/Farsi
# 2. Extract answers for each question based on what the user said
# 3. For radio questions, match the user's response to the closest option and return the corresponding English value ("yes"/"no")
# 4. For text questions, return the exact text mentioned by the user
# 5. For number questions, extract the numerical value
# 6. If you cannot find an answer for a question, return "null" for that field
# 7. Return ONLY a valid JSON object with the extracted answers


# Return only the JSON object, no additional text or explanation.
# """
    
#     return prompt

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
