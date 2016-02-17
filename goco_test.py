import unittest
import goco as gc
from goco import lispify

class GoCoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "******* Testing GoCo *******"
    
    def setUp(self):
        self.goco = gc.GoCo()
        
    def test_lispify(self):
        commitment1 = "C1(PHYSICIAN, PATIENT, diagnosisRequested ^ -vio(C2) ^ -vio(C3), diagnosisProvided)"
        self.goco.parse_commitments(commitment1)
        self.assertIsNotNone(self.goco.commitments)
        self.assertGreater(len(self.goco.commitments), 0)
        print str(self.goco.commitments['C1'].antecedent)
        lisp_expr = lispify(self.goco.commitments['C1'].antecedent)
        print lisp_expr
        self.assertEquals("(and diagnosisRequested (not (vio ?C2)) (not (vio ?C3)))", lisp_expr)
        
if __name__ == '__main__':
    unittest.main()