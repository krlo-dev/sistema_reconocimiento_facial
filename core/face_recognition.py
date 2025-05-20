import face_recognition
import cv2

def capture_face_encoding():
    video = cv2.VideoCapture(0)
    print("Capturando rostro. Presiona 'q' para capturar.")
    encoding = None

    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            # No frame válido, intentar siguiente iteración
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Registrar Rostro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if face_locations:
                encoding = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)[0]
            break

    video.release()
    cv2.destroyAllWindows()
    return encoding
