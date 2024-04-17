import cv2
import numpy as np
import face_recognition
import imutils
from pathlib import Path
import os


def process_video(input_video, output_folder, known_faces, camera_name):
    capture = cv2.VideoCapture(str(input_video))

    frame_id = 0
    skip_frames = 0

    while True:
        frame_id += 1

        for _ in range(skip_frames):
            success, _ = capture.read()
            if not success:
                break

        success, frame = capture.read()

        if success:
            frame = imutils.resize(frame, width=800)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                top = max(0, top - 10)
                left = max(0, left - 10)
                bottom = min(frame.shape[0], bottom + 10)
                right = min(frame.shape[1], right + 10)

                distances = face_recognition.face_distance(known_faces, face_encoding)

                # Порог для считывания нового лица
                threshold = 0.6

                # Проверка на совпадение с известными лицами
                if np.min(distances) > threshold:
                    known_faces.append(face_encoding)

                    cv2.rectangle(
                        frame,
                        (left, top),
                        (right, bottom),
                        (255, 255, 255),
                        1
                    )

                    # Путь для сохранения изображения лица
                    face_path = os.path.join(output_folder,
                                             f'faces/{camera_name}/{input_video.stem}_{frame_id}_{len(known_faces)}.jpg')

                    # Сохранение изображения лица на диск
                    cv2.imwrite(face_path, frame[top:bottom, left:right])

                    print('\033[92m' + face_path + '\033[0m')

            frame_path = os.path.join(output_folder, f'frames/{camera_name}/{input_video.stem}_{frame_id}.jpg')
            cv2.imwrite(frame_path, frame)

        else:
            break


if __name__ == "__main__":
    output_folder = 'datas/detection_video/output'
    os.makedirs(os.path.join(output_folder, 'faces', 'cam_1'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'frames', 'cam_1'), exist_ok=True)

    known_faces = []

    process_video(Path('datas/detection_video/input/cam_1.MOV'), output_folder, known_faces, 'cam_1')

    for input_video, camera_name in zip(
            [Path('datas/detection_video/input/cam_2.MOV'), Path('datas/detection_video/input/cam_3.MOV')],
            ['cam_2', 'cam_3']):
        known_faces = []
        process_video(input_video, output_folder, known_faces, camera_name)
