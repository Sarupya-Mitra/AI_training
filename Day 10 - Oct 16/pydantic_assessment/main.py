from pydantic import BaseModel,ValidationError,Field
import logging
from typing import Literal
import json

class Registration(BaseModel):  # 1 creating the class
    # 2. Adding fields:
    registration_id : str
    name : str
    email : str
    age : int = Field(gt=18)  # 3. validate age to greater than 18
    ticket_type : Literal['Standard','Premium','VIP']  # 5. Validate ticket_types to these values only
    amount : int = Field(gt = 0)  # 4. amount should be greater than 0

logging.basicConfig(level=logging.INFO,
                    format = "%(levelname)s - %(message)s \n ................. \n",
                    filename = "registration.log", ### 16 Saving logs into a file
                    filemode = "a")
total_Records = 0
valid_Records = 0
invalid_Records = 0
try:
    with open("registrations.json") as file:
        data = json.load(file)
    total_Records = len(data)
    for elem in data: # 6 Validation each record
        # 7  printing only the successful ones
        try:
            # 15. Warning when VIP ticket is detected
            if(elem["ticket_type"] == "VIP"):
                logging.warning("VIP registration detected")
            registration = Registration(**elem)


            ## 13 Printing an info message
            logging.info(f"Registration {elem['registration_id']} validated successfully")
            valid_Records += 1
            print(registration, "\n")
            # 9 Serializing objects to dict
            reg_dict = registration.model_dump()
            print(type(reg_dict), "\n")
            # 10 Serializing objects to json
            reg_json = registration.model_dump_json(indent=4)
            print(type(reg_json), "\n")

            ## 11 Saving the valid registrations to a new json file
            # with open("valid_registrations.json","a") as f:
            #     f.write(reg_json + "\n")

        ### 8. Catching errors and showing the failed fields and IDs for the bad data
        except ValidationError as e:
            ### 14. Logging an error:
            logging.error(e)
            invalid_Records += 1
            # print(f"Element with id = {elem['registration_id']} has the following invalid fields:\n")
            # for err in e.errors():
            #     field_name = err['loc'][0]
            #     msg = err['msg']
            #     print(f" {field_name}: {msg} \n")
            continue
    ### 20 printing the total,valid and invalid records
    print("\n Total Records: ", total_Records , "Valid Records: ", valid_Records , "Invalid Records: ", invalid_Records)
except FileNotFoundError as err:  ### 17,18 File not found exception
    logging.error(err)
    print("File not Found")





