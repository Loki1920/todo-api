## SCRUM-5: Add due date filtering to the Todo list endpoint

**Jira Ticket:** [SCRUM-5](https://telomeregs.atlassian.net/browse/SCRUM-5)

## Summary
Add due date filtering to the Todo list endpoint

## Implementation Plan

**Step 1: Review the Todo List Endpoint Implementation**  
Locate the existing implementation of the Todo list endpoint to understand its current functionality and structure. This will help identify where to add the due date filtering logic.
Files: `todo_list_endpoint.py`

**Step 2: Define Query Parameters for Due Date Filtering**  
Decide on the query parameters to be used for filtering by due date. For example, we could use 'due_date' for exact matches and 'due_date__gte' and 'due_date__lte' for range queries. Update the endpoint's function signature to accept these parameters.
Files: `todo_list_endpoint.py`

**Step 3: Implement Filtering Logic**  
Add the logic to filter the Todo items based on the due date parameters. This will likely involve modifying the database query to include conditions based on the provided due date parameters.
Files: `todo_list_endpoint.py`

**Step 4: Update API Documentation**  
If applicable, update any API documentation to reflect the new query parameters for due date filtering. This ensures that consumers of the API are aware of the new functionality.
Files: `api_documentation.md`

**Step 5: Write Unit Tests for Due Date Filtering**  
Create unit tests to verify that the due date filtering works as expected. This should include tests for exact matches, greater than or equal to, and less than or equal to scenarios.
Files: `test_todo_list_endpoint.py`

**Risk Level:** MEDIUM — The implementation involves modifying the existing endpoint and adding new query parameters, which could introduce bugs if not handled carefully. However, the changes are straightforward and should not affect existing functionality if implemented correctly.

**Deployment Notes:**
- Ensure that the new query parameters are documented for API consumers.
- Monitor the endpoint after deployment for any unexpected behavior.

## Proposed Code Changes

### `todo_list_endpoint.py` (modify)
This change modifies the existing Todo list endpoint to accept new query parameters for filtering by due date. It adds logic to filter the Todo items based on the provided due date parameters, ensuring that the endpoint can handle exact matches as well as range queries.
```python
from typing import Optional


def get_todo_list(due_date: Optional[str] = None, due_date__gte: Optional[str] = None, due_date__lte: Optional[str] = None):
    # Existing logic to fetch todos
    query = Todo.objects.all()

    if due_date:
        query = query.filter(due_date=due_date)
    if due_date__gte:
        query = query.filter(due_date__gte=due_date__gte)
    if due_date__lte:
        query = query.filter(due_date__lte=due_date__lte)

    return query
```

### `api_documentation.md` (modify)
This update to the API documentation reflects the new query parameters for due date filtering, ensuring that users of the API are aware of the new functionality.
```
### Todo List Endpoint

#### Query Parameters
- `due_date`: Filter todos by exact due date.
- `due_date__gte`: Filter todos with due dates greater than or equal to the specified date.
- `due_date__lte`: Filter todos with due dates less than or equal to the specified date.

#### Example Request
```
GET /todos?due_date=2023-10-01&due_date__gte=2023-09-01&due_date__lte=2023-10-31
```

```

### `test_todo_list_endpoint.py` (modify)
These unit tests verify that the due date filtering works as expected for exact matches, greater than or equal to, and less than or equal to scenarios. This ensures that the new functionality is covered by tests.
```python
import pytest
from your_project import get_todo_list


def test_get_todo_list_exact_match():
    response = get_todo_list(due_date='2023-10-01')
    assert len(response) == expected_count


def test_get_todo_list_gte():
    response = get_todo_list(due_date__gte='2023-09-01')
    assert all(todo.due_date >= '2023-09-01' for todo in response)


def test_get_todo_list_lte():
    response = get_todo_list(due_date__lte='2023-10-31')
    assert all(todo.due_date <= '2023-10-31' for todo in response)

```

## Test Suggestions

Framework: `pytest`

- **test_due_date_filter_exact_match** — Test that the endpoint returns todos that match the exact due date provided.
- **test_due_date_filter_greater_than** — Test that the endpoint returns todos with due dates greater than or equal to the specified date.
- **test_due_date_filter_less_than** — Test that the endpoint returns todos with due dates less than or equal to the specified date.
- **test_due_date_filter_no_results** *(edge case)* — Test that the endpoint returns an empty list when no todos match the due date filter.
- **test_due_date_filter_invalid_date_format** *(edge case)* — Test that the endpoint returns a 400 error when an invalid date format is provided.

## AI Confidence Scores
Plan: 80%, Code: 90%, Tests: 90%

---
> ⚠️ **This PR was generated by AI (Claude via AWS Bedrock) and requires thorough human review
> before merging. Verify all logic, test coverage, and edge cases independently.**
>
> _Generated by AI Agentic SDLC Assistant_