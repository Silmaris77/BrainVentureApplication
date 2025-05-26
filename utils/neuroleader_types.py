"""
Moduł zarządzający typologią neuroliderów w aplikacji BrainVenture.
"""
import json
import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from datetime import datetime

class NeuroleaderTypes:
    """Klasa do zarządzania typami neuroliderów w aplikacji."""
    
    def __init__(self):
        self.types_data = self._load_types_data()
        self.test_data = self._load_test_data()
        
    def _load_types_data(self):
        """Wczytuje podstawowe dane typów z pliku JSON."""
        try:
            filepath = os.path.join("data", "content", "neuroleader_types.json")
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Nie udało się wczytać danych typów: {e}")
            return []
    
    def _load_test_data(self):
        """Wczytuje dane testu z pliku JSON."""
        try:
            filepath = os.path.join("data", "content", "neuroleader_type_test.json")
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Nie udało się wczytać danych testu: {e}")
            return {"questions": []}
    
    def _load_markdown_content(self, type_id):
        """Wczytuje treść markdowna dla danego typu."""
        filepath = os.path.join("data", "content", "neuroleader_types", f"{type_id}.md")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            st.error(f"Nie udało się wczytać opisu dla typu {type_id}: {e}")
            return ""
    
    def get_all_types(self):
        """Zwraca wszystkie typy neuroliderów."""
        return self.types_data
    
    def get_type_by_id(self, type_id):
        """Zwraca szczegóły konkretnego typu neurolidera."""
        for type_info in self.types_data:
            if type_info["id"] == type_id:
                return type_info
        return None
    
    def get_test_questions(self):
        """Zwraca pytania testowe."""
        return self.test_data.get("questions", [])
    
    def get_test_info(self):
        """Zwraca informacje o teście."""
        return {
            "name": self.test_data.get("test_name", "Test Typologii Neuroliderów"),
            "description": self.test_data.get("description", ""),
            "instructions": self.test_data.get("instructions", "")
        }
    
    def interpret_score(self, type_id, score, max_score):
        """Interpretuje wynik testu dla danego typu."""
        score_interpretation = self.test_data.get("score_interpretation", {})
        if isinstance(score_interpretation, dict):
            interpretations = score_interpretation.get(type_id, {})
        else:
            interpretations = {}
        percentage = score / max_score
        
        if percentage < 0.4:
            return interpretations.get("low", "Niski wynik")
        elif percentage < 0.7:
            return interpretations.get("medium", "Średni wynik")
        else:
            return interpretations.get("high", "Wysoki wynik")
    
    def calculate_test_results(self, answers):
        """
        Oblicza wyniki testu na podstawie odpowiedzi.
        
        Args:
            answers: Słownik z odpowiedziami na pytania testowe (id pytania -> odpowiedź 1-5)
            
        Returns:
            dict: Wyniki testu
        """
        # Inicjalizacja wyników
        results = {
            "neuroanalityk": 0,
            "neuroreaktor": 0,
            "neurobalanser": 0,
            "neuroempata": 0,
            "neuroinnowator": 0,
            "neuroinspirator": 0,
            "question_counts": {
                "neuroanalityk": 0,
                "neuroreaktor": 0,
                "neurobalanser": 0,
                "neuroempata": 0,
                "neuroinnowator": 0,
                "neuroinspirator": 0
            }
        }
        
        # Obliczenie sumy punktów dla każdego typu
        for question in self.get_test_questions():
            q_id = question["id"]
            q_type = question["type"]
            
            if q_id in answers:
                results[q_type] += answers[q_id]
                results["question_counts"][q_type] += 1
        
        # Normalizacja wyników (średnia punktów na pytanie)
        normalized_results = {}
        for type_id, score in results.items():
            if type_id != "question_counts":
                if results["question_counts"][type_id] > 0:
                    normalized_results[type_id] = score / results["question_counts"][type_id]
                else:
                    normalized_results[type_id] = 0
        
        # Znalezienie dominującego i drugorzędnego typu
        sorted_results = sorted(normalized_results.items(), key=lambda x: x[1], reverse=True)
        
        # Przygotuj końcowy wynik
        final_results = {
            "scores": normalized_results,
            "dominant_type": sorted_results[0][0],
            "secondary_type": sorted_results[1][0] if len(sorted_results) > 1 else None,
            "tertiary_type": sorted_results[2][0] if len(sorted_results) > 2 else None,
            "interpretations": {}
        }
        
        # Dodaj interpretacje dla każdego typu
        for type_id, score in normalized_results.items():
            final_results["interpretations"][type_id] = self.interpret_score(
                type_id, score, 5  # 5 to maksymalny wynik na pytanie
            )
        
        return final_results
    
    def save_test_results(self, user_id, results):
        """
        Zapisuje wyniki testu do pliku user_data.json.
        
        Args:
            user_id: ID użytkownika (obecnie niewykorzystywane, na przyszłość)
            results: Wyniki testu do zapisania
            
        Returns:
            bool: True jeśli zapis się powiódł, False w przeciwnym razie
        """
        try:
            # Wczytaj aktualne dane użytkownika
            user_data = self._load_user_data()
            
            # Dodaj lub zaktualizuj dane testu neurolidera
            if "neuroleader_tests" not in user_data:
                user_data["neuroleader_tests"] = []
            
            # Dodaj datę do wyników
            test_result = results.copy()
            test_result["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Dodaj nowy wynik na początku listy (najnowsze na górze)
            user_data["neuroleader_tests"].insert(0, test_result)
            
            # Zapisz zaktualizowane dane
            self._save_user_data(user_data)
            
            return True
        except Exception as e:
            st.error(f"Błąd podczas zapisywania wyników testu: {e}")
            return False
    
    def get_user_test_history(self):
        """
        Pobiera historię testów użytkownika.
        
        Returns:
            list: Lista wyników testów z datami
        """
        try:
            user_data = self._load_user_data()
            return user_data.get("neuroleader_tests", [])
        except Exception as e:
            st.error(f"Błąd podczas pobierania historii testów: {e}")
            return []
    
    def _load_user_data(self):
        """Wczytuje dane użytkownika z pliku JSON."""
        try:
            filepath = os.path.join("data", "content", "user_data.json")
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Nie udało się wczytać danych użytkownika: {e}")
            return {}
    
    def _save_user_data(self, user_data):
        """Zapisuje dane użytkownika do pliku JSON."""
        try:
            filepath = os.path.join("data", "content", "user_data.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Nie udało się zapisać danych użytkownika: {e}")
    
    def render_type_card(self, type_id):
        """Renderuje kartę typu (skrócony widok w liście typów)."""
        type_info = self.get_type_by_id(type_id)
        if not type_info:
            return
            
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Wyświetl ikonę typu
            st.markdown(f"<h1 style='font-size: 3rem; margin: 0;'>{type_info.get('icon', '')}</h1>", unsafe_allow_html=True)
            
            # Wyświetl obrazek jeśli istnieje
            image_path = os.path.join("static", "images", "neuroleader_types", 
                                     type_info.get("image", f"{type_id}.png"))
            if os.path.exists(image_path):
                st.image(image_path, width=120)
        
        with col2:
            # Wyświetl podstawowe informacje
            st.markdown(f"### {type_info['name']}")
            st.markdown(type_info['short_description'])
            
            # Pokaż supermoc i słabość
            col_super, col_weak = st.columns(2)
            with col_super:
                st.markdown(f"**Supermoc:** {type_info.get('supermoc', '')}")
            with col_weak:
                st.markdown(f"**Słabość:** {type_info.get('slabość', '')}")
    
    def render_full_description(self, type_id):
        """Renderuje pełny opis typu z pliku Markdown."""
        markdown_content = self._load_markdown_content(type_id)
        if not markdown_content:
            st.error(f"Nie znaleziono szczegółowego opisu dla typu {type_id}")
            return
            
        # Renderuj markdown bezpośrednio w Streamlit
        st.markdown(markdown_content)
    
    def render_radar_chart(self, results):
        """Renderuje wykres radarowy wyników testu."""
        # Przygotuj dane do wykresu
        categories = []
        values = []
        
        for type_info in self.types_data:
            type_id = type_info["id"]
            categories.append(type_info["name"].split("–")[0].strip())  # Tylko pierwsza część nazwy
            values.append(results["scores"].get(type_id, 0))
        
        # Licz ilość zmiennych
        N = len(categories)
        
        # Co będzie kątem każdej osi w wykresie
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Domknij wykres
        
        # Wartości do wykresu
        values_for_chart = values.copy()
        values_for_chart += values[:1]  # Domknij wykres
        
        # Ustawienia wykresu
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
        
        # Rysuj wykres
        ax.plot(angles, values_for_chart, linewidth=2, linestyle='solid')
        ax.fill(angles, values_for_chart, alpha=0.4)
        
        # Ustaw osie dla każdego kąta i etykiety
        plt.xticks(angles[:-1], categories)
        
        # Ustaw limit osi Y
        ax.set_ylim(0, 5)
        
        # Ustaw etykiety osi Y
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'])
        
        # Dodaj tytuł
        plt.title("Profil neurolidera", size=15, pad=20)
        
        # Wyświetl wykres
        st.pyplot(fig)

    def display_test_history(self):
        """Wyświetla historię testów neuroleaderskich użytkownika."""
        test_history = self.get_user_test_history()
        
        if not test_history:
            st.info("Nie masz jeszcze historii testów neuroleaderskich.")
            return
        
        st.markdown("### Historia testów")
        
        for i, test_result in enumerate(test_history):
            with st.expander(f"Test #{i+1} - {test_result.get('date', 'Data nieznana')}", expanded=(i==0)):
                # Pokaż podstawowe informacje
                dominant_type = self.get_type_by_id(test_result["dominant_type"])
                secondary_type = self.get_type_by_id(test_result["secondary_type"]) if test_result["secondary_type"] else None

                if dominant_type:
                    st.markdown(f"**Dominujący typ:** {dominant_type['icon']} {dominant_type['name']}")
                else:
                    st.markdown("**Dominujący typ:** Nieznany")

                if secondary_type:
                    st.markdown(f"**Drugorzędny typ:** {secondary_type['icon']} {secondary_type['name']}")
                elif test_result.get("secondary_type"):
                    st.markdown("**Drugorzędny typ:** Nieznany")
                
                # Pokaż wykres
                self.render_radar_chart(test_result)

    def display_test_form(self):
        """Wyświetla formularz testu."""
        test_info = self.get_test_info()
        
        st.markdown(f"## {test_info['name']}")
        st.markdown(test_info['description'])
        st.markdown(f"**{test_info['instructions']}**")
        
        # Inicjalizuj odpowiedzi w session state jeśli nie istnieją
        if "neuroleader_test_answers" not in st.session_state:
            st.session_state.neuroleader_test_answers = {}
        
        # Wyświetl formularz z pytaniami
        with st.form("neuroleader_type_test"):
            for q in self.get_test_questions():
                st.markdown(f"**{q['text']}**")
                q_id = q['id']
                
                # Użyj aktualnej wartości z session state jeśli istnieje
                current_value = st.session_state.neuroleader_test_answers.get(q_id, 3)
                
                # Slider z wartościami 1-5
                value = st.slider(
                    "1 = zdecydowanie się nie zgadzam, 5 = zdecydowanie się zgadzam",
                    1, 5, current_value,
                    key=f"question_{q_id}"
                )
                
                # Zapisz odpowiedź do session state
                st.session_state.neuroleader_test_answers[q_id] = value
                st.markdown("---")
            
            # Przycisk do wysłania formularza
            submit = st.form_submit_button("Sprawdź swój typ")
            
        return submit
        
    def get_resources_for_type(self, type_id):
        """
        Zwraca listę zalecanych zasobów dla danego typu neurolidera.
        
        Args:
            type_id: ID typu neurolidera
            
        Returns:
            dict: Słownik z zasobami i materiałami dla danego typu
        """
        # Baza zasobów dla każdego typu
        resources = {
            "neuroanalityk": {
                "kursy": [
                    "Szybkie podejmowanie decyzji – dla analitycznych umysłów",
                    "Praktyczne metody zarządzania stresem decyzyjnym",
                    "Równowaga między analizą a intuicją w przywództwie"
                ],
                "książki": [
                    "\"Decyduj szybciej, myśl wolniej\" – Daniel Kahneman",
                    "\"Sztuka podejmowania dobrych decyzji\" – Chip & Dan Heath",
                    "\"Przełam swój perfekcjonizm\" – Martin Antony"
                ],
                "ćwiczenia": [
                    "Dziennik decyzji – zapisuj codziennie jedną decyzję podjętą intuicyjnie",
                    "Technika Pomodoro do ograniczania czasu analizy",
                    "Medytacja uważności przed podjęciem ważnych decyzji"
                ],
                "materiały": [
                    "Szablon do podejmowania decyzji metodą 80/20",
                    "Narzędzie do szybkiej analizy ryzyka",
                    "Karty z pytaniami decyzyjnymi do użycia przy impasie"
                ]
            },
            "neuroreaktor": {
                "kursy": [
                    "Mindfulness dla liderów pod presją",
                    "Kontrola emocji w sytuacjach stresowych",
                    "Strategiczne podejście do zarządzania kryzysem"
                ],
                "książki": [
                    "\"Emotional Intelligence 2.0\" – Travis Bradberry",
                    "\"Mindfulness dla zabieganych\" – Pedram Shojai",
                    "\"Mózg odporny na stres\" – Melanie Greenberg"
                ],
                "ćwiczenia": [
                    "10-sekundowa pauza przed reakcją w sytuacjach stresowych",
                    "Ćwiczenia oddechowe 4-7-8",
                    "Technika STOP: Zatrzymaj się, Weź oddech, Obserwuj, Postępuj"
                ],
                "materiały": [
                    "Karta szybkiej analizy konsekwencji",
                    "Aplikacja do monitorowania poziomu stresu",
                    "Zestaw list kontrolnych do podejmowania decyzji w kryzysie"
                ]
            },
            "neurobalanser": {
                "kursy": [
                    "Zaawansowana inteligencja emocjonalna w przywództwie",
                    "Integracja myślenia analitycznego i empatycznego",
                    "Przywództwo adaptacyjne w zmiennym otoczeniu"
                ],
                "książki": [
                    "\"Inteligencja emocjonalna lidera\" – Daniel Goleman",
                    "\"Równowaga: Sztuka podejmowania decyzji\" – Chip & Dan Heath",
                    "\"Zwinne przywództwo\" – Simon Hayward"
                ],
                "ćwiczenia": [
                    "Mentoring dla innych typów neuroliderów",
                    "Facylitacja dyskusji w zespołach o zróżnicowanych stylach",
                    "Dziennik równowagi – monitorowanie decyzji i ich podstaw"
                ],
                "materiały": [
                    "Matryca decyzyjna integrująca dane i emocje",
                    "Narzędzie do mapowania stylów komunikacji w zespole",
                    "Framework do zrównoważonego coachingu zespołowego"
                ]
            },
            "neuroempata": {
                "kursy": [
                    "Asertywność dla empatycznych liderów",
                    "Podejmowanie trudnych decyzji bez wypalenia emocjonalnego",
                    "Analityczne podejście do problemów dla empatycznych liderów"
                ],
                "książki": [
                    "\"Granice – kiedy mówić TAK, jak mówić NIE\" – Henry Cloud",
                    "\"Empatia w przywództwie\" – Michael Ventura",
                    "\"Od empatii do działania\" – Indi Young"
                ],
                "ćwiczenia": [
                    "Technika wewnętrznej rady doradczej",
                    "Asertywne komunikaty JA w sytuacjach konfliktowych",
                    "Dziennik granic emocjonalnych"
                ],
                "materiały": [
                    "Szablon do podejmowania decyzji opartych na danych",
                    "Narzędzie do analizy kosztów i korzyści decyzji",
                    "Zestaw ćwiczeń budujących odporność emocjonalną"
                ]
            },
            "neuroinnowator": {
                "kursy": [
                    "Od innowacji do implementacji – strukturyzacja procesu kreatywnego",
                    "Komunikacja wizji i angażowanie innych",
                    "Techniki zarządzania projektami dla innowatorów"
                ],
                "książki": [
                    "\"Od pomysłu do wdrożenia\" – Scott Belsky",
                    "\"Dyscyplina w kreacji\" – Ed Catmull",
                    "\"Sprint – jak rozwiązywać problemy\" – Jake Knapp"
                ],
                "ćwiczenia": [
                    "5 minut dziennie na planowanie małych kroków",
                    "Technika prototypowania – od wizji do minimalnego produktu",
                    "Dziennik refleksji nad wdrożeniami innowacji"
                ],
                "materiały": [
                    "Canvas do systematyzacji procesu innowacji",
                    "Narzędzie do śledzenia postępów we wdrażaniu pomysłów",
                    "Szablon prezentacji angażującej dla nowych pomysłów"
                ]
            },
            "neuroinspirator": {
                "kursy": [
                    "Aktywne słuchanie dla charyzmatycznych liderów",
                    "Podejmowanie decyzji oparte o dane",
                    "Delegowanie i budowanie autonomii zespołu"
                ],
                "książki": [
                    "\"Sztuka słuchania\" – Nancy Kline",
                    "\"Przywództwo oparte na danych\" – Carl Anderson",
                    "\"Lider jutra\" – Michael Useem"
                ],
                "ćwiczenia": [
                    "Technika 'milczącej burzy mózgów' – dawanie przestrzeni innym",
                    "Ćwiczenie w podejmowaniu decyzji na podstawie danych",
                    "Dziennik samoświadomości przywódczej"
                ],
                "materiały": [
                    "Framework do systematycznego delegowania zadań",
                    "Narzędzie do analizy danych z prostym interfejsem",
                    "Szablon do follow-up po spotkaniach motywacyjnych"
                ]
            }
        }
        
        return resources.get(type_id, {"kursy": [], "książki": [], "ćwiczenia": [], "materiały": []})
