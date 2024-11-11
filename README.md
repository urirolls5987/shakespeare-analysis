# Shakespeare Interactive

An interactive web application for exploring and analyzing Shakespeare's plays, built with Streamlit and Python.

## Features

- Navigate through acts and scenes
- Multiple text display modes including POS tagging
- Character analysis and interaction networks
- Scene metrics and visualizations
- Stage direction highlighting
- Line numbering

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shakespeare-interactive.git
cd shakespeare-interactive
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

## Project Structure

```
shakespeare-interactive/
├── src/
│   ├── config/               # Configuration files
│   ├── data/                # Data loading and parsing
│   ├── models/              # NLP model management
│   ├── services/            # Analysis services
│   ├── ui/                  # UI components
│   └── utils/               # Utility functions
├── plays/                   # Play text files
├── tests/                   # Test files
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
app.py                 # Main application file
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.