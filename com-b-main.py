import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List

# Endpoint and auth
BASELINE_URL = "https://datacollection.risa.eu/onboarding/participantsBaseline/"
USERNAME = "meliora"
PASSWORD = "jxKEwO0V4v7i0xo"

"""Initial implementation based on the COM-B model for 3 outcomes.
    1. Physical Activity
    2. Alcohol Intake
    3. Smoking Activity
    
    This initial version will parse the onboarding questionnaires of participants, scan the relevant 
    questions and define the capability, opportunity and motivation levels (low, medium, high) for each outcome.    

    One idea is to perhaps create mini-DAGs for each outcome. 
    
    The next step is to recommend initial courses based on the COM-B levels for each outcome. 
"""


def extract_answer(answers, qid, option=None):
    for ans in answers:
        if ans["questionId"] == qid and (option is None or ans.get("option") == option):
            return ans["answer"]
    return None

def categorize_alcohol(answers: List[Dict]) -> Dict[str, str]:
    freq = extract_answer(answers, "alcohol_consumption_frequency")
    intake = extract_answer(answers, "typical_daily_alcohol_intake")
    heavy = extract_answer(answers, "frequent_heavy_drinking")

    capability = "medium" if intake in ["1-2", "3-4"] else "high" if intake == "none" else "low"
    opportunity = "medium" if freq in ["monthly_or_less"] else "low" if freq == "daily_or_almost_daily" else "high"
    motivation = "low" if heavy in ["weekly", "daily"] else "medium" if heavy == "monthly" else "high"

    return {
        "behavior": "alcohol",
        "capability": capability,
        "opportunity": opportunity,
        "motivation": motivation
    }

def categorize_physical_activity(answers: List[Dict]) -> Dict[str, str]:
    health = extract_answer(answers, "general_health")
    fatigue = extract_answer(answers, "symptoms_experienced_last_week", "fatigue")
    caring = extract_answer(answers, "caring_responsibilities")
    area = extract_answer(answers, "area")

    capability = "low" if health == "poor" or int(fatigue or 0) > 6 else "medium"
    opportunity = "low" if caring == "yes" and area == "urban" else "medium" if area == "rural" else "high"
    depression = extract_answer(answers, "recent_problems_frequency", "feeling_down")
    anxiety = extract_answer(answers, "recent_problems_frequency", "feeling_nervous")
    motivation = "high" if depression == "not_at_all" and anxiety == "not_at_all" else "medium"

    return {
        "behavior": "physical_activity",
        "capability": capability,
        "opportunity": opportunity,
        "motivation": motivation
    }

def categorize_smoking(answers: List[Dict]) -> Dict[str, str]:
    smoking_status = extract_answer(answers, "current_smoking_status")
    #### To add more
    if smoking_status is None:
        return {
            "behavior": "smoking",
            "capability": "unknown",
            "opportunity": "unknown",
            "motivation": "unknown"
        }

    if smoking_status == "never":
        return {
            "behavior": "smoking",
            "capability": "high",
            "opportunity": "high",
            "motivation": "high"
        }
    elif smoking_status == "former":
        return {
            "behavior": "smoking",
            "capability": "high",
            "opportunity": "medium",
            "motivation": "medium"
        }
    else:  # current smoker
        return {
            "behavior": "smoking",
            "capability": "low",
            "opportunity": "medium",
            "motivation": "low"
        }

def categorize_user_onboarding(data: Dict) -> List[Dict[str, str]]:
    answers = data.get("answers", [])
    return [
        categorize_physical_activity(answers),
        categorize_alcohol(answers),
        categorize_smoking(answers)
    ]

def main():
    user_id = 'SE337241'
    try:
        response = requests.get(BASELINE_URL+user_id, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()

        results = categorize_user_onboarding(data)
        for r in results:
            print(f"Behavior: {r['behavior']}")
            print(f"  Capability: {r['capability']}")
            print(f"  Opportunity: {r['opportunity']}")
            print(f"  Motivation: {r['motivation']}")
            print()

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")

if __name__ == "__main__":
    main()
