
from django import template
from geonode.base.models import Configuration

register = template.Library()

def _is_mobile_device(context):
    if context and 'request' in context:
        req = context['request']
        return req.user_agent.is_mobile
    return False

@register.simple_tag(takes_context=True)
def get_custom_base_right_topbar_menu(context):

    is_mobile = _is_mobile_device(context)

    if is_mobile:
        return []

    home = {
        "type": "link",
        "href": "/",
        "label": "Home"
    }

    user = context.get('request').user
    about = {}
    if user.is_authenticated and not Configuration.load().read_only:
        about = {
            "label": "Involved",
            "type": "dropdown",
            "items": [
                {
                    "type": "link",
                    "href": "/people/",
                    "label": "People"
                },
                {
                    "type": "link",
                    "href": "/groups/",
                    "label": "Groups"
                },
                {
                    "type": "link",
                    "href": "/groups/categories/",
                    "label": "Countries"
                }
            ]
        }
        about['items'].extend([
            {
                "type": "divider"
            },
            {
                "type": "link",
                "href": "/invitations/geonode-send-invite/",
                "label": "Invite users"
            },
            {
                "type": "link",
                "href": "/admin/people/profile/add/",
                "label": "Add user"
            } if user.is_superuser else None,
            {
                "type": "link",
                "href": "/groups/create/",
                "label": "Create group"
            }if user.is_superuser else None,
        ])
    return [home, about]
