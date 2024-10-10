from odoo import api, fields, models, _


class DynamicSnippetsBuilder(models.Model):
    _name = "dynamic.snippet.builder"
    _description = "This model is used to get all the needed data from the user to create an automated process for building dynamic snippets."

    name = fields.Char("Name", required=True)
    model_id = fields.Many2one("ir.model", string="Model", ondelete="cascade", required=True)
    field_ids = fields.Many2many("ir.model.fields", string="Fields", domain="[('model_id','=',model_id)]",
                                 required=True)
    filter_id = fields.Many2one("ir.filters", string="Filter")
    theme = fields.Selection([('list', 'List'), ('card', 'Card')], default='card')

    # snippet_preview = fields.Html('Preview', default="<h3>Hello world</h3>")

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.create_view_snippet_template()
        res.create_view_inherit_snippet()
        return res

    '''
    These method enable us to create the snippet view
    '''

    def create_view_snippet_template(self):
        '''
        Generate unique template id (exp: contact_snippet_template_1 ...)
        '''
        template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self.id)])
        template_name = ' '.join(['Snippet builder ', self.name.lower(), str(self.id)])
        '''
        Create the snippet template representing the dynamic snippet builder in 'ir.ui.view'
        Define the arch_db
        '''
        arch = '''<t t-name="dynamic_snippets_builder.%s" name="%s">
                            <section class="pt40 pb40 %s">
                                <div class="container template %s">
                                    <h1 class="text-center" t-out='id'> Good job</h1>
                                </div>
                                <div class="dynamic_snippet_carousel"/>
                            </section>
                          </t>
                          ''' % (template_id, template_id, template_id, template_id)
        snippet_view = self.env['ir.ui.view'].create({
            'name': template_name,
            'key': 'dynamic_snippets_builder.' + template_id,
            'type': 'qweb',
            'arch_db': arch,
        })
        '''
        Add the created view to ir.model.data
        '''
        self.env['ir.model.data'].create({
            'name': template_id,
            'module': 'dynamic_snippets_builder',
            'res_id': snippet_view.id,
            'model': 'ir.ui.view',
            'noupdate': True,
        })

    '''
    These method enable us to inherit from /website/views/snippets/snippets.xml view
    '''

    def create_view_inherit_snippet(self):
        '''
        Generate a unique inherit name representing the name for ir.model.data
        '''
        inherit_name = '_'.join(self.name.lower().split(' ') + ['inherit_snippet', str(self.id)])
        name = 'Snippet builder ' + self.name.lower()
        template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self.id)])
        '''
        Create the inherited template representing the dynamic snippet builder in 'ir.ui.view'
        Define the arch_db
        '''
        arch = '''<data inherit_id="website.snippets" name="%s">
                        <xpath expr="//div[@id='snippet_effect']//t[@t-snippet][last()]" position="after">
                            <t t-snippet="dynamic_snippets_builder.%s" string="%s" t-thumbnail="/dynamic_snippets_builder/static/dynamic/icon.png"/>
                        </xpath>
                    </data>''' % (name, template_id, name)
        inherited_view_id = self.env['ir.model.data'].search([('name', '=', "snippets"), ('module', '=', "website")],
                                                             limit=1).res_id
        view_created = self.env['ir.ui.view'].create({
            'name': name,
            'key': 'dynamic_snippets_builder.' + inherit_name,
            'type': 'qweb',
            'inherit_id': inherited_view_id,
            'arch_db': arch,
        })
        '''
        Add the create view to "ir.model.data"
        '''
        self.env['ir.model.data'].create({
            'name': inherit_name,
            'module': 'dynamic_snippets_builder',
            'res_id': view_created.id,
            'model': 'ir.ui.view',
            'noupdate': True,
        })

    # def create_snippet_options(self):
    #     '''
    #             Generate a unique name representing the options name for the snippet ir.model.data
    #             '''
    #     option_name = '_'.join(self.name.lower().split(' ') + ['snippet_options', str(self.id)])
    #     # name = 'Snippet option ' + self.name.lower()
    #     template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self.id)])
    #     '''
    #     Create the option template representing the dynamic snippet builder options in 'ir.ui.view'
    #     Define the arch_db
    #     '''
    #     arch = '''<data inherit_id="website.snippet_options" name="%s">
    #                     <xpath expr="." position="inside">
    #                         <div data-js="Snippet" data-selector=".%s">
    #                             <we-select string="Card style" data-apply-to=".card">
    #                                 <we-button data-select-class="bg-dark text-white">Dark</we-button>
    #                                 <we-button data-select-class="">Light</we-button>
    #                             </we-select>
    #                         </div>
    #                     </xpath>
    #                 </data>''' % (option_name, template_id)
    #     inherited_view_id = self.env['ir.ui.view'].search([('key', '=', "website.snippet_options")],
    #                                                          limit=1).res_id
    #     view_created = self.env['ir.ui.view'].create({
    #         'name': option_name,
    #         'key': 'dynamic_snippets_builder.' + option_name,
    #         'type': 'qweb',
    #         'inherit_id': inherited_view_id,
    #         'arch_db': arch,
    #     })
    #     '''
    #     Add the create view to "ir.model.data"
    #     '''
    #     self.env['ir.model.data'].create({
    #         'name': option_name,
    #         'module': 'dynamic_snippets_builder',
    #         'res_id': view_created.id,
    #         'model': 'ir.ui.view',
    #         'noupdate': True,
    #     })

    '''
    Shortcut to create a filter if needed
    '''

    def action_view_filters(self):
        self.ensure_one()
        return {
            'name': _('Create filter'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'ir.filters',
            'view_id': self.env.ref('base.ir_filters_view_form').id,
            'context': {'default_model_id': self.model_id.model},
        }

    # @api.onchange("model_id")
    # def _on_change_preview(self):
    #     for record in self:
    #         record.snippet_preview = "<h3>Hello world</h3>"
