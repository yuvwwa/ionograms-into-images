import unittest
import ionread_python

import ionread as ir


class TestCalculator(unittest.TestCase):
    # setUp method is overridden from the parent class TestCase
    def setUp(self):
        pass

    def test_read_ionogram(self):
        ingr = ionread_python.read_ionogram(
            'test_data/01_02_07_20_00.dat')

        print(ingr.passport.__dict__)

        self.assertEqual(ingr.passport.receiver, 'Торы')
        self.assertEqual(ingr.passport.transmitter, 'МНСТ Торы')
        self.assertEqual(ingr.passport.session_date, '02.01.2014')
        self.assertEqual(ingr.passport.session_time, '07:20:00 UT')
        self.assertEqual(ingr.passport.latency, 0)
        self.assertEqual(ingr.passport.step_freq, 20)
        self.assertEqual(ingr.passport.velocity, 500)

    # def test_compare_with_native_lib(self):
    #     ingr = ionread_python.read_ionogram(
    #         'test_data/01_02_07_20_00.dat')

    #     ingr_native = ir.read_ionogram('test_data/01_02_07_20_00.dat')

    #     self.assertEqual(ingr.passport.transmitter,
    #                      ingr_native.passport.transmitter)
    #     self.assertEqual(ingr.passport.step_freq,
    #                      ingr_native.passport.step_freq)

    #     self.assertEqual(len(ingr.data), len(ingr_native.data))

    #     for i, bin in enumerate(ingr.data):
    #         bin_native = ingr_native.data[i]
    #         self.assertEqual(bin.ampl,
    #                          bin_native.ampl)

    #         # TODO В некот. случаях различается на 1
    #         # self.assertEqual(bin.dist,
    #         #                  bin_native.dist)

    #         self.assertEqual(abs(bin.dist - bin_native.dist) <= 1, True)

    #         self.assertEqual(bin.freq,
    #                          bin_native.freq)

    #         self.assertEqual(bin.num_dist,
    #                          bin_native.num_dist)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
