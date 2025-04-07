import base64
from io import BytesIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, From, To, Subject, HtmlContent,
    Attachment, ContentId, Disposition, FileContent, FileName, FileType
)

def attach_image_cid_from_memory(fig, image_cid):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode()

    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('image/png')
    attachment.file_name = FileName(f"{image_cid}.png")
    attachment.disposition = Disposition('inline')
    attachment.content_id = ContentId(image_cid)
    return attachment

def send_email(html_report, fig1, fig2, sender_email, sender_name, recipient_email,
               recipient_name, subject, api_key):

    to_emails = [To(email=recipient_email, name=recipient_name)]
    message = Mail(
        from_email=From(sender_email, sender_name),
        to_emails=to_emails,
        subject=Subject(subject),
        html_content=HtmlContent(html_report),
    )

    message.attachment = [
        attach_image_cid_from_memory(fig1, 'graph1'),
        attach_image_cid_from_memory(fig2, 'graph2')
    ]

    try:
        sendgrid_client = SendGridAPIClient(api_key)
        response = sendgrid_client.send(message=message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
