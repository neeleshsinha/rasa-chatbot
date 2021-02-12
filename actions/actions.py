# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

details = {
    'MYPAINTS': '+91 9580293357',
    'NEELESH': '+91 8052127738'
}


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_your_num"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="Hello World!")
        print(tracker.get_slot('num'))
        # dispatcher.utter_template('utter_your_num', tracker, number=details[str(tracker.get_slot('NAME')).lower()])
        return []


class ActionFormInfo(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["NAME", "PAINT"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit", name=tracker.get_slot('NAME'),
                                 colour=tracker.get_slot('PAINT'))
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_entity(entity="NAME", intent='my_name_is'),
                     self.from_text()],
            "colour": [self.from_entity(entity="BRAND", intent="colour"),
                        self.from_text()],
        }

    @staticmethod
    def paint_db() -> List[Text]:
        """Database of paint"""

        return [
            "red",
            "green",
            "blue",
        ]

    def validate_paint(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate paint value."""
        print(value)
        if value.lower() in self.paint_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"PAINT": value}
        else:
            print(value)
            dispatcher.utter_message(template="utter_wrong_value")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"PAINT": None}