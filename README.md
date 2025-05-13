# Smart Text Editor with Autocomplete

A modern, responsive text editor with powerful word suggestion/autocomplete functionality built with Python FastAPI backend and vanilla JavaScript frontend.

## Features
- Intelligent word suggestions with 300+ built-in words
- External API integration with DataMuse API as fallback
- Beautiful, modern UI with responsive design
- Dark mode support with theme persistence
- Mobile-friendly design that works on all devices
- Real-time word suggestions and smart positioning
- Keyboard navigation (arrow keys, enter, tab, escape)
- Word and character count tracking
- Text auto-save functionality  
- Export/download text functionality
- Copy to clipboard with visual feedback
- Click to select suggestions
- Proper cursor positioning after selection
- Debounce for better performance
- Loading indicators
- Smart suggestion scrolling
- CSS variables for easy theme customization

## Setup Instructions

### Backend Setup
1. Navigate to the Backend directory:
```bash
cd Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the server:
```bash
python server.py
```

The backend will run on http://localhost:5000

### Frontend Setup
1. Simply open `frontend/index.html` in a web browser
2. Works on both desktop and mobile browsers

## How to Use
1. Start typing in the editor
2. When you type at least 2 characters, the app will suggest words
3. Use arrow keys to navigate suggestions (suggestions will auto-scroll)
4. Press Enter or Tab to select a suggestion
5. Press Escape to hide suggestions
6. Toggle dark/light mode with the theme switch
7. Use toolbar buttons to clear, copy, or download your text
8. Your text will be automatically saved and restored when you return

## Mobile-specific Features
- Touch-friendly interface with appropriate button sizes
- Optimized suggestion positioning for small screens
- Responsive layout that adapts to different screen sizes
- Improved scrolling behavior within the editor
- Automatic suggestion hiding when editor is not in view

## Customization
To add more words to the autocomplete dictionary, modify the `dictionary` object in `server.py`. The words are organized by first letter for better performance.

You can also customize the visual appearance by modifying the CSS variables in the `:root` selector in `index.html`.

## API Integration
The editor uses two endpoints:
1. `/autocomplete-api` - First attempts to use local dictionary, then falls back to DataMuse API
2. `/autocomplete` - Uses only the local dictionary

The frontend tries the enhanced API endpoint first and falls back to the local endpoint if there's an error.

## Performance Optimization
- Words are grouped by starting letter for faster filtering
- Suggestions are limited to 10 items for better performance
- Typing has a 300ms debounce to prevent excessive API calls
- Regular expression matching for better text splitting
- Smart fallback mechanism when API calls fail
- Efficient DOM manipulation for better mobile performance 