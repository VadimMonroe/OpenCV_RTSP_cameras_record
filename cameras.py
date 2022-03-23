import sys

from settings import *
import cv2
from ffpyplayer.player import MediaPlayer

"""
system arguments variables:
python cameras.py level_1

examples:
python cameras.py rec
python cameras.py show
"""
command = 'show' if len(sys.argv) == 1 else sys.argv[1]


def show_must_go_on() -> None:
    cameras = [f'rtsp://{ip_cam_1}:554/user={login}&password={password}&channel={_}' \
               f'&stream=0.sdp?real_stream--rtp-caching=100' for _ in range(1, 5)]
    cameras.append(f'rtsp://{ip_cam_2}:554/user={login}&password={password}&channel=1&stream=100.sdp')

    list_cam = [cv2.VideoCapture(_) for _ in cameras]

    """Настройки записи в файлы, fps=200 для быстрого просмотра и сокращения памяти"""
    output = [cv2.VideoWriter(f'archive/video_{i}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 200, (360, 240)) for i in
              range(1, 6)]

    print('watch')
    file_count = 0
    player = MediaPlayer(cameras[3])

    while True:
        _, img11 = list_cam[0].read()
        _, img22 = list_cam[1].read()
        _, img33 = list_cam[2].read()
        _, img44 = list_cam[3].read()
        _, img55 = list_cam[4].read()

        try:
            img1 = cv2.resize(img11, (360, 240))
            img2 = cv2.resize(img22, (360, 240))
            img3 = cv2.resize(img33, (360, 240))
            img4 = cv2.resize(img44, (360, 240))
            img5 = cv2.resize(img55, (360, 240))

            audio_frame, val = player.get_frame()

            """Показываем трансляцию"""
            if command == 'show':
                cv2.imshow("Hole", img1)
                cv2.imshow("Gates", img2)
                cv2.imshow("Car", img3)
                cv2.imshow("Balcony", img4)
                cv2.imshow("GuestRoom", img5)

                if val != 'eof' and audio_frame is not None:
                    img342, t = audio_frame

            """Запись в файлы, включаем когда надо"""
            if command == 'rec':
                output[0].write(img1)
                output[1].write(img2)
                output[2].write(img3)
                output[3].write(img4)
                output[4].write(img5)
        except Exception as E1:
            print('E1', E1)
            break

        file_count += 1
        print('Кадр {0:04d}'.format(file_count))

        key = cv2.waitKey(20)
        if (key == ord('q')) or key == 27:
            [_.release() for _ in list_cam]
            [_.release() for _ in output]
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    show_must_go_on()
