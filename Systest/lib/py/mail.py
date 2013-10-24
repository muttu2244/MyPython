#!/usr/bin/env python2.4
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : This Script contains procedure to send mails
                          to the given persons with the specified message.

AUTHOR                  : treddy@stoke.com
REVIEWER                : jameer@stoke.com
"""

import os, time

from logging import getLogger

log = getLogger()

def mailSend(sender, receiver, sub, mesg ):
    """
    Description  : Used to send mails to the specified people with subject and message.
    Arguments    : sender -- sender mail id(must be one)
                   receiver -- receiver(s) mail id(if more than one separate by comma)
                   sub -- subject of the mail
                   mesg -- message to be displayed in the mail
    Usage        : 
    Return Value : No return value
    """
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location

    # Framing mail contents
    FROM = sender
    TO = receiver
    SUBJECT = sub
    TEXT = mesg

    # Prepare actual message template
    message = """\
      From: %s
      To: %s
      Subject: %s

      %s
    """ % (FROM, TO, SUBJECT, TEXT)
    print message
    
    log.output(message)
    # Sending mail
    p = os.popen("%s -t -i" % SENDMAIL, "w")
    p.write(message)
    time.sleep(10)
    status = p.close()

    # Checking mail status
    if status!=0:
        print "Mail sent successfully, status: ", status 
        log.info("Mail sent successfully, status: %s " % status)
    else:
        print "Unable to send mail, status: ", status
        log.error("Unable to send mail, status: %s " % status)
