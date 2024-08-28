from semantha_sdk.model.answer import Answer
from semantha_sdk.model.answer import AnswerSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint

class AnswersEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/domains/{domainname}/answers"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/answers"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    
    def post(
        self,
        question: str = None,
        maxreferences: int = None,
        similaritythreshold: float = None,
        language: str = None,
    ) -> Answer:
        """
        Finds references in library for a given question and uses references to generate an answer.
            The 'maxReferences' parameter determines how many library items are used. The language of the answer can be changed via the 'language' parameter.
        Args:
        question (str): The text to find in the library.
    maxreferences (int): Number of references found in library to base the answer on.
    similaritythreshold (float): Threshold used to find matches in library
    language (str): The language for the answer text.
            Supported Languages:
            "ar", "cs", "da", "de", "en", "es", "el", "fr", "fi", "hu", "hr",
            "it", "ja", "ko", "nl", "no", "pl", "pt", "ro", "ru", "sk", "sl",
            "sv", "tr", "zh"
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            body={
                "question": question,
                "maxreferences": maxreferences,
                "similaritythreshold": similaritythreshold,
                "language": language,
            },
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(AnswerSchema)

    
    
    