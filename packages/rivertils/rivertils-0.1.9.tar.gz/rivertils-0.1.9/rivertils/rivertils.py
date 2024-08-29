import argparse
from datetime import datetime, timedelta
from statistics import mean
import traceback
import pytz
from rivertils.lists import *
import time
from google.cloud import translate_v2
import os
import six

from dotenv import load_dotenv

load_dotenv()




def add_bayesian_average_column(data: list[dict], value_col: str, count_col: str) -> list[dict]:
    """
    Adds a 'bayesian_average' column to each dictionary in the input data list.

    This function calculates a Bayesian average for each item in the data. The Bayesian average is a way to combine an 
    item's individual average rating and the overall average rating of all items, weighted by the number of ratings 
    the item has. This helps prevent items with very few ratings from having an overly high or low average, which 
    can be misleading.

    Args:
        data: A list of dictionaries where each dictionary represents an item and contains its rating and count.
        value_col: The key in the dictionaries that holds the individual average rating for each item.
        count_col: The key in the dictionaries that holds the number of ratings for each item.

    Returns:
        A list of dictionaries, where each dictionary now includes a 'bayesian_average' key with the calculated value.

    Example:
        data = [
            {'name': 'Item A', 'rating': 4.5, 'count': 2},
            {'name': 'Item B', 'rating': 3.8, 'count': 10},
            {'name': 'Item C', 'rating': 5.0, 'count': 1}
        ]
        result = add_bayesian_average_column(data, 'rating', 'count')
        # result will be:
        # [
        #     {'name': 'Item A', 'rating': 4.5, 'count': 2, 'bayesian_average': ...},
        #     {'name': 'Item B', 'rating': 3.8, 'count': 10, 'bayesian_average': ...},
        #     {'name': 'Item C', 'rating': 5.0, 'count': 1, 'bayesian_average': ...}
        # ]
    """


    m = mean([row[count_col] for row in data])  # Mean count of all items

    C = mean([row[value_col] for row in data])  # Global average rating



    for row in data:

        n = row[count_col]  # Individual count for the specific item

        R = row[value_col]  # Individual average rating for the specific item

        bayesian_average = (n * R + m * C) / (n + m)  # Correct computation

        row['bayesian_average'] = bayesian_average

    return data


def average_a_list_of_numbers(num_list, weight_to_preferred=1.5):
    """
    Iterate through num_list and, if there are multiple ratings, compute the average rating. 
    Use the following formula to give more weight to those ratings that were updated more recently:
    - If there is one unique rating, use it.
    - If there are 2 unique ratings, the first one gets 160% weight and the second one gets 25% weight.
    - If there are 3 ratings, the first one gets 50% weight, the second one gets 30% weight, and the third one gets 20% weight.
    - And so on. So ultimately, there will be only one rating.
    """
    if len(num_list) == 0:
        raise ValueError('num_list must have at least one element')
    elif len(set(num_list)) == 1:
        return num_list[0]
    else:
        weight_to_less_preferred = 2 - weight_to_preferred  
        current_average = num_list[0]
        for i in range(1, len(num_list)):
            next_num_in_list = num_list[i]
            current_average = ((current_average * weight_to_less_preferred) + ( next_num_in_list * weight_to_preferred)) / 2
        return current_average
        


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue

def fill_empty_cells(sheet, data):
    """
    Ensure any file rows that don't have a sheet row yet get all the keys.
    Add keys with empty values to each song dict if they're missing.

    Args:
        sheet: The spreadsheet object.
        data (List[dict]): List of dictionaries representing song data.

    Returns:
        None
    """
    """ ENSURE ANY FILE ROWS THAT DON'T HAVE A SHEET ROW YET GET ALL THE KEYS. add keys with empty values to each song dict if they're missing """

    data_keys = get_keys(data)

    # get the keys to populate each song dictionary
    sheet_keys = sheet.row_values(1)

    # # pprint(sheet_keys)
    # keys = set(sheet_keys + data_keys)

    # print the keys to the top of the spreadsheet. only need to do this once.
    # sheet.append_row(keys)
    # exit()

    # add keys with empty values to each song dict if theyre missing
    for row in data:
        for key in sheet_keys:
            if key not in row:
                row[key] = ""

    return data
def get_keys(data):
    keys = []
    for row in data:
        for k, v in row.items():
            if k not in keys:
                keys.append(k)
    return keys

def get_language(message):
    """
    A crude quick test likely returns None
    """
    language = None
    if len(message) < 3:
        language = "en"
    else:
        # phrases like 'haha' are triggering bizarre language ids
        for x in indicates_english_message:
            if x.lower() in message.lower():
                language = "en"
    # print(f"from get_language(): {language}")
    return language

def is_dst(zonename):
    """
    Determines if daylight saving time (DST) is currently in effect for a given timezone.

    Args:
        zonename (str): The name of the timezone to check for DST.

    Returns:
        bool: True if DST is in effect, False otherwise.

    Raises:
        pytz.UnknownTimeZoneError: If the provided timezone name is invalid.

    Examples:
        >>> is_dst('America/Los_Angeles')
        True
        >>> is_dst('Europe/Paris')
        False
    """
    tz = pytz.timezone(zonename)
    now = datetime.now(tz)
    return now.astimezone(tz).dst() != timedelta(0)
def translate_text(text):
    """
    
    Translates text into the target language with Google Cloud Translate API.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    """
    
    translate_client = translate_v2.Client( )

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=None)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result

def get_runtime_pacific_offset():

    return "-07:00" if is_dst("America/Los_Angeles") else "-08:00"
def get_test_message_and_language(message: str):
    """
    Removes any @mention at the start of the message string.
    If the message is not english, it translates it to english.
    Also, returns a language code to let you know which language the user is communicating in.
    """
    # print("get_message_and_language()")

    # response = None
    language = None

    # message = remove_at(message)
    # print(f"{message=}")

    

    # blob = TextBlob(message)
    # print(f"blob= {blob}")
    # exit()

    language_code = get_language(message)
    # print(f"{language_code=}")

    if not language:

        try:    
            translation = translate_text(message)
            # print(f"{translation=}")

            language_code = translation["detectedSourceLanguage"]

            if translation["detectedSourceLanguage"] != "en":
                
                message = translation["translatedText"]
                # print(f"{language=}")
                # print(f"{message=}")
        except Exception as e:
            print(
                "Rivertils: couldn't do translator.translate in get_message_and_language.py: ",
                e,
                message,
                language,
            )
            language_code = "en"


    # print(f"returning {message}, {language_code}")
    return message, language_code
    # return response


def sleep(seconds):
    """
    Sleep for a given number of seconds.
    """
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
# def remove_at(message):
#     """
#     If there's a comma in the first 20 characters
#     Remove everything before and including the first comma.
#     """

#     # If there's a comma in the first 20 characters
#     if "," in message[:20]:

#         # Remove everything before and including the first comma.
#         message = message.split(",", 1)[1].strip()

#     return message

