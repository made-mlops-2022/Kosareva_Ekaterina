import unittest
from train import read_data, model_fit
from predict import predict_class
from sklearn.metrics import roc_auc_score

class TestMyTrain(unittest.TestCase):
    def test_read_data(self):
        '''check data shape'''

        self.assertEqual(read_data('data/synthetic_data.csv', 'condition')[0].shape, (300, 28), "Wrong data size")

    def test_model_fit(self):
        '''check if model has prediction better than random'''

        X, y = read_data('data/synthetic_data.csv', 'condition')
        model = model_fit(X, y, 7, 100, 0)
        y_pred = predict_class(X, model)

        self.assertGreater(roc_auc_score(y, y_pred), float(0.5))

if __name__ == '__main__':
    unittest.main()

