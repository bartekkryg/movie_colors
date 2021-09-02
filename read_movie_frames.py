from FileVideoStream import FileVideoStream
from imutils.video import FPS
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans, kmeans2
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import imutils
import time


def get_dominant_color_scikit(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    pixels = np.asarray(frame, dtype='float')
    pixels = pixels.reshape((187 * 450, 3))
    clusters = kmeans_scikit.fit(pixels)
    hist, _ = np.histogram(clusters.labels_, bins=len(np.unique(clusters.labels_)))
    col = clusters.cluster_centers_[np.argmax(hist)]
    return col


def get_dominant_color_scipy(frame, k_clusters):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    pixels = np.asarray(frame, dtype='float')
    pixels = pixels.reshape((187 * 450, 3))
    clusters, labels = kmeans2(pixels, k_clusters, minit='++', seed=0)
    hist, _ = np.histogram(labels, bins=len(np.unique(labels)))
    col = clusters[np.argmax(hist)]
    return col


def plot_colors(colors, out_file=None):
    colors = np.asarray(colors)
    x = np.arange(0, colors.shape[0])
    plt.figure(figsize=(16, 4))
    plt.axis('off')
    plt.title('Kill Bill 2008')
    plt.bar(x, 1, 1, color=colors / 255.)
    if out_file:
        plt.savefig(out_file)
    plt.show()


def process_frames(in_file, k_clusters=2):
    fps = FPS().start()
    fvs = FileVideoStream(in_file).start()
    print("[INFO] starting video file thread...")
    time.sleep(1)
    count = 0
    colors = []
    while count < 3000:
        # while fvs.more():
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        if count % 12 == 0:
            start_time = time.time()
            # cv.putText(frame, f"Queue Size: {fvs.Q.qsize()}",
            #           (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # cv.imwrite(f'{out_path}/frame{count}.jpg', frame)
            print(f"[INFO] retrieved frame {count}, Queue size: {fvs.Q.qsize()}")
            print(f"[INFO] getting dominant color from frame {count}")
            dominant_color = get_dominant_color_scipy(frame, k_clusters)
            colors.append(dominant_color)
            print(f"[INFO] saved color from frame {count}")
            end_time = time.time()
            print(f"[INFO] frame processing took: {float(end_time - start_time)} seconds")

        count += 1
        fps.update()

    fps.stop()
    print(f"[INFO] elapsed time: {fps.elapsed()} seconds")
    print(f"[INFO] approx. FPS: {fps.fps()}")
    cv.destroyAllWindows()
    fvs.stop()

    return colors


if __name__ == '__main__':
    file_path = 'D:/KillBillMovie/KillBillmp4.mp4'

    K_CLUSTERS = 2
    kmeans_scikit = KMeans(n_clusters=K_CLUSTERS)

    cols = process_frames(file_path)
    plot_colors(cols, 'killbil_colorbar_k2_scipy_3kframes')

# TODO:
#   -run the script for a full killbill movie
#   -compare differences between k=1 and k=2 (decide which is better)
#   -generate colorbars for more movies (for a presentation)
#   -recode the script to a cmd tool:
#       -add -f frames <frame_count>
#       -add -k k_clusters <k_int>
#       -add function to convert the file from .* to .mp4
