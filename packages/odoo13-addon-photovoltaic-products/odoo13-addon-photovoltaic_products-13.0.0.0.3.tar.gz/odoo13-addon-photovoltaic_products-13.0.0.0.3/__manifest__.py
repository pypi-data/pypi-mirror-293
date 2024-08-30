{
    'name': 'Photovoltaic Products',
    'version': '13.0.0.0.3',
    'depends': ['product'],
    'author': 'Librecoop',
    'category': 'Sales',
    'description': 'Manage the creation of photovoltaic products',
    'installable': True,
    'auto_install': False,
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        "views/photovoltaic_inverter.xml",
        "views/photovoltaic_module.xml",
        "views/product_template.xml",
    ],
}
