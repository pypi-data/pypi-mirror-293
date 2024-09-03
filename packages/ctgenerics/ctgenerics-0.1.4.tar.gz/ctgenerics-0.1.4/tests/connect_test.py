import unittest
import ctgenerics.connect as connect

class TestConnection(unittest.TestCase):
    
    def test_create_connection(self):
        connection = connect.Redshift()
        
        self.assertIsInstance(connection,connect.Redshift)

if __name__ == '__main__':
    unittest.main()