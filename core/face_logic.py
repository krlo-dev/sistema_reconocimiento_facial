import os
import cv2
import face_recognition
from core.database import add_user_to_db, remove_user_from_db, get_all_users, save_access

DATA_DIR = os.path.join("data", "faces")

def register_user(name, user_id, frame):
    if frame is None:
        print("Frame nulo, no se puede registrar.")
        return False

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    if len(encodings) == 0:
        print("No se detectó rostro para registrar.")
        return False
    encoding = encodings[0]

    user_folder = os.path.join(DATA_DIR, user_id)
    os.makedirs(user_folder, exist_ok=True)
    img_path = os.path.join(user_folder, f"{name}.jpg")
    cv2.imwrite(img_path, frame)

    add_user_to_db(name, user_id, encoding)
    print(f"Usuario {name} registrado correctamente.")
    return True

def delete_user(name, user_id):
    remove_user_from_db(name, user_id)
    user_folder = os.path.join(DATA_DIR, user_id)
    if os.path.exists(user_folder):
        import shutil
        shutil.rmtree(user_folder)
    print(f"Usuario {name} eliminado.")

def recognize_face(frame):
    if frame is None:
        print("Frame nulo en recognize_face.")
        return False, None, frame

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    known_users = get_all_users()

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([user['encoding'] for user in known_users], face_encoding)
        name = "Desconocido"
        user_id = None
        if True in matches:
            first_match_index = matches.index(True)
            user = known_users[first_match_index]
            name = user['name']
            user_id = user['user_id']
            save_access(name, user_id)

        color = (0, 255, 0) if name != "Desconocido" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    return True, user_id, frame
