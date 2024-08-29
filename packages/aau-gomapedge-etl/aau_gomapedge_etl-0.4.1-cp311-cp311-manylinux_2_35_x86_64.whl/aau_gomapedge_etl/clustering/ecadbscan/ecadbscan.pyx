from sklearn.cluster import DBSCAN
from numpy cimport ndarray
from libc cimport math
cimport cython

cdef class EpsConstrainedAngularDBSCAN:
    cdef object dbscan
    cdef float __eps
    cdef float __max_angle_diff

    def __cinit__(self, float eps = 10.0, int min_samples = 5, float max_angle_diff = 45):
        self.__max_angle_diff = max_angle_diff
        self.__eps = eps
        self.dbscan = DBSCAN(eps=self.__eps, min_samples=min_samples, metric=self.metric)
        

    cdef double unsigned_angle_diff(self, double a1, double a2):
        return abs(a1 - a2) % 360

    @cython.boundscheck(False) # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    cdef double metric(self, ndarray[double, ndim=1] X, ndarray[double, ndim=1] Y):
        cdef double spatial_dist = math.sqrt((X[0] - Y[0])**2 + (X[1] - Y[1])**2)
        cdef double angular_dist = self.unsigned_angle_diff(X[2], Y[2])
        cdef double scaled_angle_dist = angular_dist / self.__max_angle_diff * self.__eps
        
        return max(spatial_dist, scaled_angle_dist) 

    def run_dbscan(self, ndarray[double, ndim=2] data) -> ndarray[int]:
        self.dbscan.fit_predict(data)
        return self.dbscan.labels_