#!/usr/bin/python
from test_shared import *
from lib.sim900.smshandler import SimGsmSmsHandler, SimSmsPduCompiler
import random

COMPORT_NAME = "com22"

# logging levels
CONSOLE_LOGGER_LEVEL = logging.INFO
LOGGER_LEVEL = logging.INFO

# WARN: scecify recipient number here!!!
TARGET_PHONE_NUMBER = "+38 097 123 45 67"

# You can specify SMS center number, but it's not necessary. If you will not specify SMS center number, SIM900
# module will get SMS center number from memory
# SMS_CENTER_NUMBER       = "+1 050 123 45 67"
SMS_CENTER_NUMBER = ""


def printScaPlusPdu(pdu, logger):
    # printing SCA+PDU just for debug
    d = pdu.compile()
    if d is None:
        return False

    for (sca, pdu,) in d:
        logger.info("sendSms(): sca + pdu = \"{0}\"".format(sca + pdu))


def sendSms(sms, pdu, logger):
    # just for debug printing all SCA + PDU parts
    printScaPlusPdu(pdu, logger)

    if not sms.sendPduMessage(pdu, 1):
        logger.error("error sending SMS: {0}".format(sms.errorText))
        return False

    return True


def main():
    """
    Tests SMS sending.

    :return: true if everything was OK, otherwise returns false
    """

    # adding & initializing port object
    port = initializeUartPort(portName=COMPORT_NAME)

    # initializing logger
    (formatter, logger, consoleLogger,) = initializeLogs(LOGGER_LEVEL, CONSOLE_LOGGER_LEVEL)

    # making base operations
    d = baseOperations(port, logger)
    if d is None:
        return False

    (gsm, imei) = d

    # creating object for SMS sending
    sms = SimGsmSmsHandler(port, logger)

    # ASCII
    logger.info("sending ASCII (Latin-1) SMS")
    pduHelper = SimSmsPduCompiler(
        SMS_CENTER_NUMBER,
        TARGET_PHONE_NUMBER,
        "Hello, world! Message from GSM module. Testing ASCII (Latin-1) message. "
        "It must be single SMS (maximum length of message is 160 symbols). Enjoy!"
    )
    if not sendSms(sms, pduHelper, logger):
        return False

    # UCS2
    logger.info("sending UCS2 message")
    pduHelper = SimSmsPduCompiler(
        SMS_CENTER_NUMBER,
        TARGET_PHONE_NUMBER,
        "Test message, тестовое сообщение"
    )
    if not sendSms(sms, pduHelper, logger):
        return False

    # long UCS2 message
    logger.info("sending long UCS2 (Unicode) SMS")
    pduHelper = SimSmsPduCompiler(
        SMS_CENTER_NUMBER,
        TARGET_PHONE_NUMBER,
        "Це час, коли із затінку гілок "
        "Лунає дзвінко пісня солов'я. "
        "Це час, коли закохані шепочуть "
        "Такі солодкі клятви і слова. "
        "І хлюпіт річки, й ніжний трепет вітерця "
        "Звучить як музика в покинутих серцях. "
        "І кожну квітку приголубила роса, "
        "І зорі пострічались в небесах, "
        "І в хвилях зупинилася блакить, "
        "І на листочках тьмяна барва спить. "
        "А в небі загадкова невідомість "
        "Так ніжно-темна й лагідно-прозора, "
        "Що настає, як день згаса привітний, "
        "І тануть сутінки у місячному світлі."
    )

    pduHelper.setValidationPeriodInDays(10)

    if not sendSms(sms, pduHelper, logger):
        return False

    gsm.closePort()
    return True


if __name__ == "__main__":
    main()
    print("DONE")
