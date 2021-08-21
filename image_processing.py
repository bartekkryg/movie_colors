import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans
from imutils.video import FPS


DIR = 'killbill/'


def get_dominant_color(filename):
    im = cv2.imread(DIR + filename)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    pixels = np.asarray(im, dtype='float')
    pixels = pixels.reshape((187 * 450, 3))
    clusters = KMeans(n_clusters=2, random_state=0).fit(pixels)
    hist, _ = np.histogram(clusters.labels_, bins=len(np.unique(clusters.labels_)))
    col = clusters.cluster_centers_[np.argmax(hist)]
    return col


class ImageProcesser:
    def __init__(self, files):
        self.files = files
        self.colors = []

    def process_files(self):
        fps = FPS().start()
        for file in self.files:
            print(f"[INFO] processing {file}")
            dominant_color = get_dominant_color(file)
            print(f"[INFO] {file} -- color: {dominant_color}")
            fps.update()
            self.colors.append(dominant_color/255.)
        fps.stop()
        print(fps.elapsed())

    def plot_colors(self):
        self.process_files()
        self.colors = np.asarray(self.colors)
        x = np.arange(0, self.colors.shape[0])
        plt.figure(figsize=(16, 4))
        plt.axis('off')
        plt.title('Kill Bill 2008')
        plt.bar(x, 1, 1, color=self.colors)
        plt.savefig('colorbar')
        plt.show()


if __name__ == '__main__':
    #file_count = len(os.listdir('killbill'))
    #filenames = [f'frame{i*12+1}.jpg' for i in range(file_count)]
#    filenames = ['frame1.jpg', 'frame13.jpg','frame25.jpg']
    #imp = ImageProcesser(filenames)
    #imp.plot_colors()
    #clusters = get_dominant_color('frame103093.jpg')
    col = get_dominant_color('frame49.jpg')
    print(col)
