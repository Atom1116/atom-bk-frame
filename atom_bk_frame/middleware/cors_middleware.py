from typing import Dict, Tuple
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.response import Response
from atom_bk_frame.core.middleware import Middleware
from atom_bk_frame.util.settings_util import get_member_by_settings


class CorsMiddleware(Middleware):

    def request_process(self,
                        response: Response,
                        request: Request,
                        **kwargs) -> Tuple[bool, Response, Request, Dict]:

        if request.method == "OPTIONS":
            access_control_allo_origins = get_member_by_settings("ACCESS_ALLOW_ORIGIN")

            response_option = Response(headers={
                "Access-Control-Allow-Origin": ",".join(access_control_allo_origins),
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "Access-Control-Allow-Origin, X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
            })
            return False, response_option, request, kwargs

        return True, response, request, kwargs

    def response_process(self,
                         response: Response) -> Tuple[bool, Response]:
        access_control_allo_origins = get_member_by_settings("ACCESS_ALLOW_ORIGIN")
        response.add_headers(
            {
                "Access-Control-Allow-Origin": ",".join(access_control_allo_origins),
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "Access-Control-Allow-Origin, X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
            }
        )
        return True, response
