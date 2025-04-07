from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd

from config_loader import load_config
from data_loader import load_data
from metrics_calculator import calculate_tables
from plot_generator import generate_plots_inline
from email_sender import send_email


def main():
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / 'config.yaml'
    template_dir = base_dir / 'templates'
    template_file = 'report_template_gmail.html'

    config = load_config(str(config_path))
    if not config:
        print("Failed to load configuration.")
        return

    data_conf = config.get('data', {})
    email_conf = config.get('email', {})
    report_conf = config.get('report', {})

    df = load_data(data_conf.get('file_path'))
    if df is None or df.empty:
        print("No data loaded. Exiting.")
        return

    tables = calculate_tables(df)
    fig1, fig2 = generate_plots_inline(df)

    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template(template_file)

    html_report = template.render(
        report_title="Marketing Analytics Report",
        report_period=f"{df['c_date'].min().date()} to {df['c_date'].max().date()}",
        generation_time=datetime.now().strftime('%Y-%m-%d %H:%M'),
        tabla1=tables['tabla1'],
        tabla2=tables['tabla2'],
        tabla3=tables['tabla3']
    )

    output_path = base_dir / 'final_report.html'
    with output_path.open('w', encoding='utf-8') as f:
        f.write(html_report)
    print(f"Report saved to: {output_path}")

    success = send_email(
        html_report=html_report,
        fig1=fig1,
        fig2=fig2,
        sender_email=email_conf.get('sender_email'),
        sender_name=email_conf.get('sender_name', 'Report Bot'),
        recipient_email=email_conf.get('recipient_email'),
        recipient_name=email_conf.get('recipient_name', 'Recipient'),
        subject=email_conf.get('subject', 'Marketing Report'),
        api_key=email_conf.get('password')
    )

    if success:
        print("Email sent successfully.")
    else:
        print("Failed to send the email.")


if __name__ == "__main__":
    main()
