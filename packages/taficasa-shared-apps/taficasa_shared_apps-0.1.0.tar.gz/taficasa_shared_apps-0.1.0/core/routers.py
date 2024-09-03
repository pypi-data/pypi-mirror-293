from dataclasses import dataclass
from typing import Dict, List, Optional, OrderedDict, Tuple

from django.core.exceptions import ImproperlyConfigured
from django.urls import path, re_path
from rest_framework.routers import BaseRouter
from rest_framework.viewsets import GenericViewSet


@dataclass(frozen=True)
class CustomAPIRoute:
    # URL path string with zero-indexed format strings
    # e.g. {0} which will be swapped out for url_args
    url: str
    # Mapping of url arg name to optional django path converter
    # if path converter is not specified, the arg is defaulted to
    # the '[^/.]+' regex capturing group.
    url_args: OrderedDict[str, Optional[str]]
    # Unique name of URL. This is what you can pass into reverse
    # to get back the final URL string, like so
    # reverse("<app_label>:<url_name>")
    url_name: Dict[str, str]
    # List of methods that were implemented on the viewset
    methods: List[str]


class CustomAPIRouter(BaseRouter):
    # Default implementation, TODO check if I need to change
    def get_default_basename(self, viewset):
        return ""

    def _get_routes(self, viewset) -> List[CustomAPIRoute]:
        if not hasattr(viewset, "custom_api_routes"):
            raise ImproperlyConfigured(
                f"To use CustomAPIRouter, Viewset - {viewset.__name__} "
                "must set the custom_api_routes attribute"
            )

        # Validate that urls are set correctly in custom api routes
        # and do not have starting forward slashes
        for route in viewset.custom_api_routes:
            if route.url.startswith("/"):
                raise ImproperlyConfigured(
                    f"URL - {route.url} on CustomAPIRoute for Viewset - {viewset.__name__} "
                    "cannot start with a forward slash (/)"
                )
        return viewset.custom_api_routes

    def _get_route_action(self, action):
        """
        Returns a map between a http mthod and the
        corresponding viewset action(method)
        """
        if action == "list" or action == "retrieve":
            return {"get": action}
        elif action == "create" or action == "update":
            return {"post": action}
        elif action == "partial_update":
            return {"patch": action}
        elif action == "destroy":
            return {"delete": action}

        raise ImproperlyConfigured(
            f"Viewset method - {action} set in custom_api_routes not recognized!"
        )

    def _get_route_mapping(self, methods):
        mapping = dict()
        for method in methods:
            mapping.update(self._get_route_action(method))

        return mapping

    def _get_lookup_url(self, url: str, url_args: Dict[str, str]) -> Tuple[str, bool]:
        lookup_url = url
        used_regex = False
        used_converter = False

        for idx, (arg, converter) in enumerate(url_args.items()):
            if converter:
                if used_regex:
                    raise ImproperlyConfigured(
                        f"For URL {url}, You must use either path convereters or "
                        "the default regex exclusively"
                    )
                replacement = f"(<{converter}:{arg}>)"
                used_converter = True
            else:
                if used_converter:
                    raise ImproperlyConfigured(
                        f"For URL - {url}, You must use either path convereters or "
                        "the default regex exclusively"
                    )
                replacement = f"(?P<{arg}>[^/.]+)"
                used_regex = True

            replacement_string = f"{{{idx}}}"
            lookup_url = lookup_url.replace(replacement_string, replacement)

        return lookup_url, used_regex

    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        url_patterns = []
        for prefix, viewset, basename in self.registry:
            routes = self._get_routes(viewset)
            for route in routes:
                # Build the url pattern
                lookup_url, used_regex = self._get_lookup_url(route.url, route.url_args)
                if lookup_url:
                    final_url = "{prefix}/{lookup}/".format(
                        prefix=prefix,
                        lookup=lookup_url,
                    )
                else:
                    final_url = "{prefix}/".format(
                        prefix=prefix,
                    )

                # In the case no prefix is defined we need to make sure we don't have
                # a leading url
                final_url = final_url.lstrip("/")

                initkwargs = {
                    "basename": route.url_name,
                }
                view = viewset.as_view(
                    self._get_route_mapping(route.methods), **initkwargs
                )
                if used_regex:
                    regex_path = r"^{0}$".format(final_url)
                    url_patterns.append(re_path(regex_path, view, name=route.url_name))
                else:
                    url_patterns.append(path(final_url, view, name=route.url_name))

        return url_patterns

    def register_in_bulk(self, prefix: str, viewsets: List[GenericViewSet]):
        """
        Convenience method to register a lot of viewsets at once
        to one common prefix
        """

        for viewset in viewsets:
            self.register(prefix, viewset)
