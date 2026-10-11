import chromadb


DOCUMENTS = {
    "doc-austria": "Vienna is the capital of Austria.",
    "doc-france": "Paris is the capital of France.",
    "doc-japan": "Tokyo is the capital of Japan.",
}


def simple_embedding(text: str) -> list[float]:
    """Tiny deterministic embedding for an offline homework demo."""
    keywords = ["austria", "vienna", "france", "paris", "japan", "tokyo", "capital"]
    lowered = text.lower()
    return [1.0 if word in lowered else 0.0 for word in keywords]


def main() -> None:
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="homework_collection")

    ids = list(DOCUMENTS.keys())
    documents = list(DOCUMENTS.values())
    embeddings = [simple_embedding(document) for document in documents]

    collection.upsert(ids=ids, documents=documents, embeddings=embeddings)

    query = "What is the capital of Austria?"
    results = collection.query(
        query_embeddings=[simple_embedding(query)],
        n_results=2,
        include=["documents", "distances"],
    )

    print(f"Query: {query}")
    print("Top 2 results:")
    for rank, (doc_id, document, distance) in enumerate(
        zip(results["ids"][0], results["documents"][0], results["distances"][0]),
        start=1,
    ):
        print(f"{rank}. {doc_id}: {document} (distance: {distance:.4f})")


if __name__ == "__main__":
    main()

