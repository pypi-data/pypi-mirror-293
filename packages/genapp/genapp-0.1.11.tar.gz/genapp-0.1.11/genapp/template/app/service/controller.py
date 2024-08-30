from fastapi import HTTPException


class Controller:

    ##########################################
    ############### Client Error #############
    ##########################################
    def return_block_connection(self):
        raise HTTPException(
            status_code=401,
            detail="Request audited and will be reported",
        )

    def return_not_autenticated(self):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # def return_not_autenticated(self):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Token invalid",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    def return_not_authorization(self):
        raise HTTPException(
            status_code=403,
            detail="Not permission to access on this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_expired_token(self):
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_session_expired(self):
        raise HTTPException(
            status_code=401,
            detail="Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_error(self):
        raise HTTPException(
            status_code=404,
            detail="Unknown request",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def response_error(self, description=None):
        if not description:
            raise HTTPException(
                status_code=400,
                detail=f"Bad request",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"{description}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    ##########################################
    ############## Server Error ##############
    ##########################################
    def return_server_error(self):
        raise HTTPException(
            status_code=500,
            detail="Internal server Error",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_not_implemented(self):
        raise HTTPException(
            status_code=501,
            detail="Not Implemented",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_bad_gateway(self):
        raise HTTPException(
            status_code=502,
            detail="Bad gateway",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_not_available(self):
        raise HTTPException(
            status_code=503,
            detail="Resource not available",
            headers={"WWW-Authenticate": "Bearer"},
        )

    ##########################################
    ############# Success Request ############
    ##########################################
    def response_ok(self):
        raise HTTPException(
            status_code=200,
            detail="Request completed succesfully",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def return_response(self, status_code, content, headers):
        raise HTTPException(
            status_code=status_code,
            detail=content,
            headers=headers,
        )
