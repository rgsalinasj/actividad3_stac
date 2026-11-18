import os
import re
import sys
import unicodedata
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Lista de stopwords comunes en español para filtrado léxico ligero
SPANISH_STOPWORDS = [
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
    "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
    "ellas", "ellos", "en", "entre", "era", "eran", "es", "esa", "esas", "ese", "eso",
    "esos", "esta", "estaba", "estado", "estan", "estar", "estas", "este", "esto",
    "estos", "fue", "fueron", "ha", "han", "hasta", "hay", "la", "las", "le", "les",
    "lo", "los", "mas", "me", "mi", "mis", "mucho", "muy", "nada", "ni", "no", "nos",
    "nuestra", "nuestro", "o", "os", "otra", "otras", "otro", "otros", "para", "pero",
    "poco", "por", "porque", "que", "quien", "se", "sea", "segun", "ser", "si", "sin",
    "sobre", "somos", "son", "su", "sus", "tambien", "te", "tiene", "tienen", "todo",
    "todos", "tras", "tu", "tus", "un", "una", "uno", "unos", "usted", "ustedes", "y", "ya"
]


def remove_accents(text: str) -> str:
    """Normaliza vocales acentuadas para evitar discrepancias por tildes omitidas."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def clean_text(text: str) -> str:
    """
    Preprocesamiento mínimo de texto:
    - Conversión a minúsculas
    - Normalización de acentos
    - Eliminación de caracteres especiales y puntuación
    - Limpieza de espacios múltiples
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class DocumentRecommender:
    """Recomendador Top-K basado en contenido utilizando TF-IDF y similitud del coseno."""

    def __init__(self, corpus_path: str = "corpus.csv"):
        self.corpus_path = corpus_path
        self.df = self._load_corpus()
        self.vectorizer = TfidfVectorizer(
            stop_words=SPANISH_STOPWORDS,
            ngram_range=(1, 2),
            max_features=5000
        )
        self.tfidf_matrix = self._fit_corpus()

    def _load_corpus(self) -> pd.DataFrame:
        """Carga y valida el repositorio de documentos CSV."""
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(
                f"No se encontró el archivo '{self.corpus_path}'. "
                "Ejecute primero 'python generate_corpus.py'."
            )

        df = pd.read_csv(self.corpus_path)
        required_cols = {"id", "title", "text"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"El corpus debe contener las columnas obligatorias: {required_cols}")

        if df["id"].duplicated().any():
            raise ValueError("Se detectaron identificadores (id) duplicados en el corpus.")

        df["id"] = df["id"].astype(str).str.strip().str.upper()
        if "category" not in df.columns:
            df["category"] = "Sin categoría"

        # Combinar título y cuerpo para enriquecer la representación vectorial
        df["combined_clean"] = (
            df["title"].fillna("") + " " + df["text"].fillna("")
        ).apply(clean_text)

        return df

    def _fit_corpus(self):
        """Vectoriza el corpus limpio mediante TF-IDF."""
        return self.vectorizer.fit_transform(self.df["combined_clean"])

    def recommend_by_id(self, doc_id: str, top_k: int = 5) -> pd.DataFrame:
        """
        Devuelve los Top-K documentos más similares a un ID semilla,
        excluyendo explícitamente el propio documento semilla.
        """
        if not doc_id or not doc_id.strip():
            raise ValueError("El ID del documento no puede estar vacío.")

        normalized_id = doc_id.strip().upper()
        matches = self.df.index[self.df["id"] == normalized_id].tolist()

        if not matches:
            ejemplos = ", ".join(self.df["id"].head(5).tolist())
            raise KeyError(
                f"El ID '{normalized_id}' no existe en el repositorio. "
                f"Ejemplos válidos: {ejemplos} ... ({len(self.df)} documentos en total)."
            )

        seed_idx = matches[0]
        seed_vector = self.tfidf_matrix[seed_idx]
        similarities = cosine_similarity(seed_vector, self.tfidf_matrix).flatten()

        # Excluir el propio documento semilla
        similarities[seed_idx] = -1.0

        top_indices = similarities.argsort()[::-1][:top_k]
        results = self.df.iloc[top_indices][["id", "title", "category"]].copy()
        results["similarity_score"] = similarities[top_indices].round(4)
        return results.reset_index(drop=True)

    def recommend_by_text(self, query_text: str, top_k: int = 5) -> pd.DataFrame:
        """
        Devuelve los Top-K documentos más similares a una consulta en texto libre.
        """
        cleaned_query = clean_text(query_text)
        if not cleaned_query:
            raise ValueError("La consulta no puede estar vacía ni contener solo símbolos.")

        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        top_indices = similarities.argsort()[::-1][:top_k]
        results = self.df.iloc[top_indices][["id", "title", "category"]].copy()
        results["similarity_score"] = similarities[top_indices].round(4)
        return results.reset_index(drop=True)

    def get_document_info(self, doc_id: str) -> dict:
        """Obtiene los metadatos de un documento por su ID."""
        normalized_id = doc_id.strip().upper()
        row = self.df[self.df["id"] == normalized_id].iloc[0]
        return row.to_dict()


def print_results(results: pd.DataFrame) -> None:
    """Imprime en consola la tabla formateada con los resultados Top-K."""
    print("-" * 92)
    print(f"{'Pos.':<5} | {'ID':<7} | {'Similitud':<9} | {'Categoría':<21} | {'Título'}")
    print("-" * 92)
    for idx, row in results.iterrows():
        print(
            f"{idx + 1:<5} | {row['id']:<7} | {row['similarity_score']:<9.4f} | "
            f"{row['category']:<21} | {row['title']}"
        )
    print("-" * 92)


def run_validation_tests(recommender: DocumentRecommender) -> None:
    """Ejecuta las tres pruebas obligatorias de validación y muestra evidencia estructurada."""
    print("\n" + "=" * 92)
    print("SUITE DE VALIDACIÓN: RECOMENDADOR DE DOCUMENTOS TOP-K (SIMILITUD DEL COSENO)")
    print("=" * 92)

    # PRUEBA 1: Documento semilla de Politicas/Procesos
    seed_1 = "DOC001"
    info_1 = recommender.get_document_info(seed_1)
    print("\n[PRUEBA 1 - Documento Semilla de Politicas/Procesos]")
    print(f"Entrada (ID) : {seed_1} — '{info_1['title']}' ({info_1['category']})")
    print(f"Contenido    : {info_1['text']}")
    res_1 = recommender.recommend_by_id(seed_1, top_k=5)
    print_results(res_1)

    # PRUEBA 2: Documento semilla de Soporte/Incidentes
    seed_2 = "DOC017"
    info_2 = recommender.get_document_info(seed_2)
    print("\n[PRUEBA 2 - Documento Semilla de Soporte/Incidentes]")
    print(f"Entrada (ID) : {seed_2} — '{info_2['title']}' ({info_2['category']})")
    print(f"Contenido    : {info_2['text']}")
    res_2 = recommender.recommend_by_id(seed_2, top_k=5)
    print_results(res_2)

    # PRUEBA 3: Consulta en texto libre
    query_3 = (
        "Un empleado extravió su teléfono celular personal donde tenía instalado el correo "
        "corporativo y la mensajería. ¿Cómo realizamos el borrado remoto y protegemos sus credenciales?"
    )
    print("\n[PRUEBA 3 - Consulta de Texto Libre]")
    print(f"Entrada (Texto): \"{query_3}\"")
    res_3 = recommender.recommend_by_text(query_3, top_k=5)
    print_results(res_3)


def interactive_cli(recommender: DocumentRecommender) -> None:
    """Interfaz interactiva por consola para consulta por ID o texto libre."""
    print("\n=== Sistema Recomendador de Documentos Top-K ===")
    print(f"Repositorio cargado: {len(recommender.df)} documentos desde '{recommender.corpus_path}'.")

    while True:
        print("\nSeleccione una opción:")
        print("  1. Recomendar por ID de documento (ej. DOC001)")
        print("  2. Recomendar por consulta de texto libre")
        print("  3. Listar todos los IDs de documentos disponibles")
        print("  4. Salir")

        choice = input("Ingrese su opción (1-4): ").strip()

        if choice == "1":
            doc_id = input("Ingrese el ID del documento semilla: ").strip()
            try:
                info = recommender.get_document_info(doc_id)
                print(f"\nDocumento Semilla: [{info['id']}] {info['title']} ({info['category']})")
                results = recommender.recommend_by_id(doc_id, top_k=5)
                print_results(results)
            except (ValueError, KeyError) as e:
                print(f"[Error] {e}")

        elif choice == "2":
            query = input("Pegue o escriba el texto de consulta: ").strip()
            try:
                print(f"\nConsulta: \"{query}\"")
                results = recommender.recommend_by_text(query, top_k=5)
                print_results(results)
            except ValueError as e:
                print(f"[Error] {e}")

        elif choice == "3":
            for _, row in recommender.df.iterrows():
                print(f"  {row['id']} | {row['category']:<21} | {row['title']}")

        elif choice == "4":
            print("Saliendo del recomendador. ¡Hasta pronto!")
            break
        else:
            print("[Opción inválida] Por favor ingrese 1, 2, 3 o 4.")


if __name__ == "__main__":
    try:
        rec = DocumentRecommender("corpus.csv")
        if "--run-tests" in sys.argv:
            run_validation_tests(rec)
        else:
            interactive_cli(rec)
    except Exception as err:
        print(f"Error de inicialización: {err}")
