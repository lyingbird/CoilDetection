import icp
import numpy as np
from matplotlib import pyplot as plt
import cv2
# Create the datasets
ang = np.linspace(-np.pi/2, np.pi/2, 320)
a = np.array([ang, np.cos(ang)])
th = np.pi/2
ang = np.linspace(-np.pi/2, np.pi/2, 100)
rot = np.array([[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]])
b = np.dot(rot, a) + np.array([[0.2], [0.3]])

#b=np.delete(b,[1,2,3,4], axis = 1)


# Run the

M2 = icp.icp(a, b, [0.1,  0.33, np.pi/2.2], 30)

# Plot the result
src = np.array([a.T]).astype(np.float32)
res = cv2.transform(src, M2)
plt.figure()
plt.plot(b[0],b[1],'g')
plt.plot(res[0].T[0], res[0].T[1], 'r.')
plt.plot(a[0], a[1],'b')
# plt.scatter(b[0],b[1])
# plt.scatter(res[0].T[0], res[0].T[1])
# plt.scatter(a[0], a[1])
plt.show()
# print 'b0 '+str(b[0])
# print 'b1 '+str(b[1])

