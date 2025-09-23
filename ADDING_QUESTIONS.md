# Adding New Questions to the Survey

This guide shows how to easily add new questions to the survey system. The system is designed to scale to 100-200+ questions with minimal effort.

## Step 1: Add Question to QUESTIONS_STRUCTURE

In `app.py`, add your new question to the `QUESTIONS_STRUCTURE` dictionary:

```python
QUESTIONS_STRUCTURE = {
    # ... existing questions ...
    
    # Example: Text Question
    "city": {
        "question": "شهر محل زندگی شما کجاست؟",
        "type": "text",
        "field_name": "city"
    },
    
    # Example: Radio Question (Multiple Choice)
    "education": {
        "question": "میزان تحصیلات شما چیست؟",
        "type": "radio",
        "options": ["دیپلم", "کارشناسی", "کارشناسی ارشد", "دکترا"],
        "field_name": "education",
        "values": ["diploma", "bachelor", "master", "phd"]
    },
    
    # Example: Number Question
    "income": {
        "question": "درآمد ماهیانه شما چقدر است؟",
        "type": "number",
        "field_name": "income"
    },
    
    # Example: Conditional Question
    "years_experience": {
        "question": "چند سال سابقه کار دارید؟",
        "type": "number",
        "field_name": "years_experience",
        "depends_on": "is_employed",
        "depends_value": "yes"
    }
}
```

## Step 2: Add HTML Form Fields (Optional for Voice Mode)

If you want traditional form input in addition to voice, add the form fields to `templates/survey.html`:

```html
<!-- Example: Text Input -->
<div class="form-group">
    <label for="city">شهر محل زندگی:</label>
    <input type="text" id="city" name="city">
    
    <!-- Voice Section -->
    <div class="voice-section voice-mode" id="voice-section-city">
        <div class="voice-controls">
            <button type="button" class="voice-btn record-btn" onclick="startRecording('city')">
                🎤 ضبط
            </button>
            <button type="button" class="voice-btn stop-btn" onclick="stopRecording('city')" disabled>
                ⏹️ توقف
            </button>
            <button type="button" class="voice-btn play-btn" onclick="playRecording('city')" disabled>
                ▶️ پخش
            </button>
            <button type="button" class="voice-btn send-voice-btn" onclick="sendVoiceAnswer('city')" disabled>
                📤 ارسال
            </button>
        </div>
        <div class="audio-preview" id="audio-preview-city"></div>
        <div class="voice-status" id="voice-status-city"></div>
    </div>
</div>

<!-- Example: Radio Input -->
<div class="form-group">
    <label>میزان تحصیلات شما چیست؟</label>
    <div class="radio-group">
        <div class="radio-option">
            <input type="radio" id="edu_diploma" name="education" value="diploma">
            <label for="edu_diploma">دیپلم</label>
        </div>
        <div class="radio-option">
            <input type="radio" id="edu_bachelor" name="education" value="bachelor">
            <label for="edu_bachelor">کارشناسی</label>
        </div>
        <!-- Add more options as needed -->
    </div>
    
    <!-- Voice Section -->
    <div class="voice-section voice-mode" id="voice-section-education">
        <!-- Same voice controls as above, but with onclick="startRecording('education')" etc. -->
    </div>
</div>
```

## Step 3: Update JavaScript Form Filling (Optional)

Add handling for your new questions in the `fillSingleFormField` function in `templates/survey.html`:

```javascript
function fillSingleFormField(questionId, answer) {
    if (!answer || answer === 'null') {
        return;
    }
    
    switch (questionId) {
        // ... existing cases ...
        
        case 'city':
            document.getElementById('city').value = answer;
            break;
            
        case 'education':
            // Handle radio buttons
            const radioButtons = document.querySelectorAll('input[name="education"]');
            radioButtons.forEach(radio => {
                if (radio.value === answer) {
                    radio.checked = true;
                }
            });
            break;
            
        case 'income':
            document.getElementById('income').value = answer;
            break;
            
        default:
            // Automatic handling - tries to find element with matching ID
            const element = document.getElementById(questionId);
            if (element) {
                if (element.type === 'radio') {
                    // Handle radio buttons automatically
                    const radios = document.querySelectorAll(`input[name="${questionId}"]`);
                    radios.forEach(radio => {
                        if (radio.value === answer) radio.checked = true;
                    });
                } else {
                    element.value = answer;
                }
            }
            break;
    }
}
```

## Step 4: Update Excel Export (Optional)

If you want the new questions saved to Excel, update the `response_data` in the `submit_survey()` function:

```python
response_data = {
    'نام و نام خانوادگی': name,
    'آیا شاغل هستید؟': 'بله' if is_employed == 'yes' else 'خیر',
    'شغل': '',
    'از سن': '',
    'تا سن': '',
    'شهر': request.form.get('city', ''),  # Add new field
    'تحصیلات': request.form.get('education', ''),  # Add new field
    'درآمد': request.form.get('income', ''),  # Add new field
    'تاریخ پاسخ': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
```

## Question Types

### Text Questions
```python
"question_name": {
    "question": "سوال شما به فارسی؟",
    "type": "text",
    "field_name": "question_name"
}
```

### Radio Questions (Multiple Choice)
```python
"question_name": {
    "question": "سوال انتخابی شما؟",
    "type": "radio",
    "options": ["گزینه ۱", "گزینه ۲", "گزینه ۳"],
    "field_name": "question_name",
    "values": ["option1", "option2", "option3"]
}
```

### Number Questions
```python
"question_name": {
    "question": "عدد مورد نظر چقدر است؟",
    "type": "number",
    "field_name": "question_name"
}
```

### Conditional Questions
```python
"question_name": {
    "question": "سوال وابسته؟",
    "type": "text",
    "field_name": "question_name",
    "depends_on": "parent_field",
    "depends_value": "yes"
}
```

## Testing New Questions

1. **Test Voice Processing:**
   ```python
   from app import create_single_question_prompt
   print(create_single_question_prompt('your_question_name'))
   ```

2. **Test API Response:**
   ```bash
   curl -X GET http://localhost:5000/api/questions
   ```

3. **Test Voice Recording:**
   - Start the app: `python app.py`
   - Go to `http://localhost:5000`
   - Enable voice mode
   - Try recording for your new question

## Benefits of This Approach

1. **Scalable**: Add 100-200 questions by just updating the dictionary
2. **Automatic Prompt Generation**: AI prompts are generated automatically
3. **Type-Aware**: Different question types get appropriate processing
4. **Voice-First**: Questions work in voice mode immediately
5. **Flexible**: Support for conditional questions, dependencies, etc.

## Advanced Features

### Custom Question Processing
For complex questions, you can add custom processing in `process_answer_for_question()`:

```python
def process_answer_for_question(answer_text, question_id):
    # Handle special cases
    if question_id == 'your_special_question':
        # Custom processing logic
        return process_special_question(answer_text)
    
    # Default processing
    return answer_text
```

### Bulk Question Import
You can even load questions from a JSON file:

```python
import json

# Load questions from file
with open('questions.json', 'r', encoding='utf-8') as f:
    QUESTIONS_STRUCTURE = json.load(f)
```

This system is designed to make adding questions as simple as possible while maintaining full voice processing capabilities!