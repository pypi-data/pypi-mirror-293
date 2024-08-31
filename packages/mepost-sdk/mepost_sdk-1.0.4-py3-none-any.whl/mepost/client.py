import requests
from .config import MepostConfig
from .helpers import send_request
from .models.requests import *
from .models.responses import *


class MepostClient:
    def __init__(self, api_key: str):
        self.config = MepostConfig(api_key)

    # Company Endpoints
    def add_domain(self, request: AddDomainRequest) -> Response[AddDomainResponse]:
        return send_request('POST', '/company/domain/add', request, self.config)

    def get_domain_list(self) -> Response[CompanyDomain]:
        return send_request('GET', '/company/domain/list', config=self.config)

    def remove_domain(self, request: AddDomainRequest) -> Response[RemoveDomainResponse]:
        return send_request('DELETE', '/company/domain/remove', request, self.config)

    # Groups Endpoints
    def list_groups(self, limit: int = 10, page: int = 1) -> Response[BaseResult[EmailGroup]]:
        return send_request('GET', f'/groups?limit={limit}&page={page}', config=self.config)

    def create_group(self, request: CreateNewGroupRequest) -> Response[EmailGroup]:
        return send_request('POST', '/groups', request, self.config)

    def delete_group(self, group_id: str) -> Response[bool]:
        return send_request('DELETE', f'/groups/{group_id}', config=self.config)

    def get_group_by_id(self, group_id: str) -> Response[EmailGroupWithCounts]:
        return send_request('GET', f'/groups/{group_id}', config=self.config)

    def update_group(self, group_id: str, request: RenameGroupRequest) -> Response[bool]:
        return send_request('PUT', f'/groups/{group_id}', request, self.config)

    # Subscribers Endpoints
    def list_subscribers(self, group_id: str, limit: int = 10, page: int = 1) -> Response[BaseResult[Subscriber]]:
        return send_request('GET', f'/groups/{group_id}/subscribers?limit={limit}&page={page}', config=self.config)

    def add_subscriber(self, group_id: str, request: CreateSubscriberRequest) -> Response[bool]:
        return send_request('POST', f'/groups/{group_id}/subscribers', request, self.config)

    def delete_subscriber(self, group_id: str, request: DeleteSubscriberRequest) -> Response[bool]:
        return send_request('DELETE', f'/groups/{group_id}/subscribers', request, self.config)

    def get_subscriber_by_email(self, group_id: str, email: str) -> Response[Subscriber]:
        return send_request('GET', f'/groups/{group_id}/subscribers/{email}', config=self.config)

    # Messages Endpoints
    def get_message_info(self, schedule_id: str, email: str) -> Response[GetMessageInfoResponse]:
        return send_request('GET', f'/messages/{schedule_id}/{email}', config=self.config)

    def cancel_scheduled_message(self, request: CancelScheduledMessageRequest) -> Response[bool]:
        return send_request('POST', '/messages/cancel-scheduled', request, self.config)

    def send_marketing(self, request: SendMarketingRequest) -> Response[Schedule]:
        return send_request('POST', '/messages/marketing', request, self.config)

    def send_message_by_template(self, request: SendMessageByTemplateRequest) -> Response[Schedule]:
        return send_request('POST', '/messages/marketing-by-template', request, self.config)

    def get_schedule_info(self, schedule_id: str) -> Response[GetScheduleInfoResponse]:
        return send_request('GET', f'/messages/schedule/{schedule_id}', config=self.config)

    def send_transactional(self, request: SendTransactionalRequest) -> Response[Schedule]:
        return send_request('POST', '/messages/transactional', request, self.config)

    def send_transactional_by_template(self, request: SendMessageByTemplateRequest) -> Response[Schedule]:
        return send_request('POST', '/messages/transactional-by-template', request, self.config)

    # Outbound IP Endpoints
    def create_ip_group(self, request: CreateIpGroupRequest) -> Response[IPGroup]:
        return send_request('POST', '/outbound/ip-group/create', request, self.config)

    def get_ip_group_info(self, name: str) -> Response[IPGroup]:
        return send_request('GET', f'/outbound/ip-group/info/{name}', config=self.config)

    def list_ip_groups(self) -> Response[List[IPGroup]]:
        return send_request('GET', '/outbound/ip-group/list', config=self.config)

    def cancel_warmup(self, request: CancelWarmUpRequest) -> Response[CancelWarmUpResponse]:
        return send_request('POST', '/outbound/ip/cancel-warmup', request, self.config)

    def get_ip_info(self, ip: str) -> Response[IpAddress]:
        return send_request('GET', f'/outbound/ip/info/{ip}', config=self.config)

    def list_ips(self) -> Response[List[IpAddress]]:
        return send_request('GET', '/outbound/ip/list', config=self.config)

    def set_ip_group(self, request: SetIpGroupRequest) -> Response[SetIpGroupResponse]:
        return send_request('POST', '/outbound/ip/set-ip-group', request, self.config)

    def start_warmup(self, request: StartWarmUpRequest) -> Response[StartWarmUpResponse]:
        return send_request('POST', '/outbound/ip/start-warmup', request, self.config)

