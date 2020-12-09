from typing import List
import random

# Object Vote with all the 16 (17 including class name) attributes
class Vote:

    def __init__(self,
                    class_name, 
                    handicapped_infants, 
                    water_project_cost_sharing,
                    adoption_of_the_budget_resolution, 
                    physician_fee_freeze, 
                    el_salvador_aid,
                    religious_groups_in_schools,
                    anti_satellite_test_ban,
                    aid_to_nicaraguan_contras,
                    mx_missile,
                    immigration,
                    synfuels_corporation_cutback,
                    education_spending,
                    superfund_right_to_sue,
                    crime,
                    duty_free_exports,
                    export_administration_act_south_africa
                ) :
        self.class_name = class_name
        self.handicapped_infants = handicapped_infants 
        self.water_project_cost_sharing = water_project_cost_sharing
        self.adoption_of_the_budget_resolution = adoption_of_the_budget_resolution
        self.physician_fee_freeze = physician_fee_freeze
        self.el_salvador_aid = el_salvador_aid
        self.religious_groups_in_schools = religious_groups_in_schools
        self.anti_satellite_test_ban = anti_satellite_test_ban
        self.aid_to_nicaraguan_contras = aid_to_nicaraguan_contras
        self.mx_missile = mx_missile
        self.immigration = immigration
        self.synfuels_corporation_cutback = synfuels_corporation_cutback
        self.education_spending = education_spending
        self.superfund_right_to_sue = superfund_right_to_sue
        self.crime = crime
        self.duty_free_exports = duty_free_exports
        self.export_administration_act_south_africa = export_administration_act_south_africa

    # return all the vote data as array
    def asArray(self):
        return [
            self.class_name,
            self.handicapped_infants,
            self.water_project_cost_sharing,
            self.adoption_of_the_budget_resolution,
            self.physician_fee_freeze,
            self.el_salvador_aid,
            self.religious_groups_in_schools,
            self.anti_satellite_test_ban,
            self.aid_to_nicaraguan_contras,
            self.mx_missile,
            self.immigration,
            self.synfuels_corporation_cutback,
            self.education_spending,
            self.superfund_right_to_sue,
            self.crime,
            self.duty_free_exports,
            self.export_administration_act_south_africa
        ]

def extractFileLines(filePath: str) -> List[str]:
    file1 = open(filePath, 'r') 
    lines = file1.readlines()

    return lines

def extractVoteGivenFileLine(line: str) -> Vote:
    attributes = line.split(sep=',')

    return Vote(
        attributes[0],
        attributes[1],
        attributes[2],
        attributes[3],
        attributes[4],
        attributes[5],
        attributes[6],
        attributes[7],
        attributes[8],
        attributes[9],
        attributes[10],
        attributes[11],
        attributes[12],
        attributes[13],
        attributes[14],
        attributes[15],
        attributes[16][0]
        )

def extractVotesGivenFileLines(fileLines: List[str]) -> List[Vote]:
    votes = []
    for line in fileLines:
        votes.append(extractVoteGivenFileLine(line))
    return votes

def extractVotesGivenFilePath(filePath: str) -> List[Vote]:
    lines = extractFileLines(filePath)
    
    return extractVotesGivenFileLines(lines)

def getProbabilityForAttrValueGivenRepublican(training_dataset: List[Vote], attr_index: int, attr_value: str, cached_probabilities):
    if cached_probabilities[attr_index][attr_value]["republican"] != -1:
        return cached_probabilities[attr_index][attr_value]["republican"]

    republicans_training_dataset = list(filter(lambda elem: elem.asArray()[0] == 'republican', training_dataset))
    filtered_given_value = list(filter(lambda elem: elem.asArray()[attr_index] == attr_value, republicans_training_dataset))

    probability = len(filtered_given_value) / len(republicans_training_dataset)
    cached_probabilities[attr_index][attr_value]['republican'] = probability

    return probability

def getProbabilityForAttrValueGivenDemocrat(training_dataset: List[Vote], attr_index: int, attr_value: str, cached_probabilities):
    if cached_probabilities[attr_index][attr_value]["democrat"] != -1:
        return cached_probabilities[attr_index][attr_value]["democrat"]
    
    democrats_training_dataset = list(filter(lambda elem: elem.asArray()[0] == 'democrat', training_dataset))
    filtered_democrats_given_value = list(filter(lambda elem: elem.asArray()[attr_index] == attr_value, democrats_training_dataset))

    probability = len(filtered_democrats_given_value) / len(democrats_training_dataset)
    cached_probabilities[attr_index][attr_value]["democrat"] = probability

    return probability

# Not used
def getProbabilityForRepublicanGivenAttrValue(training_dataset: List[Vote], attr_index: int, attr_value: str):
    filtered_given_value = list(filter(lambda elem: elem.asArray()[attr_index] == attr_value, training_dataset))
    filtered_republicans_training_dataset = list(filter(lambda elem: elem.asArray()[0] == 'republican', filtered_given_value))

    return len(filtered_republicans_training_dataset) / len(filtered_given_value)

# Not used
def getProbabilityForDemocratGivenAttrValue(training_dataset: List[Vote], attr_index: int, attr_value: str):
    filtered_given_value = list(filter(lambda elem: elem.asArray()[attr_index] == attr_value, training_dataset))
    filtered_republicans_training_dataset = list(filter(lambda elem: elem.asArray()[0] == 'democrat', filtered_given_value))

    return len(filtered_republicans_training_dataset) / len(filtered_given_value)

def get_democrat_count(dataset: List[Vote]):
    democrat_set = list(filter(lambda elem: elem.asArray()[0] == "democrat", dataset))

    return len(democrat_set)

def get_republican_count(dataset: List[Vote]):
    republican_set = list(filter(lambda elem: elem.asArray()[0] == "republican", dataset))

    return len(republican_set)


# Checks the probability for the vote to be democrat
def getProbabilityDemocrat(training_dataset: List[Vote], vote: Vote, cached_probabilities):
    probability = 1
    for attr_index in range(1, 16+1):
        probability = probability * getProbabilityForAttrValueGivenDemocrat(training_dataset, attr_index, vote.asArray()[attr_index], cached_probabilities)

    is_democrat_probability = get_democrat_count(training_dataset) / len(training_dataset)

    return probability * is_democrat_probability

def getProbabilityRepublican(training_dataset: List[Vote], vote: Vote, cached_probabilities):
    probability = 1
    for attr_index in range(1, 16+1):
        probability = probability * getProbabilityForAttrValueGivenRepublican(training_dataset, attr_index, vote.asArray()[attr_index], cached_probabilities)

    is_republican_probability = get_republican_count(training_dataset) / len(training_dataset)

    return probability * is_republican_probability

def predict(training_dataset: List[Vote], vote: Vote, cached_probabilities):
    probability_republican = getProbabilityRepublican(training_dataset, vote, cached_probabilities)
    probability_democrat = getProbabilityDemocrat(training_dataset, vote, cached_probabilities)

    if probability_republican > probability_democrat:
        return "republican"
    else:
        return "democrat"

def checkPrediction(training_dataset: List[Vote], vote: Vote, cached_probabilities) -> bool:
    actual = predict(training_dataset, vote, cached_probabilities)
    expected = vote.class_name

    return actual == expected

def divideIntoArraysEqualSize(array: List, num_arrays: int) -> List[List]:
    ten_arrays = [[], [], [], [], [], [], [], [], [], []]

    random.shuffle(array)

    arrays_size = (int)(len(array) / 10)
    start_index = 0
    last_index = arrays_size

    for i in range(num_arrays - 1):
       ten_arrays[i].extend(array[start_index:last_index])
       start_index += arrays_size
       last_index += arrays_size
    ten_arrays[num_arrays - 1].extend(array[start_index : len(array)])

    return ten_arrays

# accuracy double int [0, 1]
def getPredictionAccuracy(training_dataset: List[Vote], test_dataset: List[Vote], cached_probabilities):
    correct_predictions = 0
    for i in range(len(test_dataset)):
        if checkPrediction(training_dataset, test_dataset[i], cached_probabilities):
            correct_predictions += 1

    return correct_predictions / len(test_dataset)

# filePath path of file with the expected dataset
def algorithm(filePath: str):
    def initDictionary():
        init_dict = {}
        for attr_index in range(1, 17):
            init_dict[attr_index] = {}
            
            for attr_value in ["y", "n", "?"]:
                init_dict[attr_index][attr_value] = {}
                
                for vote_class in ["republican", "democrat"]:
                    init_dict[attr_index][attr_value][vote_class] = -1

        return init_dict

    filePath = "house-votes-84.data"
    cached_probabilities = initDictionary()
    votes = extractVotesGivenFilePath(filePath)

    votes_chunks = divideIntoArraysEqualSize(votes, 10)

    prediction_accuracy = 0

    for test_dataset_index in range(10):
        # votes_chunks[test_dataset_index] = test_dataset
        training_dataset = []
        # construct training dataset
        for i in range(10):
            if i == test_dataset_index:
                continue
            training_dataset.extend(votes_chunks[i])
            
        prediction_accuracy += (1 / 10) * getPredictionAccuracy(training_dataset, votes_chunks[test_dataset_index], cached_probabilities)

    return prediction_accuracy

filePath = "house-votes-84.data"
accuracy = algorithm(filePath)

print(accuracy)



