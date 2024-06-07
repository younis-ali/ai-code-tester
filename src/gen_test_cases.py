from github import Github
import json
from openai import OpenAI
from github import Auth


class TestCaseGenerator:
    
    # constructor to read the configuration file 

    def __init__(self, configuration_file_path) -> None:
        with open(configuration_file_path) as f:
            self.config = json.load(f)
    
    # define function to get the test cases using predefined prompt

    def get_completion(self, code):
        client = OpenAI(api_key=self.config['openai_api_key'])
        model = "gpt-3.5-turbo"

        prompt = f"""
            You are an expert test case generator. Your task is to create thorough and effective test cases for the provided code. Follow these detailed steps to ensure comprehensive coverage for each function:

            1. **Identify all functions** in the provided code.

            2. For each function:
                * **Valid Inputs**: Consider various scenarios involving valid data types, formats, and ranges for the function's arguments.
                    * Provide specific examples of valid inputs and their corresponding expected results.
                * **Invalid Inputs**: Identify edge cases and unexpected data types the function might encounter.
                    * Describe how the function should handle these invalid inputs (e.g., raise exceptions, return error codes).
                * **Boundary Cases**: Test the function at the boundaries of input ranges to ensure robust handling.
                    * Specify the expected behavior at these boundaries.
                * **Error Handling**: Simulate potential errors during function execution (e.g., logical errors, boundary cases, network issues, database errors).
                    * Detail how the function should behave in these error scenarios.
                * **Return Values**: For functions that return data:
                    * Create test cases that cover various return values based on different input combinations.
                    * Include assertions to verify the correctness of the returned values.
                * **Performance Testing**: Evaluate how the function performs under heavy load or with large inputs.
                    * Specify acceptable performance criteria (e.g., execution time, memory usage).
                * **State-Based Testing**: For functions that depend on or modify internal state, create test cases that cover various state conditions.
                    * Ensure state transitions are valid and produce expected outcomes.
                * **Dependency Testing**: Identify any external dependencies (e.g., network, database, filesystem) and create test cases to simulate dependency failures.
                    * Ensure the function handles these failures gracefully.
                * **Security Testing**: Test for common security vulnerabilities (e.g., SQL injection, XSS, buffer overflow).
                    * Provide examples of inputs that test these vulnerabilities and specify expected behavior.
                * **Functional Requirements**: 
                    * Positive scenarios (valid inputs and expected outcomes)
                    * Negative scenarios (invalid inputs and appropriate error handling)
                    * Edge cases (boundary conditions and extreme values)
                    * Performance cases (speed and efficiency)
                    
            **Output Requirements**:
            For each function, generate test cases with:
                * A clear description of each test scenario.
                * Give the psedo code of each test case.
                * In the output provide only a list of test cases with the respective function.

            The code is given as follows:
            `{code}`
            """
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return completion.choices[0].message.content

    
    # function to generate the test cases
    def get_test_cases(self, repo_name):
        
        # authorize the github using PAT
        auth = Auth.Token(self.config['git_access_token'])

        # get user details
        g = Github(auth=auth)

        # get repo details
        repo = g.get_repo(repo_name)

        # View and get the last open pull request
        pulls = repo.get_pulls(state='open', sort='created')
        for pr in pulls:
            print(f"Number {pr.number}  Title {pr.title}")
        latest_pull_request = repo.get_pull(pr.number)

        # get the modfied files of the pull request
        files = latest_pull_request.get_files()

        # Define programming file extensions that will be considered in test cases generation
        programming_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.rb', '.go', '.php', '.ts', '.cs', '.html'}

        # Store the contents of each changed programming file in separate string variables
        file_contents = {}

        for file in files:
            file_path = file.filename
            # Check if the file has a programming extension
            if any(file_path.endswith(ext) for ext in programming_extensions):
                try:
                    file_content = repo.get_contents(file_path)
                    if file_content.type == 'file':
                        file_contents[file_path] = file_content.decoded_content.decode()
                except Exception as e:
                    print(f"Failed to fetch content for {file_path}: {e}")
                    file_contents[file_path] = None


        # Generate test cases for each programming file using ChatOpenAI
        test_cases = {}

        for filename, content in file_contents.items():
            if content:
                # print(content)
                test_cases[filename] = self.get_completion(content)

        for filename, cases in test_cases.items():
            print(f"Review of  {filename}:")
            print(cases)
            print("------------------------------------------------------------")

            # # commet to the pull request
            # latest_pull_request.create_issue_comment(f"Review of {filename}\n{cases}")

        return {"message" : f"test cases generated and commented on pull request {latest_pull_request}"}        
