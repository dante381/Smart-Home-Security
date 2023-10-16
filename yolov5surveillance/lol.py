import firebase_admin
from firebase_admin import credentials, messaging

firebase_cred = credentials.Certificate("yolov5surveillance\\smarthomesecurity-3e445-firebase-adminsdk-5w238-9ab3a99e6e.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)

message = messaging.Message(
    notification=messaging.Notification(
        title="SmartHomeSecurity",
        body="Unknown Person Detected"
    ),
    token="dyRJGmXyQf-Rs7iARH1WYj:APA91bGvHZlumqH9448MaAMIafqob5YsFtrE_-8LnTWtaU_4iXZNnGFLrWx9Q0AVTmSMCeZZ9E1sY8TZZV548fsjHrqnie4XjZIdzGLKZokLxu2JBD8oh9804pDFfDFiUGXLmmuwvU5u"
)
messaging.send(message)
