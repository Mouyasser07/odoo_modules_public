import time
import json
from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    """This class is used for getting values for dynamic product snippets
       """

    @http.route('/create_dynamic_snippet/<int:dynamic_snippet_builder_id>', type='json', auth='public')
    def create_dynamic_snippet(self, dynamic_snippet_builder_id=False):
        """Function for getting the data needed for the build of the snippet.
            Return
                  data of selected model found in dynamic_snippet
                  current_website-the current website for checking dynamic_snippet
            """
        current_website = request.env['website'].sudo().get_current_website().id
        data = []
        dynamic_snippet_id = request.env[
            'dynamic.snippet.builder'].sudo().browse(dynamic_snippet_builder_id)
        if not dynamic_snippet_id:
            return data
        fields = []
        if dynamic_snippet_id.field_ids:
            for field in dynamic_snippet_id.field_ids:
                fields.append(field.name)
        model = dynamic_snippet_id.model_id.model
        domain = dynamic_snippet_id.filter_id.domain if dynamic_snippet_id.filter_id.domain else []
        group_by = json.loads(dynamic_snippet_id.filter_id.context)["group_by"] if dynamic_snippet_id.filter_id else ['id']
        data = request.env[model].sudo().read_group(domain, fields=fields, groupby=group_by)
        print(data)
        return data, current_website
