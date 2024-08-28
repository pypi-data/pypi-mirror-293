# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from caplib.analytics import *

class TestAnalytics(unittest.TestCase):
    
    def test_create_default_model_settings(self):
        expected = b'\x08\x01\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00'
        test = create_model_settings('BLACK_SCHOLES_MERTON')
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_model_settings(self):
        expected = b'\x08\x01\x12\x08{\x14\xaeG\xe1z\x84?\x1a\x00"\nEURIBOR_3M'
        model_name = 'BLACK_SCHOLES_MERTON'
        const_params = [0.01]
        ts_params = [TermStructureCurve()]
        underlying = 'EURIBOR_3M'
        calib = False
        test = create_model_settings(model_name, const_params, ts_params, underlying, calib)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_pde_settings(self):
        expected = b'\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01'
        test = create_pde_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_pde_settings(self):
        expected = b'\x08e\x10\xc9\x01\x19\x00\x00\x00\x00\x00\x00\x14\xc0!\x00\x00\x00\x00\x00\x00\x14@0\x0bA\x00\x00\x00\x00\x00\x00$@H\x01P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x9a\x99\x99\x99\x99\x99\xb9?y\x9a\x99\x99\x99\x99\x99\xb9?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x02\x90\x01\x01\x98\x01\x01\xa0\x01\x02\xa8\x01\x01\xb0\x01\x01'
        test = create_pde_settings(101,201, -5, 5, 'MMT_NUM_STDEVS', 0.1, 'ADAPTIVE_GRID', 'CUBIC_SPLINE_INTERP',
                                   11, 0, 10, 'MMT_ABOSLUTE', 0.1, 'UNIFORM_GRID', 'LINEAR_INTERP')
        self.assertEqual(test.SerializeToString(), expected)
    
    def test_create_default_monte_carlo_settings(self):
        expected = b'\x08\x80\x08\x18\x80\x08 \x01(\x018\x01'
        test = create_monte_carlo_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_monte_carlo_settings(self):
        expected = b'\x08\xb8\x17\x10\x01\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01 \x02(\x010\x018e'
        test = create_monte_carlo_settings(3000, 
                                           'MERSENNE_TWIST_19937_NUMBER',  
                                           -1, 
                                           'INCREMENTAL_METHOD', 
                                           'INVERSE_CUMULATIVE_METHOD', True, 101)
        self.assertEqual(test.SerializeToString(), expected)
     
    def test_create_model_free_pricing_settings(self):
        expected = b'\nl\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01\x12\x0c\x08\x80\x08\x18\x80\x08 \x01(\x018\x01\x1a\n\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00'
        test = create_model_free_pricing_settings('', False)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_pricing_settings(self):
        expected = b'\nl\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01\x12\x0c\x08\x80\x08\x18\x80\x08 \x01(\x018\x01\x1a\x0c\x08\x01\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00:\x03CNY'
        test = create_pricing_settings('CNY', False, create_model_settings('BLACK_SCHOLES_MERTON'), 'ANALYTICAL', create_pde_settings(), create_monte_carlo_settings())
        #print('test_create_pricing_settings', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_ir_curve_risk_settings(self):
        expected = b'!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?A-C\x1c\xeb\xe26\x1a?'
        test = create_ir_curve_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_ir_curve_risk_settings(self):
        expected = b'\x08\x01\x10\x01\x18\x01!-C\x1c\xeb\xe26*?){\x14\xaeG\xe1zt?8\x01A-C\x1c\xeb\xe26*?H\x01'
        test = create_ir_curve_risk_settings(True,True, True,2.0e-4, 50e-4, 
                                             'CENTRAL_DIFFERENCE_METHOD', 
                                             'TERM_BUCKET_RISK', 2.0e-4, 
                                             'MULTI_THREADING_MODE')
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_credit_curve_risk_settings(self):
        expected = b'!-C\x1c\xeb\xe26\x1a?A-C\x1c\xeb\xe26\x1a?'
        test = create_credit_curve_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_theta_risk_settings(self):
        expected = b'\x10\x01\x19\x1ag\x016\x9fqf?'
        test = create_theta_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_theta_risk_settings(self):
        expected = b'\x08\x01\x10\x01\x19\x1ag\x016\x9fqf?'
        test = create_theta_risk_settings(True, 1, 1./365.)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_ir_yield_curve(self):
        expected = b'\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        test = create_ir_yield_curve(datetime(2022,3,9),'CNY', [datetime(2022,3,10), datetime(2025,3,10)], [0.02, 0.025])
        #pprint('test_create_default_ir_yield_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_ir_yield_curve(self):
        expected = b'\x12P\nL\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x02ON"\x023Y*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01B\rCNY_SHIBOR_3M\x10\x02\x1a\x03CNY \x01:!\n\rCNY_SHIBOR_3M\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        test = create_ir_yield_curve(datetime(2022,3,9),'CNY', 
                                     [datetime(2022,3,10), datetime(2025,3,10)], 
                                     [0.02, 0.025], 
                                     'ACT_365_FIXED', 'LINEAR_INTERP', 'FLAT_EXTRAP', 'DISCRETE_COMPOUNDING', 'ANNUAL', 
                                     [0.0], 'CNY_SHIBOR_3M', ['ON', '3Y'])
        #pprint('test_create_ir_yield_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_credit_curve(self):
        expected =  b'\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?0\x018\x01\x12\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?'
        test = create_credit_curve(datetime(2022,3,9), 
                                   [datetime(2022,3,10), datetime(2025,3,10)], [0.2e-2, 0.25e-2])
        #print('test_create_credit_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)