## SCRUM-3: Add rate limiting to the public API endpoints

**Jira Ticket:** [SCRUM-3](https://telomeregs.atlassian.net/browse/SCRUM-3)

## Summary
Add rate limiting to the public API endpoints

## Implementation Plan

**Step 1: Review and Update Dependencies**  
Check the requirements.txt file for the presence of Redis and any rate limiting libraries. If not present, add 'redis' and 'fastapi-limiter' to the dependencies.
Files: `requirements.txt`

**Step 2: Set Up Redis for Rate Limiting**  
Ensure that a Redis server is running and accessible from the application. Configure the connection settings in the application settings or environment variables.
Files: `config.py`

**Step 3: Implement Rate Limiting Middleware**  
Create a middleware component that utilizes 'fastapi-limiter' to enforce rate limits based on the specified criteria (60 requests/min for unauthenticated users, 600 requests/min for authenticated users). Exempt health check endpoints from rate limiting.
Files: `main.py`, `middleware.py`

**Step 4: Define Rate Limit Exceeded Responses**  
Implement logic to return appropriate HTTP responses and headers when the rate limit is exceeded. This should include a 429 status code and a message indicating the limit has been reached.
Files: `middleware.py`

**Step 5: Test Rate Limiting Functionality**  
Create unit tests to validate that the rate limiting works as expected for both authenticated and unauthenticated users. Ensure that health check endpoints are exempt from limits.
Files: `test_middleware.py`

**Step 6: Update Documentation**  
Update the API documentation to reflect the new rate limiting rules, including the limits for authenticated and unauthenticated users and the behavior when limits are exceeded.
Files: `docs/api_reference.md`

**Risk Level:** MEDIUM — The implementation of rate limiting involves changes to core API functionality and introduces external dependencies (Redis). There is a risk of misconfiguration or performance issues if not properly tested.

**Deployment Notes:**
- Ensure Redis is deployed and accessible in the production environment.
- Monitor API performance post-deployment to identify any potential bottlenecks.

## Proposed Code Changes

### `requirements.txt` (modify)
Adding Redis and fastapi-limiter to the requirements to support rate limiting functionality.
```
redis
fastapi-limiter

```

### `config.py` (modify)
Adding a configuration for Redis connection to allow the application to connect to the Redis server for rate limiting.
```python
import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

```

### `middleware.py` (create)
Creating middleware to implement rate limiting using fastapi-limiter, with exemptions for health check endpoints.
```python
from fastapi import Request, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

async def init_rate_limiter() -> None:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    await FastAPILimiter.init(redis_url)

async def rate_limit(request: Request):
    if request.url.path.startswith('/health'):  # exempt health check
        return
    user = request.user  # Assuming user is set in request
    if user.is_authenticated:
        await RateLimiter(limit=600, period=60)(request)
    else:
        await RateLimiter(limit=60, period=60)(request)

```

### `middleware.py` (modify)
Adding a function to handle rate limit exceeded responses, returning a 429 status code and a message.
```python
async def rate_limit_exceeded():
    raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

```

### `test_middleware.py` (create)
Creating unit tests to validate the rate limiting functionality for both authenticated and unauthenticated users.
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("authenticated, expected_status", [
    (False, 200),  # Unauthenticated user
    (True, 200),   # Authenticated user
])
def test_rate_limiting(authenticated, expected_status):
    # Simulate user authentication if needed
    for _ in range(60):  # Send requests to hit the limit
        response = client.get("/some_endpoint", headers={"Authorization": "Bearer token" if authenticated else ""})
        assert response.status_code == expected_status

    # Check for rate limit exceeded
    response = client.get("/some_endpoint", headers={"Authorization": "Bearer token" if authenticated else ""})
    assert response.status_code == 429

```

### `docs/api_reference.md` (modify)
Updating API documentation to reflect the new rate limiting rules and behavior when limits are exceeded.
```
## Rate Limiting

- Unauthenticated users: 60 requests per minute
- Authenticated users: 600 requests per minute
- Health check endpoints are exempt from rate limiting.
- If the rate limit is exceeded, a 429 status code will be returned with a message indicating the limit has been reached.

```

**New Dependencies:**
- `redis`
- `fastapi-limiter`

## Test Suggestions

Framework: `pytest`

- **test_rate_limiting_happy_path** — Test that a request within the limit returns a 200 status code.
- **test_rate_limiting_exceeded** — Test that exceeding the rate limit returns a 429 status code.
- **test_health_check_exemption** — Test that health check endpoint is exempt from rate limiting.
- **test_rate_limiting_with_authenticated_user** — Test that authenticated users have their own rate limit.
- **test_rate_limiting_boundary_conditions** *(edge case)* — Test that exactly hitting the rate limit returns a 200 status code, while exceeding it returns a 429 status code.

## Confluence Documentation References

- [Architecture Overview](https://telomeregs.atlassian.net/wiki/spaces/TODOAPI/pages/9699329) — Provides an overview of the API architecture, which is essential for understanding where to implement rate limiting.
- [API Design](https://telomeregs.atlassian.net/wiki/spaces/TODOAPI/pages/9764865) — Details the public API endpoints that will be affected by the rate limiting, including authentication requirements.
- [Coding Standards](https://telomeregs.atlassian.net/wiki/spaces/TODOAPI/pages/9830401) — Outlines coding standards that should be adhered to when implementing the rate limiting feature.
- [SCRUM-3: Add rate limiting to the public API endpoints](https://telomeregs.atlassian.net/wiki/spaces/TODOAPI/pages/11108353) — Directly addresses the requirements and specifications for implementing rate limiting, including functional requirements and acceptance criteria.

**Suggested Documentation Updates:**

- Architecture Overview: Update to include details about the new rate limiting feature and its impact on the API architecture.
- API Design: Revise to reflect the new rate limits for public API endpoints and any changes to the authentication requirements or error handling.
- SCRUM-3: Add rate limiting to the public API endpoints: Update with implementation details and any changes made during the development process.

## AI Confidence Scores
Plan: 85%, Code: 90%, Tests: 90%

---
> ⚠️ **This PR was generated by AI (Claude via AWS Bedrock) and requires thorough human review
> before merging. Verify all logic, test coverage, and edge cases independently.**
>
> _Generated by AI Agentic SDLC Assistant_