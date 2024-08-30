from silverriver.client.http_client import HTTPCruxClient
from silverriver.interfaces import SubTransition, AgentAction
from silverriver.interfaces.chat import AgentChatInterface
from silverriver.interfaces.data_models import BrowserObservation, Observation
from silverriver.utils.execution import execute_python_code


class BrowserSession:
    def __init__(self, client: HTTPCruxClient, chat_module: AgentChatInterface):
        self._client = client
        self.remote_page = None
        self.chat_module = chat_module

    def reset(self, start_url: str) -> SubTransition:
        setup = self._client.env_setup(start_url=start_url)
        self.remote_page = setup.exec_context["page"]
        response = self._client.env_get_observation()
        return response

    def execute(self, code: str) -> BrowserObservation:
        execute_python_code(
            code, execution_context={
                "page": self.remote_page,
                "chat": self.chat_module,
            })

        action = AgentAction(code=code)
        self._client.post_action(action)
        ret = self._client.env_get_observation()
        return BrowserObservation(**dict(ret.obs))


class Crux:
    def __init__(self, api_key: str):
        self.client = HTTPCruxClient(api_key=api_key)

    def create_browser_session(self, start_url: str, chat) -> tuple[BrowserSession, BrowserObservation, dict]:
        session = BrowserSession(client=self.client, chat_module=chat)
        transition = session.reset(start_url=start_url)
        return session, BrowserObservation(**transition.obs), transition.info

    def get_action(self, obs: Observation) -> str:
        obs.chat_messages = [dict(m) for m in obs.chat_messages]
        action = self.client.agent_get_action(obs)
        return action.code
