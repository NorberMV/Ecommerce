

from django import forms


# Fixed choice fields

MOTOR_HP = (
    (' ', 'Select'),
    ('1.0', '1.0'),
    ('2.0', '2.0'),
    ('3.0', '3.0'),
    ('5.0', '5.0'),
    ('10.0', '10.0'),
)

MOTOR_SPEED = (
    (' ', 'Select'),
    ('1200', '1200'),
    ('1800', '1800'),
    ('3600', '3600'),
    
)

PHASES = (
    (' ', 'Select'),
    ('1', 'Single Phase'),
    ('3', 'Three Phase'),
)

PURPOSE = (
    (' ', 'Select'),
    ('General Purpose', 'General Purpose'),
    ('Pump', 'Pump'),
    ('Fan', 'Fan')
)


class MotorFilterForm(forms.Form):

    power = forms.ChoiceField(choices=MOTOR_HP, required=True,
        label='Power [HP]')
    
    speed = forms.ChoiceField(choices=MOTOR_SPEED, required=True, 
        label="Speed [RPM]")
    
    phases = forms.ChoiceField(choices=PHASES, required=True,
        label="Phases")
    
    purpose = forms.ChoiceField(choices=PURPOSE, required=True, 
        label="Purpose")
    
