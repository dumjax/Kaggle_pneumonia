import copy
import csv

def iou(bb1, bb2):
    '''given two boxes, return intersection over union surfaces'''
    (x1, y1, w1, h1) = bb1
    (x2, y2, w2, h2) = bb2

    x_overlap = min(x1 + w1, x2 + w2) - max(x1, x2)
    y_overlap = min(y1 + h1, y2 + h2) - max(y1, y2)
    inters = max(0, x_overlap) * max(0, y_overlap)
    union_ = w1 * h1 + w2 * h2 - inters

    return inters / union_


def score_patient(bbs_guess, bbs_truth_, threshold):
    '''given two sets of boxes, calculate the score for a given threshold. 
    Assume that the first list is ordered by (decreasing) confidence'''

    # trivial cases
    if len(bbs_truth_) == 0:
        return 1. if len(bbs_guess) == 0 else 0.

    bbs_truth = copy.deepcopy(bbs_truth_)  # we're going to mess around with this list
    fp, tp = 0, 0
    for bb_guess in bbs_guess:
        scores = [iou(bb_guess, bb_truth) for bb_truth in bbs_truth]
        if max(scores) < threshold:  # false positive
            fp = fp + 1
        else:  # true positive
            tp = tp + 1
            (max_iou, idx) = max([(v, i) for i, v in enumerate(scores)])
            del bbs_truth[idx]  # remove the matched box from the truth list

    fn = len(bbs_truth)  # how many boxes didn't get matched?
    return tp / (tp + fp + fn)


def read_submission_file(file_name):
    '''returns a dictionary patientid:bounding boxes.
    The bounding boxes are sorted by confidence'''
    rv = {}
    with open(file_name) as f:
        generator = csv.reader(f)
        data = [[patient, box_data_str] for patient, box_data_str in generator]
        for patient, box_data_str in data[1:]:  # drop header
            if box_data_str == '':  # healthy case
                rv[patient] = []
            else:
                box_data = [float(x) for x in box_data_str.split(' ')]
                assert len(box_data) % 5 == 0  # should have confidence + 4 numbers
                # split into tuples of confidence, bounding boxes
                confidence_boxes = [(box_data[5*i], box_data[5*i+1:5*i+5]) for i in range(len(box_data) // 5)]
                # sort boxes by confidence
                confidence_boxes.sort()
                # store them by *decreasing* confidence
                rv[patient] = [box for conf, box in reversed(confidence_boxes)]
    return rv


def read_truth_file(file_name):
    '''returns a dictionary patientid:bounding boxes'''
    with open(file_name) as f:
        reader = csv.reader(f)
        data = [d for d in reader]
        patients = [d[0] for d in data[1:]]  # drop header
        rv = {p:[] for p in patients}

        for d in data:
            if d[-1] == '1':  # positive case
                rv[d[0]].append([float(x) for x in d[1:-1]])
    return rv


def score_submission(prediction_file, truth_file):
    '''calculate the evaluation metric for a given submission file'''
    thresholds = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]

    predictions = read_submission_file(prediction_file)
    truths = read_truth_file(truth_file)

    res = 0
    for threshold in thresholds:
        for patient, pred in predictions.items():
            truth = truths[patient]
            res = res + score_patient(pred, truth, threshold)

    return res / len(thresholds) / len(predictions)



test = score_submission('data/code_testing/submission 08333.csv', 'data/code_testing/truth.csv')
print(test)
test = score_submission('data/code_testing/submission 090625.csv', 'data/code_testing/truth.csv')
print(test)
test = score_submission('data/code_testing/submission 1.csv', 'data/code_testing/truth.csv')
print(test)

