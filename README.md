# AI-Driven Test Case Generator

This project provides an AI-driven test case generator using FastAPI. The application accepts a GitHub repository name and generates test cases for the repository using openAI LLM.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [License](#license)

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-username/ai-driven-test-case-generator.git
    cd ai-driven-test-case-generator
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the FastAPI server**

    ```bash
    uvicorn main:app --reload
    ```

2. **Access the API documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation provided by Swagger UI.

## API Endpoints

### Root Endpoint

- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message.

**Response**

```json
{
  "message": "ai-driven test case generator"
}
```

### Generate Test Cases
- **Endpoint**: `/generate test cases`
- **Method**: `POST`
- **Description**: Generates test cases for the given GitHub repository.

**Request Body**

```josn
{
  "repo_name": "owner/repository_name"
}
```

**Response**

```josn
{
  "message": "Test cases generation response"
}
```
## Configuration
The application uses a configuration file `config.json` for initializing the TestCaseGenerator. Ensure that this file is correctly set up in the root directory of your project. The `config.json` file should contain necessary configuration settings required by TestCaseGenerator. The format of `config.json` is as follows:
```json 
{
    "git_access_token" : "your PAT of Github",
    "openai_api_key" : "open api key"
}
```
