{
    'name': "Dynamic snippets builder",
    'sequence': 2,
    'version': '18.0.0.0.0',
    'depends': ['website', 'base'],
    'author': "Facilitator",
    'category': 'Website',
    "license": "OPL-1",
    'description': """
    This module is used to facilitate the process of building dynamic snippets based on the data base models.
        """,
    'data': [
        "security/ir.model.access.csv",
        "views/dynamic_snippet_builder_view.xml",
        "views/res_config_settings_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'dynamic_snippets_builder/static/src/js/dynamic_snippet.js',
            'dynamic_snippets_builder/static/src/css/style.scss',
        ],
    },
    "installable": True,
    "auto_install": False,
    "images": ["images/module_icon.png"],
}
