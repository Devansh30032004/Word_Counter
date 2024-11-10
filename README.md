# Word Counter: Intelligent Word Frequency Analyzer 🔍

**Word Counter** is a web-based application for analyzing word frequency from any webpage URL. It delivers two customizable top-10 word lists: one with all words and another excluding common words, enhancing insights by focusing on impactful terms. The app also fetches meanings for the most frequent unique words and presents results in a clean, professional table format. Perfect for writers, content strategists, and language enthusiasts seeking deeper text analysis in a user-friendly design!

## Features:
- 📊 **Top-10 Word Frequency Tables** (With & Without Common Words)
- 📖 **Word Meanings** for Key Terms
- ⏳ **Loading Spinner** for Smooth User Experience

## Tech Stack:
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **API**: Word Meaning API (for fetching word definitions)

## Installation:
1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/Word Counter.git
    cd Word Counter
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the development server:
    ```bash
    python manage.py runserver
    ```

4. Open `http://127.0.0.1:8000/` in your browser to start using Count_IT.

## How it works:
1. Enter any URL in the input field.
2. The backend fetches the content and calculates the frequency of words.
3. The results display in two tables:
   - **Top 10 Most Frequent Words (Including Common Words)**
   - **Top 10 Most Frequent Words (Excluding Common Words)**
4. Meaning of the top filtered words is displayed below the tables.

---

Feel free to contribute and create issues for any bugs or enhancements!
