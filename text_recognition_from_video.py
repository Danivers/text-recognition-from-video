import cv2
import numpy as np
import pytesseract
import re
import os
from joblib import Parallel, delayed
import multiprocessing

directory = "your videos path"
pytesseract.pytesseract.tesseract_cmd = r"your installation folder"
num_cores = multiprocessing.cpu_count()
files_list = os.listdir(directory)

keyWord = 'answer' #filter based on answer lines


def get_text(path):
    text = ''
    count = 40
    capture = cv2.VideoCapture(path)

    while capture.isOpened():
        retrieve, frame = capture.read()
        if not retrieve:
            print("\nEnd of the stream. Exiting ...")
            break
        frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        frame = cv2.blur(frame, (15,15))
        ret, thresh_image = cv2.threshold(frame, 210, 255, cv2.THRESH_BINARY)

        text += pytesseract.image_to_string(thresh_image)

        print("\nText retrieved for file {} Frame at: {}".format(path, count))

        count += 60

        capture.set(1, count)

        if cv2.waitKey(20) & 0xFF == ord('q') or not capture.read():
            break

    results = filter_text(text)

    capture.release()
    return results


def filter_text(text):
    results = []
    lines = text.splitlines()
    # filter based on keyword
    for index, line in enumerate(lines):
        if keyWord in line:
            #keep only numbers & letters
            re_line = re.sub('[\W_]+', '', lines[index-1])
            results.append(re_line)
    # remove duplicates
    results = list(dict.fromkeys(results))
    return results

def filter_results(total_list):
    dict_results = {}
    for name in total_list:
        if name in dict_results.keys():
            dict_results[name] += 1
        else:
            dict_results[name] = 1
    return dict_results


def get_participants(filename):
    participants = []
    text = get_text(os.path.join(directory, filename))
    participants += text
    return participants


def get_winners(total_dict):
    winners = 0
    for key, value in total_dict.items():
        if value == len(files_list) and key is not '':
            print("\n" + "@" + key)
            winners += 1
            if winners % 10 == 0:
                print("\n")
    if winners == 0:
        print("\nNo winners for this quiz :(, good luck next time!")
    print("\nTotal winners for this quiz: " + str(winners))



if __name__ == '__main__':
    participants = []
    with multiprocessing.Pool(processes=num_cores) as processes:
        participants = processes.map(get_participants, [filename for filename in files_list])

    merged_participants = []
    participants_dict = {}
    for p_list in participants:
        merged_participants += p_list
    print("\nmerged Participants: {}".format(merged_participants))
    participants_dict = filter_results(merged_participants)
    get_winners(participants_dict)


# participants = Parallel(n_jobs=num_cores)(delayed(get_participants(filename))
#                                           for filename in os.listdir(directory))

# loop = asyncio.get_event_loop()
# res = loop.run_until_complete(main())

# filter_text("bianca + answered ^ dksjkdsjdjskjds")
# loop = asyncio.get_event_loop()
# res = loop.run_until_complete(main())


