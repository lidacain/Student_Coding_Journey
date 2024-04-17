import face_recognition
import cv2
import os

# Папки для входных и выходных данных
input_folder = 'datas/detection_image/input'
output_folder = 'datas/detection_image/output/faces'

# Проверяем наличие выходной папки, и если её нет, создаём
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Список с известными лицами
known_faces = []

# Проходим по каждому файлу в папке с изображениями
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg"):
        # Полный путь к файлу
        image_path = os.path.join(input_folder, filename)

        # Загрузка изображения с помощью библиотеки face_recognition
        image = face_recognition.load_image_file(image_path)

        # Нахождение лиц в текущем кадре
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Проверяем, есть ли уникальные лица на этом изображении
        unique_faces = []
        for i, face_encoding in enumerate(face_encodings):
            # Проверка, есть ли уже такое лицо в списке известных
            matches = any(
                face_recognition.compare_faces(known_face, face_encoding)
                for known_face in known_faces
            )

            if not matches:
                unique_faces.append((face_locations[i], face_encoding))

        # Работа с уникальными лицами
        for (top, right, bottom, left), face_encoding in unique_faces:
            # Рисует красный квадрат на картинке по координатам
            cv2.rectangle(
                image,
                (left, top),
                (right, bottom),
                (0, 0, 255),
                2
            )

            # Сохранение изображения лица на диск в директории selected
            face_output_path = os.path.join(output_folder, 'face_{}_{}'.format(filename, len(known_faces)))
            cv2.imwrite(face_output_path + '.jpg', image[top:bottom, left:right])

            # Добавляем уникальные лица в список известных
            known_faces.append(face_encoding)

            # Информируем консоль
            print('\033[92m' + face_output_path + '\033[0m')
