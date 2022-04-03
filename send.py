from twilio.rest import Client

def Send(mes, num):
    # On stocke notre SID et notre jeton dans des variables
    sid = "AC739f0f58f5a01f17f9ce068834d0263d"
    token = "791263349e5d9f2eea6a54d73668b82e"

    # Et on initialise notre objet client avec nos identifiants.
    client = Client(sid,token)

    # Puis on forge notre premier message
    message = client.messages.create(
    
        # destinataire
        to=num,
    
        # expéditeur (votre n° Twilio)
        from_="+12342564094",
    
        # votre message
        body=mes)

    # J'affiche l'ID du message envoyé
    print(message.sid)