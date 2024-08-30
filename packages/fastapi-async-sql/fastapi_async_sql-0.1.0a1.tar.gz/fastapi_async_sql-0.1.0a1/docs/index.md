# FastAPI Async SQL

Common utilities for Async SQL FastAPI applications.

## Installation
```bash
uv add fastapi-async-sql

pip install fastapi-async-sql
```

## Features
- AsyncSQLAlchemyMiddleware: A middleware to handle database connections with AsyncSQLAlchemy
- [SQLModel](https://sqlmodel.tiangolo.com/): A library to handle database models with Pydantic and SQLAlchemy
- Base models for `SQLModel`:
  - `BaseSQLModel`: A opinionated base model for SQLAlchemy models
  - `BaseTimestampModel`: A base model with timestamps for SQLAlchemy models
  - `BaseUUIDModel`: A base model with UUID for SQLAlchemy models
- `BaseRepository`: A base repository to handle CRUD operations with SQLAlchemy models
- Filtering, Sorting and Searching with [FastAPI Filter](https://fastapi-filter.netlify.app/): A library to handle filtering and sorting of data
- Pagination with [FastAPI Pagination](https://uriyyo-fastapi-pagination.netlify.app/): A library to handle pagination of data

