{
    "name":"Auction",
    "author":" ",
    "license":"LGPL-3",
    "version":"18.0.1.0",
    "sequence":"3",
    'depends': ['web','base'],
    "data":[
        "security/ir.model.access.csv",
        "data/cron.xml",
        "views/asset_category.xml",
        "views/new_property.xml",
        "views/new_auction.xml",
        "views/bid_logs.xml",
        "views/bid_rules_view.xml",
        "views/auction_user_views.xml",
        "views/template/home.xml",
        "views/template/user_registration.xml",
        "views/template/login.xml",
        "views/template/properties.xml",
        "views/template/auction.xml",
        "views/menu.xml",
    ],

    'assets': {
            'web.assets_frontend': [
                'web.ajax',
                'auction_management/static/src/css/home.css',
                'auction_management/static/src/css/user.css',
                # 'auction_management/static/src/js/countdown.js', 
                'auction_management/static/src/css/auction.css',
                'auction_management/static/src/css/main.css',
                'auction_management/static/src/css/animation.css',
            ],
            'web.assets_backend': [
                'web.ajax',
                # '/auction_management/static/src/js/auction.js',
        ],
        },

    "installable":True,
    "application":True,
    "auto_install":False,
}