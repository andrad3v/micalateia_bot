


def create_manga_embed_message(
    content, title, description, color, field_name, field_value, 
    field_inline, author_name, author_url, author_icon_url, url, 
    image_url, thumbnail_url, footer_text, footer_icon_url, 
    timestamp, components, components_id, components_type, 
    components_components, components_style, components_label, 
    components_action_set_id, components_emoji_name, components_emoji_animated, 
    components_url, components_disabled, actions, actions_id, actions_actions, 
    actions_options, actions_options_id, actions_options_label, actions_options_action_set_id, 
    actions_options_description, actions_placeholder, username, avatar_url):

    embed_json = {
        "content": "Contteúdo da mensagem ",
        "tts": false,
        "embeds": [
            {
            "id": 652627557,
            "title": "Títutlo",
            "description": "Descrição\n**negrito**\n*itálico*\n__underline__\n~~riscado~~\nChannel\n<#1320097246116712469>\nCargo\n<@&1320064447083188235>\nUser\n<@202021316058939392>",
            "color": 2326507,
            "fields": [
                {
                "id": 347148938,
                "name": "Nome field 1",
                "value": "Valor do field 1",
                "inline": true
                }
            ],
            "author": {
                "name": "autor",
                "url": "https://google.com",
                "icon_url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg"
            },
            "url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg",
            "image": {
                "url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg"
            },
            "thumbnail": {
                "url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg"
            },
            "footer": {
                "text": "rodoapé",
                "icon_url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg"
            },
            "timestamp": "2024-12-21T04:00:00.000Z"
            }
        ],
        "components": [
            {
            "id": 125498228,
            "type": 1,
            "components": [
                {
                "id": 1844209,
                "type": 2,
                "style": 4,
                "label": "Button RED",
                "action_set_id": "304093956",
                "emoji": {
                    "name": "🐵",
                    "animated": false
                }
                },
                {
                "id": 17046084,
                "type": 2,
                "style": 5,
                "label": "LINKZAO",
                "action_set_id": "219740865",
                "url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg",
                "emoji": {
                    "name": "🦧",
                    "animated": false
                },
                "disabled": false
                },
                {
                "id": 451368263,
                "type": 2,
                "style": 2,
                "label": "grey",
                "action_set_id": "778405318"
                }
            ]
            },
            {
            "id": 371308439,
            "type": 1,
            "components": [
                {
                "id": 514713599,
                "type": 3,
                "options": [
                    {
                    "id": 132333789,
                    "label": "opt-1",
                    "action_set_id": "719656967",
                    "description": "Ler cap 1"
                    }
                ],
                "placeholder": "Escolha um capítulo:"
                }
            ]
            }
        ],
        "actions": {
            "219740865": {
            "actions": []
            },
            "304093956": {
            "actions": []
            },
            "719656967": {
            "actions": []
            },
            "778405318": {
            "actions": []
            }
        },
        "username": "Micalateia",
        "avatar_url": "https://i.pinimg.com/736x/89/bb/3d/89bb3d19bed26516f6d5e47b25d73ac4.jpg"
        }