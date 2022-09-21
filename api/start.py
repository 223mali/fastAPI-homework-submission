import uvicorn


async def app(scope, receive, send):
    ...

if __name__ == "__main__":
    uvicorn.run("sql_app.main:app", host="0.0.0.0",
                port=8080, log_level="info", reload=True)
