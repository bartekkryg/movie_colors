from imutils.video import FPS
import cv2 as cv

file_path = 'D:/Kill.Bill.Volume.1.2003.1080p.BluRay.x264-LiBRARiANS' \
            '/Kill.Bill.Vol.1.2003.RERiP.iNTERNAL.1080p.BluRay.x264-LiBRARiANS.mkv'

out_path = 'killbill'

cap = cv.VideoCapture(file_path)
fps = FPS().start()
count = 1

prev_time = -1
while count < 95:
    grabbed = cap.grab()
    if grabbed:
        time_s = cap.get(cv.CAP_PROP_POS_MSEC) / 500
        #frame = imutils.resize(frame, width=450)
        if int(time_s) > int(prev_time):
            ret, frame = cap.retrieve()
            cv.imwrite(f'{out_path}/frame{count}_{int(time_s)}.jpg', frame)
            print(f'retrieved frame{count} -- {int(time_s)}')
            count += 1
            fps.update()
        prev_time = time_s

    if not grabbed:
        print("Can't receive frame (stream end?). Exiting ...")
        break



fps.stop()

print(f"[INFO] elapsed time: {fps.elapsed()}")
print(f"[INFO] approx. FPS: {fps.fps()}")

cap.release()
cv.destroyAllWindows()


