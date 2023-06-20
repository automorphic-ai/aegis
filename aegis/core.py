# -*- coding: utf-8 -*-
import os
import requests


class Aegis:
    """Aegis API client."""

    BASE_URL = "https://api.automorphic.ai/aegis"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("AEGIS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "AEGIS_API_KEY must be set in the environment or passed into the client."
            )

    def ingress(
        self,
        prompt: str,
        user_input: str,
        strength: int = 1,
        heuristic_score_threshold: float = 0.75,
        vector_score_threshold: float = 0.9,
    ):
        """
        Send a prompt and user input to Aegis for evaluation before sending to the model.

        :param prompt: The prompt/task/system instructions given to the model.
        :param user_input: The user input to evaluate.
        :param strength: The strength/rigor of Aegis's evaluation (potential values: 1, 2, 3). 1 is the default
        (and best in terms of the cost-accuracy tradeoff). 3 is the most expensive and cleverest,
        with the lowest risk of false positives, but also a higher risk of false negatives—
        don't use it unless you're using it alongside an exceptionally intelligent model like GPT-4.
        :param heuristic_score_threshold: Indicates the tolerable level of lexical similarity to previously seen attacks (between 0 and 1)
        :param vector_score_threshold: Indicates the tolerable level of semantic similarity to previously seen attacks (between 0 and 1)
        :return: A dictionary of the form `{"detected": bool}` reflecting whether or not an attack was detected.
        """
        if strength not in [1, 2, 3]:
            raise ValueError("strength must be 1, 2, or 3")

        if heuristic_score_threshold < 0 or heuristic_score_threshold > 1:
            raise ValueError("heuristic_score_threshold must be between 0 and 1")

        if vector_score_threshold < 0 or vector_score_threshold > 1:
            raise ValueError("vector_score_threshold must be between 0 and 1")

        response = requests.post(
            f"{Aegis.BASE_URL}/ingress",
            headers={"X-API-Key": self.api_key},
            json={
                "prompt": prompt,
                "user": user_input,
                "strength": strength,
                "heuristic_score": heuristic_score_threshold,
                "vector_score": vector_score_threshold,
            },
        )
        return response.json()

    def egress(
        self,
        prompt: str,
        model_response: str,
        censored_words: list[str] | None = None,
        # censor_similar_words: bool = False,
    ):
        """
        Send a prompt and the model's response to Aegis for evaluation.

        :param prompt: The prompt/task/system instructions given to the model.
        :param model_response: The model's response to evaluate.
        :param censored_words: A list of words to censor in the model's response.
        :param censor_similar_words: Whether or not to censor words semantically similar to those in the censored_words list.
        :return: A dictionary of the form `{"detected": bool}` reflecting whether or not an attack was detected.
        """
        if not censored_words:
            censored_words = []

        response = requests.post(
            f"{Aegis.BASE_URL}/egress",
            headers={"X-API-Key": self.api_key},
            # TODO: Support censor_similar_words
            json={
                "prompt": prompt,
                "model": model_response,
                "censored_words": censored_words,
                # "censor_similar_words": censor_similar_words,
            },
        )
        return response.json()

    def report(self, prompt: str, user_input: str):
        """
        Report an attack to Aegis.

        :param prompt: The prompt/task/system instructions given to the model.
        :param user_input: The malicious user input.
        """
        response = requests.post(
            f"{Aegis.BASE_URL}/report",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "user": user_input},
        )
        return response.json()
