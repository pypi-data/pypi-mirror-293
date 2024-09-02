import asyncio
import os
import aiohttp
import requests
import json
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from threading import Lock
from .utils.twingenio_faker import TwingenioFaker
from .utils.errors import ErrCode
from .models.twingenio_api_models import (
    ExtSigninResponseData,
    ExtInfoResponse,
    ExtGetReceiptResponse,
    ExtSetReceiptResponse,
)

from flask import current_app, session
from .utils.constants import TwingenioConstants
from .utils.keys import AlfredKeys
from .utils.errors import RemoteServiceError
from .utils.in_memory_user import InMemoryUser
from .logger import get_logger

# ==============================================================================
# region Constants and Enums
# ==============================================================================
TGCLIENT_APPTOKEN_KEY = "TGCLIENT_APPTOKEN_KEY"

logger = get_logger()


class TwingenioEndpoints:
    """
    Enumerazione degli endpoint API di Twingenio.

    Questa classe contiene le costanti per i percorsi degli endpoint
    utilizzati nelle chiamate API a Twingenio.
    """

    # --------------------------------------------------------------------------
    # Endpoint per l'autenticazione dell'agente singolo
    SINGLEAGENT_SIGNIN = "/ext/signin"

    # --------------------------------------------------------------------------
    # Endpoint per ottenere informazioni sull'agente
    INFO = "/ext/info"

    # --------------------------------------------------------------------------
    # Endpoint per ottenere la ricevuta (verifica del budget)
    GET_RECEIPT = "/ext/get_receipt"

    # --------------------------------------------------------------------------
    # Endpoint per impostare la ricevuta (finalizzazione del budget)
    SET_RECEIPT = "/ext/set_receipt"


# endregion


# ==============================================================================
# region TwingenioClient Class
# ==============================================================================


class TwingenioClient:
    _instance = None
    _lock = Lock()
    _server_url = None

    # ==============================================================================
    # region Initialization and Instance Management
    # ==============================================================================

    @classmethod
    def get_instance(cls):
        logger.debug("TwingenioClient.get_instance()::start")
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger.debug("TwingenioClient.get_instance()::nuova istanza")
                    cls._instance = cls()
        logger.debug("TwingenioClient.get_instance()::end")
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.mock_responses = TwingenioFaker()
            server_url = self.__class__._server_url
            env_backend = os.getenv(AlfredKeys.TWINGENIO_BACKEND)
            logger.debug(f"TwingenioClient.__init__::server_url={server_url}")
            logger.debug(
                f"TwingenioClient.__init__::AlfredKeys.TWINGENIO_BACKEND={env_backend}"
            )
            # self.base_url = self._server_url if self._server_url else env_backend
            if self.base_url == TwingenioConstants.OVERRIDE_BACKENDURL_CONST:
                self.base_url = env_backend
            else:
                self.base_url = server_url  # server_url può anche essere vuota

    # endregion
    # ==============================================================================

    # ==============================================================================
    # region Helper Methods
    # ==============================================================================

    @staticmethod
    def set_apptoken(token: str):
        """Memorizza l'apptoken in sessione"""
        session[TGCLIENT_APPTOKEN_KEY] = token

    @staticmethod
    def get_apptoken() -> str:
        """Recupera l'apptoken dalla sessione"""
        return session[TGCLIENT_APPTOKEN_KEY]

    # @classmethod
    # def set_server_url(cls, url: str, override: bool):
    #     logger.debug(
    #         f"TwingenioClient.set_url(PRE)::self.base_url={cls._server_url};self.override={cls._override}"
    #     )
    #     cls._override = override
    #     cls._server_url = url
    #     logger.debug(
    #         f"TwingenioClient.set_url(POST)::self.base_url={cls._server_url};self.override={cls._override}"
    #     )

    @classmethod
    def set_server_url(cls, url: str):
        logger.debug(f"TwingenioClient.set_url(PRE)::self.base_url={cls._server_url}")
        cls._server_url = url
        logger.debug(f"TwingenioClient.set_url(POST)::self.base_url={cls._server_url}")

    def _get_base_url(self) -> str:
        return self.base_url

    def _avoid_remote_call(self) -> bool:
        return self._get_base_url() == ""

    def _prepare_json_for_submit(self, data: str) -> dict[str, str]:
        return {"params": json.dumps(data)}

    def _prepare_apptoken(self, apptoken, params={}):
        form_data = {"params": json.dumps(params)}
        if apptoken:
            form_data["apptoken"] = apptoken
        return form_data

    # endregion
    # ==============================================================================

    # ==============================================================================
    # region Authentication Methods
    # ==============================================================================

    def signin(self, email: str, password: str) -> ExtSigninResponseData:
        """
        Sign in to the application using the remote API or mock data.

        :param email: The email of the user.
        :param password: The password of the user.
        :return: LoginData containing session and user information.
        :raises RemoteServiceError: If the API request fails or returns an error.
        """
        skill_id = os.getenv(AlfredKeys.SKILL_ID)
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = self._mock_signin(email)
            else:
                response_data, status_code = self._remote_signin(
                    email, password, skill_id
                )

            call_data = ExtSigninResponseData.model_validate(response_data)
            if status_code == 200:
                TwingenioClient.set_apptoken(call_data.data.apptoken)
                return call_data
            elif (
                call_data.is_error
                and call_data.data.error_code == ErrCode.ERR_LOGIN_INVALID
            ):
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except requests.RequestException as e:
            raise RemoteServiceError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise RemoteServiceError(f"Invalid response format: {str(e)}")

    def _mock_signin(self, email: str):
        if "john" in email:
            return self.mock_responses.ext_signin_response_1001, 200
        elif "wolf" in email:
            return self.mock_responses.ext_signin_response_1002, 200
        else:
            return self.mock_responses.signin_denied, 500

    def _remote_signin(self, email: str, password: str, skill_id: str):
        url = f"{self.base_url}{TwingenioEndpoints.SINGLEAGENT_SIGNIN}"
        data = {"email": email, "password": password, "skill_id": skill_id}
        response = requests.post(url, data=self._prepare_json_for_submit(data))
        return response.json(), response.status_code

    # endregion
    # ==============================================================================

    # ==============================================================================
    # region Information Methods
    # ==============================================================================

    def info_agent(self, apptoken: str) -> ExtInfoResponse:
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = self._mock_info_agent(apptoken)
            else:
                response_data, status_code = self._remote_info_agent(apptoken)

            call_data = ExtInfoResponse.model_validate(response_data)
            if status_code == 200:
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except requests.RequestException as e:
            raise RemoteServiceError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise RemoteServiceError(f"Invalid response format: {str(e)}")

    def _mock_info_agent(self, apptoken: str):
        if apptoken[-4:] == "1001":
            return self.mock_responses.ext_info_response_1001_voice, 200
            # return self.mock_responses.ext_info_response_1001_llama, 200
            # return self.mock_responses.ext_info_response_1001_claude, 200
        elif apptoken[-4:] == "1002":
            return self.mock_responses.ext_info_response_1002, 200
        else:
            return self.mock_responses.ext_info_err, 500

    def _remote_info_agent(self, apptoken: str):
        url = f"{self.base_url}{TwingenioEndpoints.INFO}"
        response = requests.post(url, data=self._prepare_apptoken(apptoken))
        return response.json(), response.status_code

    # endregion
    # ==============================================================================

    # ==============================================================================
    # region Budget Methods
    # ==============================================================================

    def check_budget(self, apptoken: str, action_id: str) -> ExtGetReceiptResponse:
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = self.mock_responses.credit_enough, 200
            else:
                response_data, status_code = self._remote_check_budget(
                    apptoken, action_id
                )

            call_data = ExtGetReceiptResponse.model_validate(response_data)
            if status_code == 200:
                return call_data
            elif (
                call_data.is_error
                and call_data.data.error_code == ErrCode.ERR_TOKEN_INSUFFICIENT_BALANCE
            ):
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except requests.RequestException as e:
            raise RemoteServiceError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise RemoteServiceError(f"Invalid response format: {str(e)}")

    def _remote_check_budget(self, apptoken: str, action_id: str):
        url = f"{self.base_url}{TwingenioEndpoints.GET_RECEIPT}"
        data = {"action_id": action_id}
        response = requests.post(url, data=self._prepare_apptoken(apptoken, data))
        return response.json(), response.status_code

    async def async_check_budget(
        self, apptoken: str, action_id: str
    ) -> ExtSigninResponseData:
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = self.mock_responses.credit_enough, 200
            else:
                response_data, status_code = await self._async_remote_check_budget(
                    apptoken, action_id
                )

            call_data = ExtGetReceiptResponse.model_validate(response_data)
            if status_code == 200:
                return call_data
            elif (
                call_data.is_error
                and call_data.data.error_code == ErrCode.ERR_TOKEN_INSUFFICIENT_BALANCE
            ):
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except aiohttp.ClientError as e:
            raise RemoteServiceError(f"Failed to check credit: {str(e)}")

    async def _async_remote_check_budget(self, apptoken: str, action_id: str):
        url = f"{self.base_url}{TwingenioEndpoints.GET_RECEIPT}"
        data = {"action_id": action_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=self._prepare_apptoken(apptoken, data)
            ) as response:
                return await response.json(), response.status

    def finalize_budget(
        self, apptoken: str, receipt_id: str, executed: bool
    ) -> ExtSetReceiptResponse:
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = (
                    self.mock_responses.finalize_credit_response,
                    200,
                )
            else:
                response_data, status_code = self._remote_finalize_budget(
                    apptoken, receipt_id, executed
                )

            call_data = ExtSetReceiptResponse.model_validate(response_data)
            if status_code == 200:
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except requests.RequestException as e:
            raise RemoteServiceError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise RemoteServiceError(f"Invalid response format: {str(e)}")

    def _remote_finalize_budget(self, apptoken: str, receipt_id: str, executed: bool):
        url = f"{self.base_url}{TwingenioEndpoints.SET_RECEIPT}"
        data = {
            "receipt_id": receipt_id,
            "executed": executed,
        }
        response = requests.post(url, data=self._prepare_apptoken(apptoken, data))
        return response.json(), response.status_code

    async def async_finalize_budget(
        self, apptoken: str, receipt_id: str, executed: bool
    ) -> ExtSetReceiptResponse:
        status_code = 0
        try:
            if self._avoid_remote_call():
                response_data, status_code = (
                    self.mock_responses.finalize_credit_response,
                    200,
                )
            else:
                response_data, status_code = await self._async_remote_finalize_budget(
                    apptoken, receipt_id, executed
                )

            call_data = ExtSetReceiptResponse.model_validate(response_data)
            if status_code == 200:
                return call_data
            else:
                raise NotImplementedError(
                    f"Errore da gestire: error_code:{call_data.data.error_code}, error_message:{call_data.data.error_message}"
                )

        except aiohttp.ClientError as e:
            raise RemoteServiceError(f"Failed to check credit: {str(e)}")

    async def _async_remote_finalize_budget(
        self, apptoken: str, receipt_id: str, executed: bool
    ):
        url = f"{self.base_url}{TwingenioEndpoints.SET_RECEIPT}"
        data = {
            "receipt_id": receipt_id,
            "executed": executed,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=self._prepare_apptoken(apptoken, data)
            ) as response:
                return await response.json(), response.status

    # endregion
    # ==============================================================================


# endregion
# ==============================================================================
