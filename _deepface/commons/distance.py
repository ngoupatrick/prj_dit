import numpy as np

def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

def findEuclideanDistance(source_representation, test_representation):
    if type(source_representation) == list:
        source_representation = np.array(source_representation)

    if type(test_representation) == list:
        test_representation = np.array(test_representation)

    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))

def findThreshold(model_name, distance_metric):

	base_threshold = {'cosine': 1.0, 'euclidean': 0.55, 'euclidean_l2': 0.75}#'cosine': 0.40

	thresholds = {
		'VGG-Face': {'cosine': 1.0, 'euclidean': 0.60, 'euclidean_l2': 0.86},#'cosine': 0.40
        'Facenet':  {'cosine': 1.0, 'euclidean': 10, 'euclidean_l2': 0.80},#'cosine': 0.40
        'Facenet512':  {'cosine': 1.0, 'euclidean': 23.56, 'euclidean_l2': 1.04},#'cosine': 0.30
        'ArcFace':  {'cosine': 1.0, 'euclidean': 4.15, 'euclidean_l2': 1.13},#'cosine': 0.68
        'Dlib': 	{'cosine': 1.0, 'euclidean': 0.6, 'euclidean_l2': 0.4},#'cosine': 0.07

		'OpenFace': {'cosine': 1.0, 'euclidean': 0.55, 'euclidean_l2': 0.55},#'cosine': 0.10
		'DeepFace': {'cosine': 1.0, 'euclidean': 64, 'euclidean_l2': 0.64},#'cosine': 0.23
		'DeepID': 	{'cosine': 1.0, 'euclidean': 45, 'euclidean_l2': 0.17}#'cosine': 0.015

		}

	threshold = thresholds.get(model_name, base_threshold).get(distance_metric, 0.4)

	return threshold
