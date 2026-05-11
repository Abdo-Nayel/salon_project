"""
Salon Middleware
"""


class BranchMiddleware:
    """Middleware to handle branch-based access control"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Add branch info to request
            request.user_branch = request.user.branch
            request.is_admin = request.user.is_admin

        response = self.get_response(request)
        return response
