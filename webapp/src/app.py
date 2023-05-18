import os

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# read config parameters
# with open('src/config.json', 'r') as c:
#     config = json.loads(c.read())

# CATEGORY = config["Category"]

CATEGORY = os.getenv("dataCategory", "planets")

@app.get("/")
def hello():
    return {"message": "Hello, World!"}


@app.get("/data")
def get_star_wars_data(id=1):
    try:
        # TODO: Replace the "1" in the URL below with the value of a query parameter
        # TODO: Replace the "people" in the URL below with the value of a configuration parameter
        response = requests.get(f"https://swapi.dev/api/{CATEGORY}/{id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


# TODO: Add new endpoint to return the top 20 people in the Star Wars API with the highest BMI.
@app.get("/top-people-by-bmi")
def top_people_by_bmi():
    try:
        url = "https://swapi.dev/api/people"
        top_twenty = []
        while url:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            for people in response.json()["results"]:
                if people["mass"] != "unknown" and people["height"] != "unknown":
                    mass_num = float(people["mass"].replace(",", ""))  # in kg
                    height_num = float(people["height"].replace(",", ""))  # in centermeter
                    # add new key for sorting
                    people["bmi"] = mass_num / ((height_num / 100) ** 2)
                    top_twenty.append(people)

            url = response.json()["next"]
        
        # sort by bmi, get the last 20 and revser the list
        top_twenty = sorted(top_twenty, key=lambda x: int(x['bmi']))[-20:][::-1]  # slice before reverse
        # remove key "bmi" as it's not the data provided originally
        top_twenty = [{category: value for category, value in dude.items() if category != 'bmi'} for dude in top_twenty]

        return top_twenty
    
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
