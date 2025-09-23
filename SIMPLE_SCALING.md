# Simple Question Scaling Guide

With the new generic approach, adding questions is extremely simple! No complex configuration needed.

## Adding New Questions - 3 Easy Steps

### Step 1: Add Question to JavaScript
In `templates/survey.html`, add your question to the `getQuestionData()` function:

```javascript
function getQuestionData(questionId) {
    const questions = {
        // ... existing questions ...
        
        // Example: Text Question
        'city': {
            text: 'شهر محل زندگی شما کجاست؟',
            type: 'text',
            fields: 'city'
        },
        
        // Example: Radio Question
        'education': {
            text: 'میزان تحصیلات شما چیست؟',
            type: 'radio',
            options: 'دیپلم,کارشناسی,کارشناسی ارشد,دکترا',
            fields: 'education'
        },
        
        // Example: Number Question
        'income': {
            text: 'درآمد ماهیانه شما چقدر است؟',
            type: 'number',
            fields: 'income'
        },
        
        // Example: Dropdown Question
        'province': {
            text: 'استان محل زندگی شما کدام است؟',
            type: 'dropdown',
            options: 'تهران,اصفهان,شیراز,مشهد,تبریز',
            fields: 'province'
        },
        
        // Example: Multiple Fields (like age range)
        'work_experience': {
            text: 'از چه سالی تا چه سالی در این شغل کار کردید؟',
            type: 'number',
            fields: 'start_year,end_year'
        }
    };
    
    return questions[questionId] || {
        text: 'Question not found',
        type: 'text',
        fields: questionId
    };
}
```

### Step 2: Add HTML Form (Optional - for traditional input)
Add the HTML form field if you want traditional input too:

```html
<!-- Text Input -->
<div class="form-group">
    <label for="city">شهر محل زندگی:</label>
    <input type="text" id="city" name="city">
    
    <div class="voice-section voice-mode" id="voice-section-city">
        <!-- Voice controls -->
    </div>
</div>

<!-- Radio Input -->
<div class="form-group">
    <label>میزان تحصیلات:</label>
    <div class="radio-group">
        <div class="radio-option">
            <input type="radio" id="edu1" name="education" value="دیپلم">
            <label for="edu1">دیپلم</label>
        </div>
        <!-- Add more options -->
    </div>
    
    <div class="voice-section voice-mode" id="voice-section-education">
        <!-- Voice controls -->
    </div>
</div>
```

### Step 3: That's It!
Your question now works with voice mode automatically! The system will:
- Generate appropriate AI prompts based on question type
- Process voice input correctly
- Fill form fields automatically

## Question Types

### 1. Text Questions
```javascript
'question_id': {
    text: 'سوال شما؟',
    type: 'text',
    fields: 'field_name'
}
```

### 2. Number Questions
```javascript
'question_id': {
    text: 'عدد مورد نظر؟',
    type: 'number',
    fields: 'field_name'
}
```

### 3. Radio Questions
```javascript
'question_id': {
    text: 'سوال انتخابی؟',
    type: 'radio',
    options: 'گزینه ۱,گزینه ۲,گزینه ۳',
    fields: 'field_name'
}
```

### 4. Dropdown Questions
```javascript
'question_id': {
    text: 'انتخاب از فهرست؟',
    type: 'dropdown',
    options: 'آیتم ۱,آیتم ۲,آیتم ۳',
    fields: 'field_name'
}
```

### 5. Multiple Fields (Special Cases like Age Range)
```javascript
'question_id': {
    text: 'از ... تا ...؟',
    type: 'number',  // or 'text'
    fields: 'field1,field2'
}
```

## Benefits of This Approach

✅ **Simple**: Just add one object to JavaScript
✅ **No Backend Changes**: Python code handles everything generically  
✅ **Scalable**: Add 100+ questions easily
✅ **Type-Aware**: Different prompts for different question types
✅ **Voice-First**: Voice mode works immediately
✅ **Clean**: No complex configurations or mappings

## Example: Adding 5 New Questions

```javascript
// Add to getQuestionData() function:
'age': {
    text: 'سن شما چقدر است؟',
    type: 'number',
    fields: 'age'
},
'gender': {
    text: 'جنسیت شما چیست؟',
    type: 'radio',
    options: 'مرد,زن',
    fields: 'gender'
},
'city': {
    text: 'شهر محل زندگی شما؟',
    type: 'text',
    fields: 'city'
},
'favorite_color': {
    text: 'رنگ مورد علاقه شما؟',
    type: 'dropdown',
    options: 'قرمز,آبی,سبز,زرد,سفید,مشکی',
    fields: 'favorite_color'
},
'work_period': {
    text: 'از چه سالی تا چه سالی کار کردید؟',
    type: 'number',
    fields: 'work_start,work_end'
}
```

That's it! 5 new questions with full voice support added in under 2 minutes.

## How It Works

1. **JavaScript** sends: audio + question text + type + options + target fields
2. **Python** creates generic prompt based on question type
3. **Gemini AI** processes audio with the prompt
4. **System** returns answer and fills form fields automatically

This approach scales to hundreds of questions without any backend modifications!