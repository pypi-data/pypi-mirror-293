from fastapi import Request

async def custom_middleware(request: Request, call_next):
    """
    A middleware that is executed on every request.

    The middleware will print a message before and after the request is handled.
    """

    # Print a message before the request is handled
    print("Custom middleware before request")

    # Call the next middleware in the chain
    response = await call_next(request)

    # Print a message after the request is handled
    print("Custom middleware after request")

    # Return the response
    return response

