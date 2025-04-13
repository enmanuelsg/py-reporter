from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd

from config_loader import load_config
from data_loader import load_data
from metrics_calculator import calculate_tables
from plot_generator import generate_plots_inline
from email_sender import send_email
import time

def main():
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / 'config.yaml'

    print("Loading configuration...")
    time.sleep(0.5) # remove in prond env
    config = load_config(str(config_path))
    if not config:
        print("Failed to load configuration.")
        return
    print("Configuration [OK]")

    data_conf = config.get('data', {})
    email_conf = config.get('email', {})
    report_conf = config.get('report', {})

    print("Loading Data...")
    time.sleep(0.7) # remove in prond env
    df = load_data(data_conf['file_path'])
    if df is None or df.empty:
        print("No data loaded. Exiting.")
        return
    print("Data loaded [OK]")

    print("Generating tables and plot")
    time.sleep(0.7) # remove in prond env
    tables = calculate_tables(df)
    fig1, fig2 = generate_plots_inline(df)

    template_dir = base_dir / report_conf['template_dir']
    template_file = report_conf['template_name']
    output_path = base_dir / report_conf['output_file']
    print("Tables and plot [OK]")

    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template(template_file)

    print("Report Generation...")
    time.sleep(0.7) # remove in prond env
    html_report = template.render(
        report_title=report_conf['title'],
        report_period=f"{df['c_date'].min().date()} to {df['c_date'].max().date()}",
        generation_time=datetime.now().strftime('%Y-%m-%d %H:%M'),
        tabla1=tables['table1'],
        tabla2=tables['table2'],
        tabla3=tables['table3']
    )

    with output_path.open('w', encoding='utf-8') as f:
        f.write(html_report)
    print("Report generated [OK]")

    print("Sending email...")
    success = send_email(
        html_report=html_report,
        fig1=fig1,
        fig2=fig2,
        sender_email=email_conf['sender_email'],
        sender_name=email_conf['sender_name'],
        recipient_email=email_conf['recipient_email'],
        recipient_name=email_conf['recipient_name'],
        subject=email_conf['subject'],
        api_key=email_conf.get('password')
    )
    if success:
        print("Email sent successfully [OK]")
    else:
        print("Failed to send the email.")


if __name__ == "__main__":
    main()
