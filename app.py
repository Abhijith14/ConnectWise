from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import os

df = pd.read_csv('company copy.csv', header=None)

# Create a dictionary to store the company names and emails
company_emails_dict = {}

# Iterate through the DataFrame and populate the dictionary
for index, row in df.iterrows():
    company_name = row[0]
    emails = [row[col] for col in df.columns if pd.notna(row[col])][2:]
    company_emails_dict[company_name] = emails


for company_name, emails in company_emails_dict.items():
    print("Sending email to {}...".format(company_name))
    print("Emails: {}".format(emails))
    

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = os.environ["sender_email"]
    msg['To'] = ', '.join(emails)
    msg['Subject'] = "Seeking Opportunity to Demonstrate AI Expertise"

    # The email body
    message=f"""
        Dear Hiring Manager,

        I am writing to express my strong interest in opportunities at {company_name} where I can apply my specialized skills in artificial intelligence and machine learning. As a recent MSc graduate from the University of Aberdeen with a focus on AI, I am eager to join an innovative company like {company_name}.

        Throughout my master's studies, I honed expertise across computer vision, NLP, data analysis, and other areas of AI/ML. For example, I developed an automated driving simulation combining ML and multi-agent systems. I also created multiple real-world applications utilizing CV, NLP, and other cutting-edge techniques. These hands-on projects allowed me to gain valuable experience building end-to-end AI solutions.

        In addition to my academic background, I have collaborated on over 200 projects spanning automation, data science, and other domains. My work has been recognized through awards from SRM University and Intel India. I am adept at researching complex problems, designing optimized AI systems, and clearly presenting technical concepts to cross-functional partners.

        Given my specialized skills and passion for leveraging AI to solve real-world problems, I am confident I can add tremendous value to {company_name}. I would greatly appreciate the opportunity to showcase my expertise, whether through an in-person or virtual interview. My goal is to demonstrate how I can apply my strengths in AI/ML to drive innovation and excellence at {company_name}.

        I have attached my resume to provide further details on my qualifications. Please let me know if there is an open position or other opportunity where I could highlight my talents. I look forward to learning more about potential next steps.

        Thank you for your time and consideration.

    """

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Attach the doc file
    doc_file_path = 'Abhijith.docx'  # Replace with the actual path to your doc file
    with open(doc_file_path, 'rb') as doc_file:
        doc_attachment = MIMEApplication(doc_file.read(), _subtype="docx")
        doc_attachment.add_header('content-disposition', 'attachment', filename='resume.docx')
        msg.attach(doc_attachment)


    # Establish a connection to the Gmail SMTP server
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(os.environ["sender_email"], os.environ["app_password"])

        # Send the email to all recipients
        smtp_server.sendmail(os.environ["sender_email"], ', '.join(emails), msg.as_string())

        # Close the SMTP server
        smtp_server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred:", str(e))

    print("=====================================\n")
