import time
import cv2


def run_motion_detector(min_area: int = 1500, cooldown_sec: float = 3.0):
  cap = cv2.VideoCapture(0)  # 0 = webcam/kamera utama
  if not cap.isOpened():
    raise RuntimeError("Kamera gagal dibuka.")

  prev_gray = None
  last_action_time = 0.0

  try:
    while True:
      ret, frame = cap.read()
      if not ret:
        break

      # --- 1. ALGORITMA DETEKSI (Frame Differencing) ---
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (21, 21), 0)  # kurangi noise piksel

      if prev_gray is None:
        prev_gray = gray
        continue

      diff = cv2.absdiff(prev_gray, gray)
      _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
      thresh = cv2.dilate(thresh, None, iterations=2)

      contours, _ = cv2.findContours(
          thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
      )

      motion_detected = False
      for contour in contours:
        if cv2.contourArea(contour) < min_area:
          continue  # abaikan gerakan kecil/noise
        motion_detected = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

      # --- 2. LOGIKA AKSI (Use Case / Business Logic) ---
      now = time.time()
      if motion_detected and (now - last_action_time >= cooldown_sec):
        last_action_time = now
        on_motion_detected(frame)

      cv2.imshow("Motion Detector", frame)
      prev_gray = gray  # update frame acuan untuk iterasi berikutnya

      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
  finally:
    cap.release()
    cv2.destroyAllWindows()


def on_motion_detected(frame):
  # Ganti bagian ini sesuai kebutuhan: kirim notif, log ke file, panggil API, dll.
  filename = f"motion_{int(time.time())}.jpg"
  cv2.imwrite(filename, frame)
  print(f"[AKSI] Gerakan terdeteksi -> snapshot disimpan: {filename}")


if _name_ == "_main_":
  run_motion_detector()