from io import BytesIO


def test_rag_upload_and_query_without_llm(client, auth_header):
    content = (
        "Methodology: this study uses retrieval-augmented generation over PDF chunks.\n\n"
        "Findings: students completed roadmaps faster when resources were categorized.\n\n"
        "Conclusions: a unified interface reduced context switching between tools."
    )
    response = client.post(
        "/api/rag/upload",
        data={"title": "Study notes", "file": (BytesIO(content.encode()), "notes.txt")},
        content_type="multipart/form-data",
        headers=auth_header,
    )
    assert response.status_code == 201
    doc_id = response.get_json()["data"]["id"]
    query = client.post(
        "/api/rag/query",
        json={"document_id": doc_id, "question": "What methodology was used?"},
        headers=auth_header,
    )
    assert query.status_code == 200
    payload = query.get_json()["data"]
    assert payload["retrieved_chunks"]
    assert payload["llm_configured"] is False
    assert payload["answer"] is None
