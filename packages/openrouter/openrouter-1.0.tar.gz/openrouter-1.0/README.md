openrouter library
```bash
pip install openrouter
```

Use Library
```python
from openrouter.openrouter import Openrouter
from openrouter.openrouter import models
from openrouter.openrouter import roles
router = Openrouter(models.openai.gpt4o_mini,system_prompt="You are Persian Assistant")
```
get and save messages to json file
```python
#save to File
router.export_messages_to_file("msg.json",router.get_messages())

#append answer or question to messages
#as user
router.append_messages(roles.USER,"Questuin")
#as robot response
router.append_messages(roles.ASSISTANT,"Bot Response")

#get messages
print(router.get_messages())

#clear messages
router.clear_messages()

#set messages to session from file
router.set_messages(router.get_messages_from_file("msg.json"))
```