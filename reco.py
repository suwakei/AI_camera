from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
def reco():
	#新しい人が識別された場合にのみトリガーするように「currentname」を初期化
	currentname = "unknown"
	#train_model.pyから作成されたencodings.pickleファイルモデルから顔を決定
	encodingsP = "./models/pickles/encodings.pickle"
	#使用するxml
	cascade = "./models/face_recognize/haarcascade_frontalface_default.xml"

	# knownnameとenbbedingsをOpenCVのHaarと共にロード
	# 顔検出のカスケード
	print("encoding.pickleと顔検出器をロードしてます...")
	data = pickle.loads(open(encodingsP, "rb").read())
	detector = cv2.CascadeClassifier(cascade)

	# Videostreamを初期化しカメラセンサーが作動するようにする
	print("カメラスタート...")
	vs = VideoStream(src=0).start()
	#vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	#FPSカウンタースタート
	fps = FPS().start()

	# ビデオファイルストリームからのフレームをループ
	while True:
		# スレッド化されたビデオ ストリームからフレームを取得、サイズを変更
		# 500pxまで（処理高速化のため）
		frame = vs.read()
		frame = imutils.resize(frame, width=800)
		
		# 入力フレームをBGR からグレースケールに変換し(顔用検出)  BGRからRGBへ（顔認識用）
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# グレースケールフレームで顔を検出する
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		# バウンディングボックスの座標を（x、y、w、h）の順序で返す
		# ただし、(上、右、下、左) の順序でそれらを必要とするため、少し並べ替える必要あり
		boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

		# 顔の境界ボックスごとに顔の埋め込みを計算する
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []

		# 顔の埋め込みをループする
		for encoding in encodings:
			# 入力画像の各顔を既知のものと一致させようとします
			matches = face_recognition.compare_faces(data["encodings"], encoding)
			name = "Unknown" #顔が認識されない場合は、Unknownと出力

			# 一致するものが見つかったかどうかを確認
			if True in matches:
				# 一致したすべての顔のインデックスを見つけ、辞書を初期化し、各顔が一致した合計回数をカウントする
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# 一致したインデックスをループし、認識された顔ごとにカウントを維持
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# 投票数が最も多い認識された顔を決定する (注: 可能性が低い同点の場合、辞書の最初のエントリを選択します)
				name = max(counts, key=counts.get)
				
				#データセット内の誰かが特定された場合は、その名前を画面に出力する
				if currentname != name:
					currentname = name
					print(currentname)
			
			# nameリスト更新
			names.append(name)

		# 認識された顔をループ
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# 画像に予測された顔の名前を描画 - 色は BGR にある
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		# 画面に画像を表示する
		cv2.imshow("recognizing...", frame)
		key = cv2.waitKey(1) & 0xFF

		# q キーが押されたら終了する
		if key == ord("q"):
			break

		# FPS カウンターを更新する
		fps.update()

	# タイマーを停止して FPS 情報を表示する
	fps.stop()
	print("経過時間: {:.2f}".format(fps.elapsed()))
	print("おおよそのFPS: {:.2f}".format(fps.fps()))


	cv2.destroyAllWindows()
	vs.stop()
	print(name+"です")
	return name


if __name__ == "__main__":
	nn = reco()#ちゃんと名前がreturnできてる