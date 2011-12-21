import os.path

import numpy as np
from numpy import testing

from skimage import data_dir
from skimage.morphology.grey import *
from skimage.morphology import selem


lena = np.load(os.path.join(data_dir, 'lena_GRAY_U8.npy'))

class TestMorphology():

    def morph_worker(self, img, fn, morph_func, strel_func):
        matlab_results = np.load(os.path.join(data_dir, fn))
        k = 0
        for arrname in sorted(matlab_results):
            expected_result = matlab_results[arrname]
            mask = strel_func(k)
            actual_result = morph_func(lena, mask)
            testing.assert_equal(expected_result, actual_result)
            k = k + 1

    def test_erode_diamond(self):
        self.morph_worker(lena, "diamond-erode-matlab-output.npz",
                          erosion, selem.diamond)

    def test_dilate_diamond(self):
        self.morph_worker(lena, "diamond-dilate-matlab-output.npz",
                          dilation, selem.diamond)

    def test_open_diamond(self):
        self.morph_worker(lena, "diamond-open-matlab-output.npz",
                          opening, selem.diamond)

    def test_close_diamond(self):
        self.morph_worker(lena, "diamond-close-matlab-output.npz",
                          closing, selem.diamond)

    def test_tophat_diamond(self):
        self.morph_worker(lena, "diamond-tophat-matlab-output.npz",
                          white_tophat, selem.diamond)

    def test_bothat_diamond(self):
        self.morph_worker(lena, "diamond-bothat-matlab-output.npz",
                          black_tophat, selem.diamond)

    def test_erode_disk(self):
        self.morph_worker(lena, "disk-erode-matlab-output.npz",
                          erosion, selem.disk)

    def test_dilate_disk(self):
        self.morph_worker(lena, "disk-dilate-matlab-output.npz",
                          dilation, selem.disk)

    def test_open_disk(self):
        self.morph_worker(lena, "disk-open-matlab-output.npz",
                          opening, selem.disk)

    def test_close_disk(self):
        self.morph_worker(lena, "disk-close-matlab-output.npz",
                          closing, selem.disk)


class TestEccentricStructuringElements():

    def setUp(self):
        self.black_pixel = 255 * np.ones((4, 4), dtype=np.uint8)
        self.black_pixel[1, 1] = 0
        self.white_pixel = 255 - self.black_pixel
        self.selems = [selem.square(2), selem.rectangle(2, 2),
                       selem.rectangle(2, 1), selem.rectangle(1, 2)]

    def test_dilate_erode_symmetry(self):
        for s in self.selems:
            c = erosion(self.black_pixel, s)
            d = dilation(self.white_pixel, s)
            assert np.all(c == (255 - d))

    def test_open_black_pixel(self):
        for s in self.selems:
            grey_open = opening(self.black_pixel, s)
            assert np.all(grey_open == self.black_pixel)

    def test_close_white_pixel(self):
        for s in self.selems:
            grey_close = closing(self.white_pixel, s)
            assert np.all(grey_close == self.white_pixel)

    def test_open_white_pixel(self):
        for s in self.selems:
            assert np.all(opening(self.white_pixel, s) == 0)

    def test_close_black_pixel(self):
        for s in self.selems:
            assert np.all(closing(self.black_pixel, s) == 255)

    def test_white_tophat_white_pixel(self):
        for s in self.selems:
            tophat = white_tophat(self.white_pixel, s)
            assert np.all(tophat == self.white_pixel)

    def test_black_tophat_black_pixel(self):
        for s in self.selems:
            tophat = black_tophat(self.black_pixel, s)
            assert np.all(tophat == (255 - self.black_pixel))

    def test_white_tophat_black_pixel(self):
        for s in self.selems:
            tophat = white_tophat(self.black_pixel, s)
            assert np.all(tophat == 0)

    def test_black_tophat_white_pixel(self):
        for s in self.selems:
            tophat = black_tophat(self.white_pixel, s)
            assert np.all(tophat == 0)


if __name__ == '__main__':
    testing.run_module_suite()

