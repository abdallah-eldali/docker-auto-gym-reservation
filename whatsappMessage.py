from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "[DELETED]"
auth_token = "[DELETED]"
client = Client(account_sid, auth_token)

def sendMessage(message: str):
    client.messages.create(from_='whatsapp:[DELETED]',
                           body=message,
                           to='whatsapp:[DELETED]'
                           )