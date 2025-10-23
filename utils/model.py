class DummyModel:
    def embed(self, text):
        # имитация вектора
        return [hash(text) % 1000 / 1000.0 for _ in range(10)]
