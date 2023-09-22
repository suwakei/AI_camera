import os
import cv2
import sys

def headshots():
    name = input("名前を入力してください(日本語はダメ): ")#opencvは日本語対応してないからimwriteした後リネームする
    print("写真を撮ります")#マスクありの写真も撮ることでマスクのまま認識可能
    try:
        userDirPath = "dataset/" + name
        os.mkdir(userDirPath)
    except:
        print(f"\"{name}\"と同じ名前が存在しています ")
        sys.exit()

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("press space key to take pictures", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("press space key to take pictures", 800, 600)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("失敗しました")
            break
        cv2.imshow("press space key to take pictures", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escが押されたのでウィンドウを閉じます...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} に保存されました!".format(img_name))
            img_counter += 1

    cam.release()
    # window delete
    cv2.destroyAllWindows()


if __name__ == "__main__":
    headshots()