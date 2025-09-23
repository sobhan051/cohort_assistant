# Persian Survey Application with Voice Mode

A Flask-based survey application that supports both traditional form input and voice input using Google Gemini-1.5-flash for audio transcription and answer extraction.

## Features

- **Traditional Survey Mode**: Regular form inputs for survey questions
- **Voice Mode**: Record audio answers and automatically extract responses using AI
- **Persian Language Support**: Fully supports Persian/Farsi language
- **Real-time Audio Preview**: Listen to recordings before sending
- **Excel Export**: Automatically saves all responses to Excel file
- **Conditional Questions**: Shows/hides questions based on previous answers
- **Scalable Question Structure**: Easy to add more questions (up to 100-200)

## Requirements

- Python 3.7+
- Google Gemini API key
- Modern web browser with microphone access

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

### 3. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**Windows (CMD):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Usage

### 1. Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 2. Using the Survey

#### Traditional Mode:
- Fill out the form fields manually
- Click "ارسال پاسخ" to submit

#### Voice Mode:
1. Click "🎤 فعال کردن حالت صوتی" to enable voice mode
2. For each question:
   - Click "🎤 ضبط" to start recording
   - Speak your answer in Persian
   - Click "⏹️ توقف" to stop recording
   - Click "▶️ پخش" to preview your recording (optional)
   - Click "📤 ارسال" to process with AI and auto-fill the form
3. Submit the form when all answers are filled

### 3. Current Questions

1. **نام و نام خانوادگی**: Name field
2. **آیا شاغل هستید؟**: Employment status (Yes/No)
3. **شغل شما چیست؟**: Job title (shown if employed)
4. **از چه سنی تا چه سنی**: Age range for work (shown if employed)

## Voice Processing

The application uses Google Gemini-1.5-flash model to:
1. Transcribe Persian audio to text
2. Extract answers for each question
3. Match responses to the appropriate form fields
4. Return "null" for questions that cannot be answered from the audio

## Adding More Questions

With the new simple approach, adding questions is super easy! Just add to the JavaScript in `templates/survey.html`:

```javascript
// In getQuestionData() function, add:
'new_question': {
    text: 'سوال جدید',
    type: 'text',  // or 'radio', 'number', 'dropdown'
    options: 'گزینه ۱,گزینه ۲',  // for radio/dropdown
    fields: 'new_question'  // or 'field1,field2' for multiple fields
}
```

That's it! The backend automatically handles any question type.

## Files Structure

```
cohort/
├── app.py                 # Main Flask application
├── templates/
│   └── survey.html       # HTML template with voice functionality
├── requirements.txt      # Python dependencies
├── setup_env.py         # Environment setup script
├── README.md            # This file
└── survey_responses.xlsx # Generated Excel file with responses
```

## Browser Compatibility

Voice recording requires a modern browser with:
- MediaRecorder API support
- getUserMedia API support
- Microphone permission

Tested on:
- Chrome 80+
- Firefox 70+
- Edge 80+

## Troubleshooting

### Voice Recording Issues

1. **Microphone not accessible**: Ensure browser has microphone permission
2. **Recording not working**: Check if HTTPS is enabled (required for some browsers)
3. **API errors**: Verify GOOGLE_API_KEY is set correctly

### Audio Format Issues

The application uses WebM format for audio recording. If you encounter issues:
- Try using Chrome or Edge browsers
- Check browser console for error messages

### API Issues

1. **"Google API key not configured"**: Set the GOOGLE_API_KEY environment variable
2. **Rate limiting**: Gemini API has usage limits, wait and try again
3. **Invalid response**: The AI might return non-JSON response, check logs

## Excel Output

Responses are automatically saved to `survey_responses.xlsx` with columns:
- نام و نام خانوادگی
- آیا شاغل هستید؟  
- شغل
- از سن
- تا سن
- تاریخ پاسخ

## Development

To extend the application:
1. Add questions to `QUESTIONS_STRUCTURE`
2. Update HTML template with new form fields
3. Add voice sections for new questions
4. Update JavaScript to handle new question IDs

## License

This project is open source and available under the MIT License.