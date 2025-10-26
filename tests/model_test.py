from unittest import TestCase, main
from unittest.mock import MagicMock, patch, call
import numpy as np
import json

from core.models.model import LocalEmbedder


class LocalEmbedderTest(TestCase):
    def setUp(self):
        self.model_mock = MagicMock()
        self.model_mock.encode.return_value = np.array([[0.1, 0.2, 0.3]])

        self.embedder = LocalEmbedder.__new__(LocalEmbedder)  # обходим инициализацию реальной модели
        self.embedder.model = self.model_mock

    @patch('core.models.model.SentenceTransformer')
    def test_init(self, model_class_mock):
        model_class_mock.return_value = MagicMock()
        emb = LocalEmbedder('test-model')

        model_class_mock.assert_called_once_with('test-model')
        self.assertEqual(emb.model, model_class_mock.return_value)

    def test_embed(self):
        texts = ['hello', 'world']
        result = self.embedder.embed(texts)

        self.model_mock.encode.assert_called_once_with(
            texts, show_progress_bar=False, convert_to_numpy=True
        )

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)

    @patch('core.models.model.normalize_text', return_value='query text')
    def test_request(self, normalize_mock):
        vdb_mock = MagicMock()
        vdb_mock._conn.execute.return_value.fetchall.return_value = [
            {'file_path': 'path1', 'chunk_index': 0, 'text': 'text1', 'vector': json.dumps([0.2, 0.4, 0.6])},
            {'file_path': 'path2', 'chunk_index': 1, 'text': 'text2', 'vector': json.dumps([0.1, 0.2, 0.3])}
        ]

        self.embedder.model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        result = self.embedder.request('query', vdb_mock, top_k=1)

        normalize_mock.assert_called_once_with('query')
        vdb_mock._conn.execute.assert_called_once_with('SELECT file_path, chunk_index, text, vector FROM vectors')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['file_path'], 'path1')
        self.assertIn('score', result[0])
        self.assertGreaterEqual(result[0]['score'], 0.0)

    @patch('core.models.model.normalize_text', side_effect=TypeError('Неверный тип'))
    def test_request_except(self, normalize_mock):
        vdb_mock = MagicMock()

        with self.assertRaises(TypeError):
            self.embedder.request('qwe', vdb_mock)

        normalize_mock.assert_called_once_with('qwe')

    def test_vector_normalization(self):
        """Проверяем, что вектор нормализуется до длины 1"""
        vec = np.array([3, 4], dtype=np.float32)
        normed = vec / np.linalg.norm(vec)
        self.assertAlmostEqual(float(np.linalg.norm(normed)), 1.0, places=6)


if __name__ == '__main__':
    main()
