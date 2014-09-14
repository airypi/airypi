import utils
import json
from remote_obj import send_to_device
import uuid

class UIElement(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
    
    def to_json(self):
        return {'id': self.id}
    
class Label(UIElement):
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        send_to_device('ui', {
            'element_id': self.id,
            'update': {'text': text}
        })
    
    def __init__(self, text):
        super(Label, self).__init__()
        self._text = text

    def to_json(self):
        json_dict = super(Label, self).to_json()
        json_dict['type'] = 'Label'
        json_dict['text'] = self.text
        return json_dict
    
class Button(Label):
    @property
    def disabled(self):
        return self._disabled
    
    @disabled.setter
    def disabled(self, disabled):
        self.disabled = disabled
        send_to_device('ui', {
            'element_id': self.id,
            'update': {'disabled': disabled}
        })
    
    def __init__(self, text = None, disabled = False):
        super(Button, self).__init__(text)
        self._disabled = disabled
        
    def to_json(self):
        json_dict = super(Button, self).to_json()
        json_dict['type'] = 'Button'
        json_dict['disabled'] = self.disabled
        return json_dict
    
class SwitchButton(Button):
    @property
    def activated(self):
        return self._activated
    
    @activated.setter
    def activated(self, activated):
        self._activated = activated
        send_to_device('ui', {
            'element_id': self.id,
            'update': {'activated': activated}
        })

    
    def __init__(self, text, disabled = False, activated = False):
        super(SwitchButton, self).__init__(text, disabled)
        self._activated = activated
        
    def to_json(self):
        json_dict = super(SwitchButton, self).to_json()
        json_dict['type'] = 'SwitchButton'
        json_dict['activated'] = self.activated
        return json_dict