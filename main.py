import cv2 as cv
import numpy as np
import socket
import time

camera_matrix = np.array([[14 * (4032 / 17.3), 0., 4032 / 2],
                          [0., 14 * (3024 / 13), 3024 / 2],
                          [0., 0., 1.]],
                         dtype=float)


def Rx(theta):
    return np.matrix([[1, 0, 0],
                      [0, np.cos(theta), -np.sin(theta)],
                      [0, np.sin(theta), np.cos(theta)]])


def Ry(theta):
    return np.matrix([[np.cos(theta), 0, np.sin(theta)],
                      [0, 1, 0],
                      [-np.sin(theta), 0, np.cos(theta)]])


def Rz(theta):
    return np.matrix([[np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta), np.cos(theta), 0],
                      [0, 0, 1]])


def point_3d(fp1, fp2, tpos1, tpos2):
    #
    pos1 = [[1, 0, 0, tpos1[0]],
            [0, 1, 0, tpos1[1]],
            [0, 0, -1, tpos1[2]]]
    pos1 = np.asarray(pos1, np.double)

    pos2 = [[0, 0, -1, tpos2[0]],
            [0, 1, 0, tpos2[1]],
            [-1, 0, 0, tpos2[2]]]
    pos2 = np.asarray(pos2, np.double)

    rmat = np.asarray([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
    tmat = np.asarray(tpos1)

    # pos1 = np.matmul(camera_matrix, pos1)
    # pos2 = np.matmul(camera_matrix, pos2)

    # a, b, c, d, e, f, g = cv.decomposeProjectionMatrix(pos1)
    #
    # print(a, b, c/c[3], sep='\n\n')
    #
    # a, b, c, d, e, f, g = cv.decomposeProjectionMatrix(pos2)
    #
    # print(a, b, c / c[3], sep='\n\n')

    fp1 = np.asarray(fp1, np.double)

    fp2 = np.asarray(fp2, np.double)

    loc = cv.triangulatePoints(pos1, pos2, fp1.T, fp2.T)

    # objectPoints = np.asarray([1, 0.0, 0.0])
    # objectPoints = objectPoints.T.reshape(-1, 1, 3)
    #
    # print(objectPoints)
    # rvec = np.asarray([0, 2, 0], float)
    # tvec = np.asarray([0, 0, 0], float)
    # point2d, _ = cv.projectPoints(objectPoints, rvec, tvec, camera_matrix, np.zeros(4, float))
    # print(point2d)

    X = loc / loc[3]
    # X1 = pos1[:3] @ X
    # X2 = pos2[:3] @ X

    print(X[0][0], X[1][0], X[2][0], sep=' ')
    return [X[0][0], X[1][0], X[2][0]]


def non_distort(x, y):
    test = np.asarray([[[x, y]]], dtype=np.float32)
    xy_undistorted = cv.undistortPoints(test, camera_matrix, 0)
    # print(xy_undistorted[0][0][0], xy_undistorted[0][0][1])
    return [xy_undistorted[0][0][0], xy_undistorted[0][0][1]]


if __name__ == '__main__':
    v1 = 4032 / 2
    v2 = 3024 / 2
    # pos = [v1 * 0, v2 * 0]

    host, port = "127.0.0.1", 25001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    while True:
        time.sleep(0.05)
        receivedData = sock.recv(1024).decode("UTF-8")
        print(receivedData)

        argv = receivedData.split(' ')

        res = point_3d(non_distort(v1 - (v1 * float(argv[0])), v2 - (v2 * float(argv[1]))),
                 non_distort(v1 - (v1 * float(argv[2])), v2 - (v2 * float(argv[3]))),
                 [0, 0, -1],
                 [0, 0, -1])

        sock.sendall(res.__str__()[1:-1].encode("UTF-8"), )  # Converting string to Byte, and sending it to C#
