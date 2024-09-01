import pandas as pd
import numpy as np
import requests
import json


def date_converter(date_string):
    new_string = date_string+"T00:00:00+03:00"
    return new_string

def epias_tgt(e_mail,psw):

    url = f"https://giris.epias.com.tr/cas/v1/tickets?username={e_mail}&password={psw}"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept':"text/plain"
        
    }
    global response
    response = requests.request("POST", url, headers=headers,timeout=30)

    if response.status_code == 201:
        return response.text

def epias_mcp(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the MCP for a given interval
    
    """
    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/mcp?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        
        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        return response.text

def epias_kgup(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the DPP's (KGUP) based on resources for a given interval
    """

    url = f"HTTPS://seffaflik.epias.com.tr/electricity-service/v1/generation/data/dpp?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd,
      "region": "TR1",

    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        response.text

def epias_plant_kgup(start_date,end_date,pl_id,o_id,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the DPP's (KGUP) based on resources for a given interval (org_id: Organization ID, pl_id: Plant ID)
    
    Organization IDs can be obtained via epias_org function 

    Plant IDs can be obtained via  epias_uevcb function

    """

    url = f"HTTPS://seffaflik.epias.com.tr/electricity-service/v1/generation/data/dpp?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd,
      "region": "TR1",
      "organizationId": o_id,
      "uevcbId": pl_id

    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        response.text

def epias_org(start_date,end_date,tgt,e_mail,psw):

    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the organizations for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/organization-list?username={e_mail}&password={psw}"


    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])

        return df
    else:
        return response.text
    

def epias_uevcb(start_date,end_date,o_id,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the UEVCB data for a given interval (o_id: Organization ID)
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/uevcb-list?username={e_mail}&password={psw}"

    payload = json.dumps({
      "organizationId": o_id,
      "startDate":  sd,
      "endDate":  ed
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        return df
    else:
        return response.text

    
def epias_demand(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the real time electricity consumption for a given interval
    
    """

    url = f"HTTPS://seffaflik.epias.com.tr/electricity-service/v1/consumption/data/realtime-consumption?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd,
      "region": "TR1",

    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }


    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        response.text

def epias_idmp(start_date,end_date,tgt,e_mail,psw):

    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the intraday markey prices for a given interval
    
    """
    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/idm/data/weighted-average-price?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])

        return df
    else:
        return response.text
    
def epias_idma(start_date,end_date,tgt,e_mail,psw):
  
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the trade amount at intraday market for a given interval 

    """
    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/idm/data/matching-quantity?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])

        return df
    else:
        return response.text
    

def epias_smp(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the System Marginal Price for a given interval 
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/bpm/data/system-marginal-price?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    

def epias_sd(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that returns the System Direction for a given interval 
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/bpm/data/system-direction?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text

def epias_yal(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of load orders (YAL) for a given interval 
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/bpm/data/order-summary-up?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.drop(columns = ["upRegulationDelivered","net"], inplace = False)
        df.rename(columns = {'upRegulationZeroCoded':'YAL 0','upRegulationOneCoded':'YAL 1','upRegulationTwoCoded':'YAL 2'}, inplace = True)

        return df
    else:
        return response.text
    
def epias_yat(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of deload orders (YAT) for a given interval 
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/bpm/data/order-summary-down?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.drop(columns = ["downRegulationDelivered","net"], inplace = False)
        df.rename(columns = {'downRegulationZeroCoded':'YAT 0','downRegulationOneCoded':'YAT 1','downRegulationTwoCoded':'YAT 2'}, inplace = True)

        return df
    else:
        return response.text    


def epias_sfc(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the SFC prices for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/ancillary-services/data/secondary-frequency-capacity-price?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    
def epias_pfc(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the SFC prices for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/ancillary-services/data/primary-frequency-capacity-price?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    

def epias_pi_offer(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of price independent offers in day-ahead-market for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/price-independent-offer?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        
        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
def epias_pi_bid(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of price independent bids in day-ahead-market for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/price-independent-bid?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    
    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    
def epias_spot(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of matched amount in day-ahead-market for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/clearing-quantity?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    
    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])

        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    
def epias_ba_offers(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of block offers (matched and non-matched) of day-ahead-market for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/amount-of-block-selling?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])

        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
    

def epias_ba_bids(start_date,end_date,tgt,e_mail,psw):
    
    sd = date_converter(start_date)
    ed = date_converter(end_date)

    """
    Function that turns the amount of block bids (matched and non-matched) of day-ahead-market for a given interval
    
    """

    url = f"https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/amount-of-block-buying?username={e_mail}&password={psw}"

    payload = json.dumps({
      "endDate": ed,
      "startDate": sd
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': "application/json",
      'TGT':tgt
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:

        df = pd.json_normalize(response.json()['items'])
        df['date'] = pd.to_datetime(df['date'])

        return df
    else:
        return response.text
  

  