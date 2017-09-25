"""Navigation library defining different navigation function"""
import time



class Navigate(object):
    """navigate wrapper class APIs"""

    def __init__(self):
        """Constructor"""
        pass

    def to_help(self, client, obj, os_obj="aObject"):
        """API to navigate to 'help' menu"""
        if os_obj == "aObject":
            obj.click(client, "NATIVE", "xpath=//*[@id='ic_menu']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE",
                      "xpath=(//*[@id='left_drawer']/*/*[@id='lblListHeaderSlideView'])[6]", 0, 1)
        else:
            # "ios code will come here"
            obj.click(client)
            time.sleep(2)
            obj.click(client)

    def to_my_reminder(self, client, obj, os_obj="aObject"):
        """API to navigate to 'My Reminder' menu"""
        print "Entering toMyReminder:"
        if os_obj == "aObject":
            obj.click(client, "NATIVE", "xpath=//*[@id='ic_menu']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", "xpath=//*[@text='My Reminders']", 0, 1)
        else:
            # "ios code will come here"
            print "iOS: "
            obj.click(client, "NATIVE",
                      "xpath=//*[@accessibilityIdentifier='Menu-icn_1x.png']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", "xpath=//*[@class='YGLinedView' and "
                                        "./following-sibling::*[@accessibilityLabel='My "
                                        "Reminders']]", 0, 1)

    def to_my_profile(self, client, obj, os_obj="aObject"):
        """API to navigate to 'My Profile' menu"""
        if os_obj == "aObject":
            obj.click(client, "NATIVE", "xpath=//*[@id='ic_menu']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE",
                      "xpath=//*[@text='My Profile' and @id='lblListHeaderSlideView']", 0, 1)
        else:
            # "ios code will come here"
            obj.click(client)
            time.sleep(2)
            obj.click(client)

    def to_smart_testing(self, client, obj, os_obj="aObject"):
        """API to navigate to 'Smart Testing' menu"""
        if os_obj == "aObject":
            obj.click(client, "NATIVE", "xpath=//*[@id='ic_menu']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", "xpath=//*[@text='Smart Testing']", 0, 1)
        else:
            # "ios code will come here"
            time.sleep(2)
            obj.click(client, "NATIVE",
                      """xpath=//*[@class='UIImageView' and @height>0
                      and ./parent::*[@accessibilityLabel='Menu icn 1x']]""",
                      0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", """xpath=//*[@class='YGLinedView'
            and ./following-sibling::*[@accessibilityLabel='Smart Testing']]""", 0, 1)

    def to_settings(self, client, obj, os_obj="aObject"):
        """API to navigate to 'Setting' menu"""
        if os_obj == "aObject":
            obj.click(client, "NATIVE", "xpath=//*[@id='ic_menu']", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", """xpath=(//*[@id='left_drawer']
            /*/*[@id='lblListHeaderSlideView'])[5]""", 0, 1)
        else:
            # "ios code will come here"
            time.sleep(2)
            obj.click(client, "NATIVE", """xpath=//*[@class='UIImageView' and @height>0
            and ./parent::*[@accessibilityLabel='Menu icn 1x']]""", 0, 1)
            time.sleep(2)
            obj.click(client, "NATIVE", """xpath=//*[@class='YGLinedView'
            and ./following-sibling::*[@accessibilityLabel='Settings']]""", 0, 1)
