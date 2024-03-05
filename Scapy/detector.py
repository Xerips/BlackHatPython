import cv2
import os

# Change these directories according to your setup.
ROOT = '/home/$USER/TopSecretMission/pictures' # The source files for the tool to perform recognition on.
FACES = '/home/$USER/TopSecretMission/faces' # What the tool found according to it's training.
TRAIN = '/home/$USER/TopSecretMission/training' # What you want the tool to learn.

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswitch('.JPG'): # Add to or change .JPG according to source image format.
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)
        img = cv2.imread(full) # Read image with OpenCV library cv2.
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml') # Load training file.
        cascade = cv2.CascadeClassifier(training) # Create the cv2 face detector object.
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            if rects.any():
                print('Got a face...')
                rects[:, 2:] += rects[:, :2] # Python slice syntax to convert the returned rects data to actual coordinates.
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue

        # Rectangle the faces in the image:
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        cv2.imwrite(newname, img)

if name == '__main__':
    detect()
