# Module 13 Resources

## Core Documentation

### FastAPI
- **Official Documentation**: https://fastapi.tiangolo.com/
- **Tutorial - First Steps**: https://fastapi.tiangolo.com/tutorial/first-steps/
- **Request Body**: https://fastapi.tiangolo.com/tutorial/body/
- **Response Model**: https://fastapi.tiangolo.com/tutorial/response-model/
- **Dependencies**: https://fastapi.tiangolo.com/tutorial/dependencies/
- **Security**: https://fastapi.tiangolo.com/tutorial/security/
- **Async**: https://fastapi.tiangolo.com/async/
- **Performance**: https://fastapi.tiangolo.com/benchmarks/

### Pydantic
- **Official Documentation**: https://docs.pydantic.dev/
- **Models**: https://docs.pydantic.dev/latest/concepts/models/
- **Validators**: https://docs.pydantic.dev/latest/concepts/validators/
- **Field Constraints**: https://docs.pydantic.dev/latest/concepts/fields/
- **Error Handling**: https://docs.pydantic.dev/latest/errors/errors_ui/
- **Settings Management**: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

### Google OpenAI API
- **Official Documentation**: https://ai.google.dev/
- **Python SDK**: https://ai.google.dev/tutorials/python_quickstart
- **Generative AI**: https://ai.google.dev/gemini-api/docs
- **Streaming**: https://ai.google.dev/gemini-api/docs/streaming

## Tutorials and Guides

### FastAPI Tutorials
- **Full Stack FastAPI**: https://fastapi.tiangolo.com/tutorial/first-steps/
- **SQL Database**: https://fastapi.tiangolo.com/tutorial/sql-databases/
- **Background Tasks**: https://fastapi.tiangolo.com/tutorial/background-tasks/
- **Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **GraphQL**: https://fastapi.tiangolo.com/external-resources/#graphql

### Pydantic Guides
- **Data Validation**: https://docs.pydantic.dev/latest/concepts/dataclasses/
- **JSON Schema**: https://docs.pydantic.dev/latest/concepts/json_schema/
- **Environment Variables**: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

## Deployment and Production

### Docker
- **Docker Best Practices**: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- **Docker Compose**: https://docs.docker.com/compose/
- **FastAPI Docker**: https://fastapi.tiangolo.com/deployment/docker/

### Cloud Platforms
- **AWS Lambda**: https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
- **Google Cloud Run**: https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
- **Azure Functions**: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function-python
- **Heroku**: https://devcenter.heroku.com/articles/python-gunicorn

### Serverless Frameworks
- **Zappa**: https://zappa.readthedocs.io/
- **Mangum**: https://mangum.io/
- **AWS Chalice**: https://aws.github.io/chalice/

## Security and Authentication

### Authentication Methods
- **OAuth2 with FastAPI**: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- **JWT Authentication**: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- **API Keys**: https://fastapi.tiangolo.com/tutorial/security/first-steps/

### Security Best Practices
- **OWASP API Security**: https://owasp.org/www-project-api-security/
- **Rate Limiting**: https://cloud.google.com/architecture/rate-limiting-strategies-techniques
- **Input Validation**: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

## Performance and Monitoring

### Performance Optimization
- **Async Performance**: https://fastapi.tiangolo.com/async/
- **Connection Pooling**: https://www.psycopg.org/docs/usage/pool/
- **Caching Strategies**: https://docs.python.org/3/library/functools.html#functools.lru_cache

### Monitoring and Logging
- **Structured Logging**: https://docs.python.org/3/library/logging.html
- **Prometheus Metrics**: https://prometheus.io/docs/guides/python/
- **OpenTelemetry**: https://opentelemetry.io/docs/languages/python/

## Testing Resources

### Testing Frameworks
- **Pytest**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **HTTPX**: https://www.python-httpx.org/

### Load Testing
- **Locust**: https://locust.io/
- **Hey**: https://github.com/rakyll/hey
- **Apache Bench**: https://httpd.apache.org/docs/2.4/programs/ab.html

## Example Projects

### GitHub Repositories
- **FastAPI Official Examples**: https://github.com/tiangolo/fastapi/tree/master/docs_src
- **Pydantic Examples**: https://github.com/pydantic/pydantic/tree/main/tests
- **Gemini Python Samples**: https://github.com/google/generative-ai-python

### Tutorial Projects
- **ChatGPT Clone with FastAPI**: https://github.com/fastapi/full-stack-fastapi-template
- **AI Image Generator**: https://github.com/fastapi/fastapi/tree/master/docs_src
- **Real-time Streaming API**: https://github.com/fastapi/fastapi/tree/master/docs_src

## Community and Support

### Forums and Discussion
- **FastAPI Discord**: https://discord.gg/fastapi
- **Pydantic Discord**: https://discord.gg/pydantic
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/fastapi

### Blog Posts and Articles
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices
- **Production Deployment Guide**: https://testdriven.io/blog/fastapi-deployment/
- **Building REST APIs with FastAPI**: https://realpython.com/fastapi-python-web-apis/

## Books and Courses

### Books
- **FastAPI for Python Developers**: https://www.amazon.com/dp/B09X29RQ6S
- **Building APIs with FastAPI**: https://www.packtpub.com/product/building-apis-with-fastapi/9781837630042

### Online Courses
- **FastAPI Course - freeCodeCamp**: https://www.youtube.com/watch?v=0sOvCWFmrtA
- **Pydantic Course - Talk Python Training**: https://training.talkpython.fm/
- **Google OpenAI API Course**: https://ai.google.dev/courses

## Additional Tools

### API Development Tools
- **Postman**: https://www.postman.com/
- **Insomnia**: https://insomnia.rest/
- **Swagger Editor**: https://editor.swagger.io/

### Database Tools
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Alembic**: https://alembic.sqlalchemy.org/
- **Tortoise ORM**: https://tortoise.github.io/

### Message Queues
- **Celery**: https://docs.celeryproject.org/
- **Redis**: https://redis.io/documentation
- **RabbitMQ**: https://www.rabbitmq.com/tutorials

---

## Quick Reference

### FastAPI Commands
```bash
# Install FastAPI
pip install fastapi uvicorn

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with auto-reload
uvicorn main:app --reload

# Run production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Pydantic Commands
```bash
# Install Pydantic
pip install pydantic

# Install with all extras
pip install pydantic[email,datetime]
```

### Environment Variables
```bash
# Set API keys
export OPENAI_API_KEY="your-key"
export API_KEYS="key1,key2,key3"

# Load from .env file (using python-dotenv)
# Add to your code:
# from dotenv import load_dotenv
# load_dotenv()
```

---

## Next Steps

After completing Module 13, consider exploring:
- **Module 14**: Deploying AI Services
- **Module 15**: Monitoring and Observability
- **Module 16**: Security Best Practices
- **Module 17**: Scalability and Performance

---

*Last updated: June 2026*