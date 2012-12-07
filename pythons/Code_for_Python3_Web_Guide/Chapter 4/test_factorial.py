import unittest
from factorial import fac

class Test(unittest.TestCase):
	
	def test_number(self):
		self.assertEqual(24,fac(4))
		self.assertEqual(120,fac(5))
		self.assertEqual(720,fac(6))

	def test_zero(self):
		self.assertEqual(1,fac(0))
	
	def test_illegal(self):
		with self.assertRaises(ValueError):
			fac(-4)
		with self.assertRaises(ValueError):
			fac(3.1415)
			
if __name__ == '__main__':
	unittest.main()
