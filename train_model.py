from imutils import paths
import face_recognition
from headshots import headshots
import pickle
import cv2
import os

def train_model():
	# 画像をdatasetフォルダに置きます
	print(" 顔パターン学習を開始します...")
	imagePaths = list(paths.list_images("dataset"))

	# known encodings and knownnamesを初期化
	knownEncodings = []
	knownNames = []

	# image pathsをループ
	for (i, imagePath) in enumerate(imagePaths):
		# image pathから穂との名前を切り抜く
		print(f"画像学習進捗 {i + 1}/{len(imagePaths)}")
		name = imagePath.split(os.path.sep)[-2]

		# インプットした画像をロードして(RGB)に転換する
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# 境界ボックスの (x, y) 座標を検出する
		# 入力画像の各顔に対応
		boxes = face_recognition.face_locations(rgb,
			model="hog")

		# 顔の埋め込みを計算
		encodings = face_recognition.face_encodings(rgb, boxes)

		# エンコーディングをループする
		for encoding in encodings:
			# 各エンコーディング + nameをknownnameに追加しエンコーディング
			knownEncodings.append(encoding)
			knownNames.append(name)


	print("encodingsをserializeします...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open("./models/pickles/encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()


if __name__ == "__main__":
	yorn = str(input("顔写真撮影をスキップしますか？ y or n =>"))
	if yorn == "n":
		headshots()
		train_model()
	elif yorn == "y":
		print("撮影をスキップします")
		train_model()
	else:
		print("y(yes)かn(no)のみでお願い")