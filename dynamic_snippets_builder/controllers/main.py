from odoo import http
from odoo.http import request


def generate_dynamic_snippet_data(dynamic_snippet_id):
    fields = []
    relational_fields = []
    if dynamic_snippet_id.field_ids:
        for field in dynamic_snippet_id.field_ids:
            fields.append(field.name)
            if field.ttype == 'one2many' or field.ttype == 'many2many' or field.ttype == 'many2one':
                relational_fields.append([field.name, field.relation])
    model = dynamic_snippet_id.model_id.model
    domain = dynamic_snippet_id.filter_id.domain if dynamic_snippet_id.filter_id.domain else []
    domain_list = eval(str(domain))
    data = request.env[model].sudo().search_read(domain_list, fields)
    # Return the name or display_name instead of ids for relational fields
    if relational_fields:
        for d in data:
            for f in relational_fields:
                if d[f[0]]:
                    if type(d[f[0]]) != tuple:
                        names = request.env[f[1]].browse(d[f[0]]).mapped(
                            lambda x: x.name if 'name' in request.env[f[1]]._fields else x.display_name)
                    else:
                        names = d[f[0]][1]
                    d[f[0]] = names
    return data


class DynamicSnippets(http.Controller):
    """This class is used for getting values for dynamic snippets
       """

    @http.route('/create_dynamic_snippet/<int:dynamic_snippet_builder_id>', type='json', auth='public')
    def create_dynamic_snippet(self, dynamic_snippet_builder_id=False):
        """Function for getting the data needed for the build of the snippet.
            Return
                  data of selected model found in dynamic_snippet
            """
        dynamic_snippet_id = request.env[
            'dynamic.snippet.builder'].sudo().browse(dynamic_snippet_builder_id)
        if not dynamic_snippet_id:
            return []
        # If group_id is found return data only to users in this group otherwise the snippet is public
        if dynamic_snippet_id.group_id:
            if request.env.user.has_group(dynamic_snippet_id.group_id.get_metadata()[0].get('xmlid')):
                return generate_dynamic_snippet_data(dynamic_snippet_id)
            return []
        else:
            return generate_dynamic_snippet_data(dynamic_snippet_id)

