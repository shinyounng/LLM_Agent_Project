from langchain_core.messages import HumanMessage #패키지: langchain_core, 모듈: messages, 클래스: HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv 

load_dotenv() #현재 디렉토리에서 해당 .env파일을 찾는 역할을 함 

def main(): 
    #클래스 호출
    model = ChatOpenAI(temperature = 0) 
    #클래스(ChatOpneAI)를 사용해 생성한 model이라는 객체 변수 내부에 temperature이라는 변수를 0으로 설정한 것 
    #이 과정이 필요한 이유: agent는 LLM없이는 생각을 못 함. 그러므로, LLM과 연결된 객체 하나 만드는 과정!
    #temperature = 0의 의미: 항상 최대한 똑같이, 논리적으로 (LLM의 랜덤성 조절기)
    #(우리는 openai의 LLM을 사용할 것) 

    tools = [] #빈 리스트 -> agent가 사용할 수 있는 도구들로 채울 예정 
    agent_excutor = create_react_agent(model, tools) #함수 
    #반환하는 객체: 에이전트 실행 객체(model과 tools를 이용하여 실행)

    print("Welcom! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True: 
        user_input = input("\nYou:").strip() #.strip()은 텍스트의 앞 뒤 공백을 없앰/ ex: " hello" -> "hello"

        if user_input == "quit":
            break

        #응답 시작
        print("\nAssistant: ", end= "") #end ="": 줄바꿈 방지
        #해석: 에이전트에게 질문 보내기
        for chunk in agent_excutor.stream( #객체.함수() //agent_executor라는 객체 안에 들어 있는 함수(stream)를 호출
            {"messages": [HumanMessage(content = user_input)]}
        ):  
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end= "")

        print()

if __name__ == "__main__": #이 파이썬 파일을 직접 실행할 경우에만 실행하고, 어디선가 import하는 경우에는 호출하지 않는다는 의미
    main()