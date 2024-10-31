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
    group_id = fields.Many2one("res.groups", string="Access group")

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.create_view_snippet_template()
        res.create_view_inherit_snippet()
        return res


    def unlink(self):
        self.unlink_view_snippet_template()
        self.unlink_view_inherit_snippet()
        return super().unlink()


    '''
    These method enable us to create the snippet view
    '''
    def create_view_snippet_template(self):
        # Generate unique template id (exp: contact_snippet_template_1 ...)
        template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self.id)])
        template_name = ' '.join(['Snippet builder ', self.name.lower(), str(self.id)])
        # Create the snippet template representing the dynamic snippet builder in 'ir.ui.view'
        # Define the arch_db
        if self.theme == 'card':
            arch = '''<t t-name="dynamic_snippets_builder.%s" name="%s">
                                <section class="pt40 pb40 %s">
                                    <div class="container template %s">
                                        <h1 class="text-center" t-out='id'> %s </h1>
                                    </div>
                                    <div class="dynamic_snippet_card"/>
                                </section>
                              </t>''' % (template_id, template_id, template_id, template_id, self.model_id.name)
        else :
            arch = '''<t t-name="dynamic_snippets_builder.%s" name="%s">
                                <section class="pt40 pb40 %s">
                                    <div class="container template %s">
                                        <h1 class="text-center" t-out='id'> %s </h1>
                                    </div>
                                    <div class="dynamic_snippet_table"/>
                                </section>
                              </t>''' % (template_id, template_id, template_id, template_id, self.model_id.name)
        # snippet_view_id = self.env['ir.ui.view'].search([('key','=','dynamic_snippets_builder.' + template_id)])
        snippet_view = self.env['ir.ui.view'].create({
            'name': template_name,
            'key': 'dynamic_snippets_builder.' + template_id,
            'type': 'qweb',
            'arch_db': arch,
        })
        # Add the created view to ir.model.data
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
        # Generate a unique inherit name representing the name for ir.model.data
        inherit_name = '_'.join(self.name.lower().split(' ') + ['inherit_snippet', str(self.id)])
        name = 'Snippet builder ' + self.name.lower()
        template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self.id)])
        # Create the inherited template representing the dynamic snippet builder in 'ir.ui.view'
        # Define the arch_db
        arch = '''<data id="dynamic_snippets_builder.%s" inherit_id="website.snippets" name="%s">
                            <xpath expr="//snippets[@id='snippet_groups']//t[@t-snippet][last()]" position="after">
                                 <t t-snippet="dynamic_snippets_builder.%s" t-if="request.env.user.has_group('%s')" string="%s" t-thumbnail="/dynamic_snippets_builder/static/dynamic/icon.png"/>
                            </xpath>
                 </data>''' % (inherit_name, name, template_id, self.group_id.id, name)
        inherited_view_id = self.env['ir.model.data'].search([('name', '=', "snippets"), ('module', '=', "website")],
                                                             limit=1).res_id
        view_created = self.env['ir.ui.view'].create({
            'name': name,
            'key': 'dynamic_snippets_builder.' + inherit_name,
            'type': 'qweb',
            'inherit_id': inherited_view_id,
            'arch_db': arch,
        })
        # Add the created view to "ir.model.data"
        self.env['ir.model.data'].create({
            'name': inherit_name,
            'module': 'dynamic_snippets_builder',
            'res_id': view_created.id,
            'model': 'ir.ui.view',
            'noupdate': True,
        })


    '''
    These method enable us to modify the snippet view
    '''
    @api.onchange('name')
    def on_change_view_snippet_template(self):
        print(self._origin.name)
        if self.name and self._origin.name:
            origin_template_id = '_'.join(self._origin.name.lower().split(' ') + ['snippet_template', str(self._origin.id)])
            template_id = '_'.join(self.name.lower().split(' ') + ['snippet_template', str(self._origin.id)])
            # origin_template_name = ' '.join(['Snippet builder ', self._origin.name.lower(), str(self._origin.id)])
            template_name = ' '.join(['Snippet builder ', self.name.lower(), str(self._origin.id)])
            origin_inherit_name = '_'.join(self._origin.name.lower().split(' ') + ['inherit_snippet', str(self._origin.id)])
            inherit_name = '_'.join(self.name.lower().split(' ') + ['inherit_snippet', str(self._origin.id)])
            # origin_name = 'Snippet builder ' + self._origin.name.lower()
            name = 'Snippet builder ' + self.name.lower()
            if self.theme == 'card':
                arch = '''<t t-name="dynamic_snippets_builder.%s" name="%s">
                                    <section class="pt40 pb40 %s">
                                        <div class="container template %s">
                                            <h1 class="text-center" t-out='id'> %s </h1>
                                        </div>
                                        <div class="dynamic_snippet_card"/>
                                    </section>
                                  </t>''' % (template_id, template_id, template_id, template_id, self.model_id.name)
            else :
                arch = '''<t t-name="dynamic_snippets_builder.%s" name="%s">
                                    <section class="pt40 pb40 %s">
                                        <div class="container template %s">
                                            <h1 class="text-center" t-out='id'> %s </h1>
                                        </div>
                                        <div class="dynamic_snippet_table"/>
                                    </section>
                                  </t>''' % (template_id, template_id, template_id, template_id, self.model_id.name)
            snippet_view_created_id = self.env['ir.ui.view'].search([('key', '=', 'dynamic_snippets_builder.' + origin_template_id)])
            if snippet_view_created_id:
                snippet_view_created_id.write({
                    'name': template_name,
                    'key': 'dynamic_snippets_builder.' + template_id,
                    'type': 'qweb',
                    'arch_db': arch,
                })
                model_snippet_created_id = self.env['ir.model.data'].search([('name','=',origin_template_id)])
                if model_snippet_created_id:
                    model_snippet_created_id.write({
                        'name': template_id,
                        'module': 'dynamic_snippets_builder',
                        'res_id': snippet_view_created_id.id,
                        'model': 'ir.ui.view',
                        'noupdate': True,
                    })
            arch_inherit = '''<data id="dynamic_snippets_builder.%s" inherit_id="website.snippets" name="%s">
                                                    <xpath expr="//snippets[@id='snippet_groups']//t[@t-snippet][last()]" position="after">
                                                         <t t-snippet="dynamic_snippets_builder.%s" t-if="request.env.user.has_group('%s')" string="%s" t-thumbnail="/dynamic_snippets_builder/static/dynamic/icon.png"/>
                                                    </xpath>
                                         </data>''' % (inherit_name, name, template_id, self.group_id.id, name)

            inherited_view_id = self.env['ir.model.data'].search(
                [('name', '=', "snippets"), ('module', '=', "website")],
                limit=1).res_id
            inherit_view_created_id = self.env['ir.ui.view'].search([('key','=','dynamic_snippets_builder.' + origin_inherit_name)])
            if inherit_view_created_id:
                inherit_view_created_id.write({
                    'name': name,
                    'key': 'dynamic_snippets_builder.' + inherit_name,
                    'type': 'qweb',
                    'inherit_id': inherited_view_id,
                    'arch_db': arch_inherit,
                })
                model_inherit_created_id = self.env['ir.model.data'].search([('name','=',origin_inherit_name)])
                if model_inherit_created_id:
                    model_inherit_created_id.write({
                        'name': inherit_name,
                        'module': 'dynamic_snippets_builder',
                        'res_id': inherit_view_created_id.id,
                        'model': 'ir.ui.view',
                        'noupdate': True,
                    })


    def unlink_view_snippet_template(self):
            for record in self:
                template_id = '_'.join(record.name.lower().split(' ') + ['snippet_template', str(record.id)])
                view_snippet_template_id = self.env['ir.ui.view'].search([('key','ilike',template_id)], limit=1)
                view_ir_model = self.env['ir.model.data'].search([('res_id','=',view_snippet_template_id.id)])
                view_ir_model.unlink()
                view_snippet_template_id.unlink()


    def unlink_view_inherit_snippet(self):
            for record in self:
                inherit_name = '_'.join(record.name.lower().split(' ') + ['inherit_snippet', str(record.id)])
                view_snippet_inherit_id = self.env['ir.ui.view'].search([('key', 'ilike', inherit_name)], limit=1)
                view_ir_model = self.env['ir.model.data'].search([('res_id', '=', view_snippet_inherit_id.id)])
                view_ir_model.unlink()
                view_snippet_inherit_id.unlink()

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

    '''
    Shortcut to create a group if needed
    '''
    def action_view_groups(self):
        self.ensure_one()
        return {
            'name': _('Create group'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'res.groups',
            'view_id': self.env.ref('base.view_groups_form').id,
        }
