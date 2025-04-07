# Email Report Generator

This project generates analytics reports in HTML format and sends them via email.

---

## Features

- Load data from CSV or Excel.
- Calculate metrics
- Generate a HTML report with tables and inline charts:
- Embed charts using CID-based inline images (Gmail-friendly)
- Email reports automatically using SendGrid

---

## Project Structure

```
.
├── config.yaml
├── templates/
│   └── report_template_gmail.html
├── src/
│   ├── main.py
│   ├── config_loader.py
│   ├── data_loader.py
│   ├── metrics_calculator.py
│   ├── plot_generator.py
└── README.md
```

---

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configuration
Edit `config.yaml`

---

## Sending the Report
To generate and send the report:
```bash
python src/main.py
```

## Gmail Compatibility Notes
- Uses table-based layout and inline CSS
- Embeds plots as CID images (not base64 or local paths)
