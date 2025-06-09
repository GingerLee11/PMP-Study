import genanki

MODEL_ID_BASIC = 1607392319
MODEL_ID_CLOZE = 1782910741

basic_model = genanki.Model(
    MODEL_ID_BASIC,
    'Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'UID'},
    ],
    templates=[
        {
            'name': 'Basic Card',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css="""
    .card {
      font-family: arial;
      font-size: 40px;
      text-align: center;
      color: black;
      background-color: white;
    }
    """
)

cloze_model = genanki.Model(
    MODEL_ID_CLOZE,
    'Cloze Model',
    fields=[
        {'name': 'Text'},
        {'name': 'BackExtra'},
        {'name': 'UID'},
    ],
    templates=[
        {
            'name': 'Cloze Card',
            'qfmt': '{{cloze:Text}}',
            'afmt': '{{cloze:Text}}<br>{{BackExtra}}',
        },
    ],
    css=basic_model.css,
    model_type=genanki.Model.CLOZE,
)
