import json
import logging
from typing import Any
from openai import OpenAI
from src.rag.citations import CitationFormatter

logger = logging.getLogger(__name__)

class AnswerService:
    SYSTEM_PROMPT = """
        You are a policy assistant.
 
        Use ONLY the retrieved evidence.
        
        If evidence is insufficient:
        - do not guess
        - return supported=false
        
        Always provide:
        - answer
        - citations
        - limitations
        
        Return ONLY valid JSON:
        {
            "answer": "string",
            "supported": true,
            "evidence": ["chunk_id"],
            "limitations": []
        }
        """
    def __init__(self, client: OpenAI, model: str, citation_formatter: CitationFormatter, min_retrieval_score: float = 0.50,):
        self.client = client
        self.model = model
        self.min_retrieval_score = min_retrieval_score
        self.citation_formatter = citation_formatter

    def validate_retrieval(self, chunks: list[dict[str, Any]],) -> bool:
        if not chunks: return False
        best_score = max(chunk["score"] for chunk in chunks)

        return best_score >= self.min_retrieval_score

    def build_user_prompt(self, question: str, chunks: list[dict[str, Any]],) -> str:
        evidence = []

        for chunk in chunks:
            evidence.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "metadata": chunk["metadata"],
            })

        return f"""
            USER QUESTION:
            {question}

            RETRIEVED EVIDENCE:
            {json.dumps(evidence, indent=2, default=str)}

            Answer using only the retrieved evidence.
            """

    def generate_answer(self, question: str, chunks: list[dict[str, Any]],) -> dict[str, Any]:

            if not self.validate_retrieval(chunks):
                return self.abstain("No sufficiently relevant evidence was retrieved.")

            user_prompt = self.build_user_prompt(question, chunks,)
            response = self.client.chat.completions.create(
                 model = self.model,
                 messages=[
                      {
                           "role": "system",
                           "content": self.SYSTEM_PROMPT,
                      },
                      {
                           "role": "user",
                           "content": user_prompt
                      },
                 ],
                 response_format = {
                      "type": "json_object"
                 },
            )

            answer = json.loads(response.choices[0].message.content)

            if not self.validate_evidence(answer, chunks):
                return self.abstain("The generated answer contains invalid evidence references.")

            return answer

    def abstain(self, reason: str,) -> dict[str, Any]:
         return {
              "answer": (
                   "I cannot provide a reliable answer "
                   "based on the available evidence."
              ),
              "supported": False,
              "citations": [],
              "limitations": [reason],
         }

    def validate_evidence(self, answer: dict[str, Any], chunks: list[dict[str, Any]],) -> bool:
        retrieved_ids = {chunk["chunk_id"] for chunk in chunks}

        cited_ids = answer.get("evidence", [])

        if not isinstance(cited_ids, list):
            return False

        if not all(isinstance(cid, str) for cid in cited_ids):
            return False

        if not set(cited_ids).issubset(retrieved_ids):
            return False

        if answer.get("supported") and not cited_ids:
            return False

        return True