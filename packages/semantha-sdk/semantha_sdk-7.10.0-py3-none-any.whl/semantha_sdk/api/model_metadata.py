from semantha_sdk.api.model_onemetadata import ModelOnemetadataEndpoint
from semantha_sdk.model.model_metadata import ModelMetadata
from semantha_sdk.model.model_metadata import ModelMetadataSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from typing import List

class ModelMetadataEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/model/domains/{domainname}/metadata"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/metadata"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def __call__(
            self,
            id: str,
    ) -> ModelOnemetadataEndpoint:
        return ModelOnemetadataEndpoint(self._session, self._endpoint, id)

    def get(
        self,
    ) -> List[ModelMetadata]:
        """
        Get metadata
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(ModelMetadataSchema)

    def post(
        self,
        body: ModelMetadata = None,
    ) -> ModelMetadata:
        """
        Create metadata
        Args:
        body (ModelMetadata): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=ModelMetadataSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(ModelMetadataSchema)

    
    def delete(
        self,
    ) -> None:
        """
        Delete all metadata
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    