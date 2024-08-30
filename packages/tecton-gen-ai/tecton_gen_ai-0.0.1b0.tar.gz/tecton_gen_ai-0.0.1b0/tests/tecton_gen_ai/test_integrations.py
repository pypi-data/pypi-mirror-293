import json

from pytest import fixture

from tecton_gen_ai import prompt, tool
from tecton_gen_ai.agent import AgentClient, AgentService
from tecton_gen_ai.testing.mocks import mock_batch_feature_view


@fixture
def model_kwargs():
    return {"seed": 0, "response_format": {"type": "json_object"}}


@fixture
def langchain_llm(model_kwargs):
    import langchain
    from langchain_openai import ChatOpenAI

    langchain.debug = True

    return ChatOpenAI(model="gpt-4o", model_kwargs=model_kwargs, temperature=0)


@fixture
def llamaindex_llm(model_kwargs):
    from llama_index.llms.openai import OpenAI

    return OpenAI(model="gpt-4o", additional_kwargs=model_kwargs, temperature=0)


@fixture
def mock_agent_service(tecton_unit_test):
    user_info = mock_batch_feature_view(
        "user_info",
        {"user_id": "user2", "name": "Jim"},
        ["user_id"],
        description="Getting user name",
    )

    @prompt()
    def sys_prompt():
        return (
            # "You are serving user whose user_id " + user_id + ". "
            "The result should be in json format, the key is always 'result'"
        )

    @tool
    def get_tecton_employee_count() -> int:
        """
        Returns the number of employees in Tecton
        """
        return 110

    @tool
    def get_tecton_female_employee_count() -> int:
        """
        Returns the number of female employees in Tecton
        """
        return 60

    return AgentService(
        name="test",
        tools=[
            get_tecton_employee_count,
            get_tecton_female_employee_count,
            user_info,
        ],
        prompts=[sys_prompt],
    )


def test_langchain_agent(mock_agent_service, langchain_llm):
    client = AgentClient.from_local(mock_agent_service)
    res = client.invoke_agent(
        langchain_llm,
        "how many employees in tecton that are not female",
        system_prompt="sys_prompt",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_agent(langchain_llm, system_prompt="sys_prompt")
    with client.set_context({"user_id": "user2"}):
        res = agent.invoke({"input": "what is my name"})["output"]
    assert json.loads(res)["result"] == "Jim"


def test_llamaindex_agent(mock_agent_service, llamaindex_llm):
    client = AgentClient.from_local(mock_agent_service)
    res = client.invoke_agent(
        llamaindex_llm,
        "how many employees in tecton that are not female",
        system_prompt="sys_prompt",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_agent(llamaindex_llm, system_prompt="sys_prompt")
    with client.set_context({"user_id": "user2"}):
        res = str(agent.chat("what is my name"))
    assert json.loads(res)["result"] == "Jim"
