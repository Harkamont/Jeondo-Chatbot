# LLM Chatbot with Streamlit

A modern chatbot application built with Streamlit and OpenAI's language models.

## Features

- Clean, modern UI with Streamlit
- Powered by OpenAI's language models
- Environment-based configuration
- Modular and maintainable code structure

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── .env               # Environment variables (create this)
├── utils/
│   └── llm.py        # LLM interaction utilities
└── README.md         # This file
```

## Development

- The application uses environment variables for configuration
- LLM interactions are abstracted in the utils module
- The UI is built with Streamlit for easy customization

## License

MIT License # Jeondo-Chatbot
