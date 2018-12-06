# -*- coding: utf-8 -*-
{
    'name': 'Office Custom theme EPS',
    'description': '',
    'summary': '',
    'category': 'Theme',
    'version': '1.0',
    'website': '',
    'author': 'Marwa BEN MESSAOUD I-WAY',
    'depends': ['website','website_sale','survey'],
    'data': [
        'views/slide_images.xml',
        #'views/website_image_carousel.xml',
        #'views/theme.xml',
        'views/res_config.xml',
        'views/layout.xml',
        'views/contact.xml',
        'views/homepage.xml',
        'views/references.xml',
        'views/mentions_legales.xml',
        'views/conditions.xml',
        'views/eps_definition.xml',
        'views/product_promo.xml',
        'views/newsletter_views.xml',
        'views/product_template_view.xml',
        'security/ir.model.access.csv',
    ],
    'images':[
            'static/description/splash_screen.png',
    ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
