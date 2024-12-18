"""
NOTE: No other views should be added to this file as the `FrontendView`
is the only view that does not belong to any app and serves as a fallback
view for unmatched URLs.

This view should be the last route to be matched in the URL configuration,
meaning it will catch all requests that do not match any other defined routes.
It is intended solely to serve the frontend React application.
"""

from django.views.generic import TemplateView


class FrontendView(TemplateView):
    """
    Renders the `index.html` template for the frontend application.

    This view serves the `index.html` file, which references static assets
    built by Vite during the build process. The template includes the necessary
    CSS and JavaScript files to initialize the React-based frontend.
    """
    template_name = 'index.html'
