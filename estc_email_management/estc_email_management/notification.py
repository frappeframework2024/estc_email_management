# custom_app/custom_notification.py
import frappe
from frappe.email.doctype.notification.notification import Notification

class CustomNotification(Notification):
    def send_an_email(self, doc, context):
        
        from email.utils import formataddr

        from frappe.core.doctype.communication.email import _make as make_communication

        subject = self.subject
        if "{" in subject:
            subject = frappe.render_template(self.subject, context)

        attachments = self.get_attachment(doc)
        recipients, cc, bcc = self.get_list_of_recipients(doc, context)
        if not (recipients or cc or bcc):
            return

        sender = None
        message = frappe.render_template(self.message, context)
        if self.sender and self.sender_email:
            sender = formataddr((self.sender, self.sender_email))

        communication = None
        # Add mail notification to communication list
        # No need to add if it is already a communication.
        if doc.doctype != "Communication":
            communication = make_communication(
                doctype=doc.doctype,
                name=doc.name,
                content=message,
                subject=subject,
                sender=sender,
                recipients=recipients,
                communication_medium="Email",
                send_email=False,
                attachments=attachments,
                cc=cc,
                bcc=bcc,
                communication_type="Automated Message",
                
            ).get("name")

        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            sender=sender,
            cc=cc,
            bcc=bcc,
            message=message,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
            attachments=attachments,
            expose_recipients="header",
            print_letterhead=((attachments and attachments[0].get("print_letterhead")) or False),
            communication=communication,
            reply_to=doc.email_address
        )