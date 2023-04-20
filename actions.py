class Actionlock(lock):
    def name(self):
        return "lock_execute_script"

    def run(self, dispatcher, tracker, domain):
        # Call the script and get the output
        siteId = tracker.get_slot("code_site")

        cmd = "cmedit set " + siteId + " EutranCellTDD administrativeState=block "
        cmd2 = ""+ siteId +"blocked"

        # Pass the output to the response
        dispatcher.utter_message(text=cmd2)
        return []