# -*- coding: utf-8 -*-
def list_projects(config, options, http):
    projects_response = http.make_request("/projects", "GET")

    json_data = projects_response.json()

    x = http.make_request("/projects", "GET")
