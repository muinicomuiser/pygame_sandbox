import curses
import cv2
import numpy as np
def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("No hay cámara")
        exit()    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("q para salir")

    while True:
        ret, frame = camera.read()
        if not ret:

            print("Error: Unable to read frame!")

            break
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = np.where(frame > 127, 255, 0).astype(np.uint8)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cv2.imshow("Cámara", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()