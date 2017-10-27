import os
import numpy as np
import cv2
import sqlite3

# instantiate the camera object and haar cascade
cam = cv2.VideoCapture(0)
face_cas = cv2.CascadeClassifier('/home/anshul/Desktop/Project/haarcascade_frontalface_default.xml')

# declare the type of font to be used on output window
font = cv2.FONT_HERSHEY_SIMPLEX
data = []
MAX = 0
path = '/home/anshul/Desktop/Project/'
files=[os.path.join(path,f) for f in os.listdir(path)]
for file in files:
	if file.endswith('.npy'):
		data.append(np.load(file).reshape((20, 50*50*3)))
		MAX = MAX + 20
data = np.concatenate(data)

labels = np.zeros((MAX, 1))
idx = 0
for i in range(20,MAX+1,20):
	labels[i-20:i, :] = idx
	idx = idx + 1.0
	print(i)

for label in labels:
    print(label)

print(data.shape, labels.shape)	# (MAX, 1)

# the distance and knn functions we defined earlier
def distance(x1, x2):
    return np.sqrt(((x1-x2)**2).sum())

def knn(x, train, targets, k=5):
    m = train.shape[0]
    dist = []
    for ix in range(m):
        # compute distance from each point and store in dist
        dist.append(distance(x, train[ix]))
    dist = np.asarray(dist)
    indx = np.argsort(dist)
    sorted_labels = labels[indx][:k]
    counts = np.unique(sorted_labels, return_counts=True)
    return counts[0][np.argmax(counts[1])]

while True:
	# get each frame
	ret, frame = cam.read()

	if ret == True:
		# convert to grayscale and get faces
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cas.detectMultiScale(gray, 1.3, 5)

		# for each face
		for (x, y, w, h) in faces:
			face_component = frame[y:y+h, x:x+w, : ]
			fc = cv2.resize(face_component, (50, 50))

			# after processing the image and rescaling
			# convert to linear vector using .flatten()
			# and pass to knn function along with all the data

			lab = knn(fc.flatten(), data, labels)
			# convert this label to int and get the corresponding name
			ID = int(lab)
			conn=sqlite3.connect("data.sqlite")
			c=conn.cursor()
			conn.commit()
			c.execute('SELECT NAME FROM people Where ID = ?',(ID,))
			text = c.fetchall()[0][0]
			conn.commit()
			# display the name
			cv2.putText(frame, text, (x, y), font, 1, (255, 255, 0), 2)

			# draw a rectangle over the face
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
		cv2.imshow('face recognition', frame)

		if cv2.waitKey(1) == ord('e'):
			break
	else:
		print('Error')

cv2.destroyAllWindows()
cam.release()
