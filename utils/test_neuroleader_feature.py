"""
Test skrypt do weryfikacji poprawności implementacji funkcji typologii neuroliderów.
"""
import os
import sys
import json
from datetime import datetime
import unittest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.neuroleader_types import NeuroleaderTypes

class TestNeuroliderFeature(unittest.TestCase):
    """Klasa do testowania funkcjonalności typologii neuroliderów."""
    
    def setUp(self):
        self.neuroleader_types = NeuroleaderTypes()
        
    def test_types_data_loaded(self):
        """Sprawdza, czy dane typów neuroliderów zostały poprawnie załadowane."""
        types = self.neuroleader_types.types_data
        self.assertIsNotNone(types)
        self.assertGreater(len(types), 0)
        print(f"✅ Znaleziono {len(types)} typów neuroliderów")
        
        # Sprawdzamy czy wszystkie 6 typów jest dostępnych
        type_ids = [t['id'] for t in types]
        expected_types = ['neuroanalityk', 'neurobalanser', 'neuroempata', 
                          'neuroinnowator', 'neuroinspirator', 'neuroreaktor']
        for type_id in expected_types:
            self.assertIn(type_id, type_ids)
        print("✅ Wszystkie 6 oczekiwanych typów neuroliderów jest dostępnych")
        
    def test_test_data_loaded(self):
        """Sprawdza, czy dane testu neuroliderów zostały poprawnie załadowane."""
        test_data = self.neuroleader_types.test_data
        self.assertIsNotNone(test_data)
        
        questions = self.neuroleader_types.get_test_questions()
        self.assertGreater(len(questions), 0)
        print(f"✅ Znaleziono {len(questions)} pytań testowych")
        
    def test_images_exist(self):
        """Sprawdza, czy pliki graficzne dla typów neuroliderów istnieją."""
        base_dir = os.path.join("static", "images", "neuroleader_types")
        
        # Lista wszystkich oczekiwanych plików
        expected_files = []
        for type_id in ['neuroanalityk', 'neurobalanser', 'neuroempata', 
                        'neuroinnowator', 'neuroinspirator', 'neuroreaktor']:
            expected_files.append(f"{type_id}.png")
            expected_files.append(f"{type_id}_brain.png")
        
        for filename in expected_files:
            filepath = os.path.join(base_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"Nie znaleziono pliku {filepath}")
        
        print(f"✅ Wszystkie {len(expected_files)} plików graficznych istnieje")
        
    def test_save_results(self):
        """Testuje funkcję zapisywania wyników testu."""
        # Przygotuj przykładowe wyniki
        test_results = {
            "dominant_type": "neuroanalityk",
            "secondary_type": "neuroinnowator",
            "scores": {
                "neuroanalityk": 85,
                "neurobalanser": 60,
                "neuroempata": 55,
                "neuroinnowator": 75,
                "neuroinspirator": 45,
                "neuroreaktor": 30
            },
            "answers": {
                "1": 4,
                "2": 5,
                "3": 3
                # ... więcej odpowiedzi
            }
        }
        
        # Zapisz wyniki dla testowego użytkownika
        test_user_id = "test_user_" + datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            self.neuroleader_types.save_test_results(test_user_id, test_results)
            print(f"✅ Zapisano testowe wyniki dla użytkownika {test_user_id}")
            
            # Próba odczytu zapisanych danych
            user_data_path = os.path.join("data", "content", "user_data.json")
            with open(user_data_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            
            # Sprawdź czy dane testowe są w pliku
            if "neuroleader_tests" in user_data and len(user_data["neuroleader_tests"]) > 0:
                # Sprawdź pierwszy (najnowszy) wpis w historii testów
                latest_test = user_data["neuroleader_tests"][0]
                self.assertEqual(latest_test["dominant_type"], "neuroanalityk")
                print("✅ Znaleziono i zweryfikowano dane testów neuroliderów")
            else:
                self.fail("Nie znaleziono historii testów neuroliderów w danych użytkownika")
            
        except Exception as e:
            self.fail(f"Wystąpił błąd podczas zapisu/odczytu wyników: {str(e)}")
    
    def test_get_resources(self):
        """Sprawdza funkcję pobierania zasobów dla typu neuroliderów."""
        resources = self.neuroleader_types.get_resources_for_type("neuroanalityk")
        self.assertIsNotNone(resources)
        print(f"✅ Pobrano zasoby dla typu neuroanalityk: {len(resources)} elementów")
    
    def test_get_test_history(self):
        """Sprawdza funkcję pobierania historii testów użytkownika."""
        test_history = self.neuroleader_types.get_user_test_history()
        self.assertIsInstance(test_history, list)
        if test_history:
            print(f"✅ Pobrano historię testów użytkownika: {len(test_history)} wpisów")
        else:
            print("ℹ️ Historia testów jest pusta, ale funkcja działa poprawnie")


if __name__ == "__main__":
    print("🧪 Uruchamianie testów funkcjonalności typologii neuroliderów...")
    # Użyj TextTestRunner zamiast unittest.main() aby uzyskać bardziej szczegółowe wyniki
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNeuroliderFeature)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Podsumowanie
    print("\n=== PODSUMOWANIE TESTÓW ===")
    print(f"✅ Liczba testów zakończonych sukcesem: {result.testsRun - len(result.errors) - len(result.failures)}")
    if result.failures:
        print(f"❌ Liczba niepowodzeń: {len(result.failures)}")
        for i, failure in enumerate(result.failures):
            print(f"  Niepowodzenie {i+1}: {failure[0]}")
            print(f"  Szczegóły: {failure[1]}")
    if result.errors:
        print(f"❌ Liczba błędów: {len(result.errors)}")
        for i, error in enumerate(result.errors):
            print(f"  Błąd {i+1}: {error[0]}")
            print(f"  Szczegóły: {error[1]}")
    
    if not result.failures and not result.errors:
        print("✅ Wszystkie testy zakończone sukcesem! Funkcjonalność typologii neuroliderów działa poprawnie.")
    else:
        print("❌ Niektóre testy nie powiodły się. Proszę naprawić problemy przed wdrożeniem.")
