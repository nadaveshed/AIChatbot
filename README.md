# Neural Search and Chatbot Service
This repository contains a service that integrates a simple neural search functionality and a chatbot capable of generating responses based on user queries.

### Setup
To set up the development environment, follow these steps:

1. Clone this repository:
```
git clone <repository_url>
cd neural-search-chatbot
```
2. Install dependencies. You will need Python 3.x and pip installed on your system. Install required Python packages using:
```
pip install -r requirements.txt
```
3. Pull the Qdrant Docker image:
```
docker pull qdrant/qdrant
```
4. Run the Qdrant Docker container:
```
docker run -p 6333:6333 qdrant/qdrant
```
### Usage
Follow the guide here to create the neural search service. You can query the service using the endpoint:

```
GET http://localhost:8000/api/search?q=<query>
```
For example:

```
GET http://localhost:8000/api/search?q=Are there startups about wine?
```
The chatbot provides information and answers questions using the neural search service and OpenAI's chat completion API. The service implements a single endpoint named query.

Send a POST request to the /query endpoint with the following payload:

```
{
    "user_id": "<unique_user_identifier>",
    "message": "<user_message>"
}
```
The response will be in JSON format with the following payload:

```
{
    "output": "<AI-generated_response>"
}
```

The service supports context. It considers the previous message to provide appropriate responses based on the conversation history.
Also the service handles situations where users send multiple messages in quick succession. It ensures that responses address the most recent query.

Error Handling
Proper error handling is implemented, and appropriate error responses are returned when necessary.

Security and Privacy
Sensitive information, such as API keys, are handled securely, and appropriate measures are taken to ensure data security and privacy.

Docker
Alternatively, you can also run the service using Docker. Use the provided Dockerfile to build the Docker image and run it on your local machine.
