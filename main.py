from fastapi import FastAPI
from src.gen_test_cases import TestCaseGenerator
from pydantic import BaseModel

class GitRepo(BaseModel):
    repo_name: str


app = FastAPI()

GenTestCases = TestCaseGenerator(configuration_file_path="config.json")

# define the root
@app.get("/")
def read_root():
    return {"message" : "ai-driven test case generator"}

@app.post("/generate test cases")
async def generate_test_cases(repository: GitRepo):
    repo_name = repository.repo_name

    resp = GenTestCases.get_test_cases(repo_name=repo_name)
    return {"message" : resp}

