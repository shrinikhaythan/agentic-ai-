def get_policy_details(policy_id: str)->str :
    '''
    look up policy type by policy id 
    '''
    db={
        "P1001":"health insurance"
    }
    return db.get(policy_id,"policy not found")

