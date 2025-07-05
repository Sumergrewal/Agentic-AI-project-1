from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent_workflow import GraphBuilder
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv

app=FastAPI()

class RequestQuery(BaseModel):
    query:str


@app.post("/query")
async def travel_agent(query:RequestQuery):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app=graph()
        #react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def main():
    print("Hello from ai-trip-planner!")


if __name__ == "__main__":
    main()