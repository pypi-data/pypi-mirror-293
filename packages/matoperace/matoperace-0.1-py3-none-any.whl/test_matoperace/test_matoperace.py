from matoperace import matfunkce
import unittest
import numpy as np

regMaticeRadu3 = [[4, 3, -7], [0, -5, 6], [-7, 2, 2]]
regMaticeRadu4 = [[4, 3, -7, 3], [0, -5, 6, 48], [-7, 2, 2, -4], [3, 5, -4, 2]]
singMatice = [[2, 7, 6], [6, 21, 18], [3, 4, 5]]
maticeProQrRozklad = [[3, 0, 4], [5, 12, 0], [[0, 8, 15]]]
soustavaReg = [[4, 3, -7, -36], [0, -5, 6, 45], [-7, 2, 2, -10]]
soustavaSing = [[4, 3, 8, -13], [0, -5, 0, -5], [-7, 2, -14, 30]]
soustavaSingBezReseni = [[4, 3, 8, 4], [0, -5, 0, 12], [-7, 2, -14, 3]]
body = [[0, 1], [1, 1], [2, 2], [3, 4], [4, 5]]

class TestDeterminant(unittest.TestCase):

    def test_reg_rad_3(self):
        self.assertEqual(round(matfunkce.Determinant(regMaticeRadu3), 10), round(np.linalg.det(regMaticeRadu3), 10))

    def test_reg_rad_4(self):
        self.assertEqual(round(matfunkce.Determinant(regMaticeRadu4), 10), round(np.linalg.det(regMaticeRadu4), 10))

    def test_singRad_3(self):
        self.assertEqual(matfunkce.Determinant(singMatice), 0)

class TestLURozklad(unittest.TestCase):

    def test_reg_rad_3(self):
        rozklad = matfunkce.LURozklad(regMaticeRadu3)
        kontrola = np.matmul(rozklad[0], rozklad[1])
        kontrola = matfunkce.ZaokMat(kontrola, 10)
        for i in range(3):
            self.assertListEqual(list(kontrola[i]), regMaticeRadu3[i])

    def test_reg_rad_4(self):
        rozklad = matfunkce.LURozklad(regMaticeRadu4)
        kontrola = np.matmul(rozklad[0], rozklad[1])
        kontrola = matfunkce.ZaokMat(kontrola, 10)
        for i in range(3):
            self.assertListEqual(list(kontrola[i]), regMaticeRadu4[i])

class TestQRRozklad(unittest.TestCase):

    def test_rad_3(self):
        rozklad = matfunkce.QRRozklad(regMaticeRadu3)
        kontrola = np.matmul(rozklad[0], rozklad[1])
        kontrola = matfunkce.ZaokMat(kontrola, 10)
        for i in range(3):
            self.assertListEqual(list(kontrola[i]), regMaticeRadu3[i])

    def test_rad_4(self):
        rozklad = matfunkce.QRRozklad(regMaticeRadu4)
        kontrola = np.matmul(rozklad[0], rozklad[1])
        kontrola = matfunkce.ZaokMat(kontrola, 10)
        for i in range(4):
            self.assertListEqual(list(kontrola[i]), regMaticeRadu4[i])

class TestCramer(unittest.TestCase):

    def test_reg_matice(self):
        self.assertListEqual(matfunkce.Cramer(soustavaReg), [2, -3, 5])

    def test_sing_matice(self):
        self.assertIsNone(matfunkce.Cramer(soustavaSing))

class TestGaussJorEliminace(unittest.TestCase):

    def test_reg_matice(self):
        self.assertListEqual(matfunkce.GaussJorEliminace(soustavaReg), [2, -3, 5])

    def test_sing_matice(self):
        self.assertListEqual(matfunkce.GaussJorEliminace(soustavaSing), [-4, 1, 0])

class TestLinearniRegrese(unittest.TestCase):

    def test_body(self):
        self.assertListEqual(matfunkce.LinearniRegrese(body), [1.1, 0.4])


if __name__ == '__main__':
    unittest.main()