from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ''#agrega tus datos de twilio
auth_token = '' #
client = Client(account_sid, auth_token)

response = VoiceResponse()
#Agrega el nuemro de twilio y el destinatario con codigo de pais
call = client.calls.create(
                        url='https://daffodil-dragonfly-4559.twil.io/assets/PruebaAudio.mp3',
                        to='+',
                        from_='+'
                    )
print(call.sid)
