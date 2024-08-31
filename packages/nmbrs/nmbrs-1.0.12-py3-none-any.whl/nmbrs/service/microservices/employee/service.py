# pylint: disable=line-too-long
"""Microservice responsible for service related actions on the employee level."""
import logging

from zeep import Client

from ..micro_service import MicroService
from ....auth.token_manager import AuthManager
from ....utils.nmbrs_exception_handler import nmbrs_exception_handler

logger = logging.getLogger(__name__)


class EmployeeServiceService(MicroService):
    """Microservice responsible for service related actions on the employee level."""

    def __init__(self, auth_manager: AuthManager, client: Client):
        super().__init__(auth_manager, client)

    @nmbrs_exception_handler(resource="EmployeeService:Service_GetList")
    def get_all(self):
        """
        Get all service intervals.

        For more information, refer to the official documentation:
            [Service_GetList](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_GetList)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Service_Insert")
    def post(self):
        """
        Start a new service interval. If the date is before the company's current period, unprotected mode flag is required.

        For more information, refer to the official documentation:
            [Service_Insert](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_Insert)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Service_Insert2")
    def post_2(self):
        """
        Start a new service interval. If the date is before the company's current period, unprotected mode flag is required.

        For more information, refer to the official documentation:
            [Service_Insert2](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_Insert2)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Service_Delete")
    def delete(self):
        """
        Delete a service interval.

        For more information, refer to the official documentation:
            [Service_Delete](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_Delete)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Service_StopCurrent")
    def stop_current(self):
        """
        Stop the current service interval. If the date is before the company's current period, unprotected mode flag is required.
        If the employee income type requires and the employee is an applicant the EndServiceReasonId is mandatory, otherwise this field is ignored whatever the value is passed.

        For more information, refer to the official documentation:
            [Service_StopCurrent](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_StopCurrent)
        """
        raise NotImplementedError()  # pragma: no cover

    @nmbrs_exception_handler(resource="EmployeeService:Service_RemoveOutService")
    def remove_out_service(self):
        """
        Remove out of service date.

        For more information, refer to the official documentation:
            [Service_RemoveOutService](https://api.nmbrs.nl/soap/v3/EmployeeService.asmx?op=Service_RemoveOutService)
        """
        raise NotImplementedError()  # pragma: no cover
