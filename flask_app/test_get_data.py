# import requests
# import json
# import datetime

# cluster = "nam1"
# application = "ncrc-1173-mkrwan-1310"
# app_key = "NNSXS.T4KWNY3LYSGIGS6YI3ES57QIB3SZ63C43QKMMXY.RKU3O2I6J5SRIK535YXWS4R7TPDBYQK5X4OFWEGNBGCHTOKW3OWQ"

# def get_new_data():
#     last_seconds = 3600  
#     for each_device in ["eui-a8610a34363a9216"]:  
#         payload_endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.decoded_payload&time={last_seconds}s"
#         metadata_endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.rx_metadata&time={last_seconds}s"
        
#         key = f'Bearer {app_key}'
#         headers = {'Authorization': key}

#         try:
#             payload_response = requests.get(payload_endpoint, headers=headers)
#             if payload_response.status_code != 200:
#                 print("Payload request failed:", payload_response.reason)
#                 continue
            
#             metadata_response = requests.get(metadata_endpoint, headers=headers)
#             if metadata_response.status_code != 200:
#                 print("Metadata request failed:", metadata_response.reason)
#                 continue

#             process_data(each_device, payload_response, metadata_response)

#         except Exception as e:
#             print("Error processing response:", e)

# def process_data(each_device, payload_response, metadata_response):
#     try:
#         payload_data = payload_response.json().get("data", [])
#         metadata_data = metadata_response.json().get("data", [])
#     except json.JSONDecodeError as e:
#         print("Error decoding JSON response:", e)
#         print("Payload response text:", payload_response.text)
#         print("Metadata response text:", metadata_response.text)
#         return
    
#     for payload_item, metadata_item in zip(payload_data, metadata_data):
#         result = payload_item.get("result", {})
#         uplink_message = result.get("uplink_message", {})
#         decoded_payload = uplink_message.get("decoded_payload", {})
#         received = result.get("received_at", "")
#         lat = decoded_payload.get("latitude", "")
#         lon = decoded_payload.get("longitude", "")
#         temp = decoded_payload.get("temperature", "")
#         humidity = decoded_payload.get("humidity", "")
        
#         rx_metadata = metadata_item.get("result", {}).get("uplink_message", {}).get("rx_metadata", [{}])[0]
#         rssi = rx_metadata.get("rssi", "")
#         snr = rx_metadata.get("snr", "")
#         gateway_id = rx_metadata.get("gateway_ids", {}).get("gateway_id", "")
        
#         print("Gateway ID:", gateway_id)
#         print("Device ID:", each_device)
#         print("Latitude:", lat)
#         print("Longitude:", lon)
#         print("Temperature:", temp)
#         print("Humidity:", humidity)
#         print("RSSI:", rssi)
#         print("SNR:", snr)
#         print("-------------------------")

# get_new_data()

import requests
import json

cluster = "nam1"
application = "sensecap-lora-tracker"
app_key = "NNSXS.TGFGSOEXIKJROJXVOWTDUUOVWQH76LKAKOPLICI.7VSE4Z6NTIHL5WQBASAB7MX7COYW6CNL66NCVRTH5674DR4ZIKWQ"

def get_new_data():
    last_seconds = 3600  
    for each_device in ["eui-2cf7f1c054600134"]:  
        payload_endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.decoded_payload&time={last_seconds}s"
        metadata_endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.rx_metadata&time={last_seconds}s"
        
        key = f'Bearer {app_key}'
        headers = {'Authorization': key}

        try:
            payload_response = requests.get(payload_endpoint, headers=headers)
            if payload_response.status_code != 200:
                print("Payload request failed:", payload_response.reason)
                continue
            
            metadata_response = requests.get(metadata_endpoint, headers=headers)
            if metadata_response.status_code != 200:
                print("Metadata request failed:", metadata_response.reason)
                continue

            process_data(each_device, payload_response, metadata_response)

        except Exception as e:
            print("Error processing response:", e)

def process_data(each_device, payload_response, metadata_response):
    try:
        payload_data = payload_response.json().get("data", [])
        metadata_data = metadata_response.json().get("data", [])
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        print("Payload response text:", payload_response.text)
        print("Metadata response text:", metadata_response.text)
        return

    
    # Limit the loop to 2 iterations to show only the first 2 records
    for i in range(min(2, min(len(payload_data), len(metadata_data)))):
        payload_item = payload_data[i]
        metadata_item = metadata_data[i]
        
        result = payload_item.get("result", {})
        uplink_message = result.get("uplink_message", {})
        decoded_payload = uplink_message.get("decoded_payload", {})
        received = result.get("received_at", "")
        
        # Extracting temperature, latitude, and longitude
        messages = decoded_payload.get("messages", [])
        temp, lat, lon = None, None, None
        for message in messages:
                    if "Air Temperature" in message:
                        temp = message["Air Temperature"]
                    if "Longitude" in message:
                        lon = message["Longitude"]
                    if "Latitude" in message:
                        lat = message["Latitude"]
        
        rx_metadata = metadata_item.get("result", {}).get("uplink_message", {}).get("rx_metadata", [{}])[0]
        rssi = rx_metadata.get("rssi", "")
        snr = rx_metadata.get("snr", "")
        gateway_id = rx_metadata.get("gateway_ids", {}).get("gateway_id", "")
        
        print("Gateway ID:", gateway_id)
        print("Device ID:", each_device)
        print("Latitude:", lat)
        print("Longitude:", lon)
        print("Temperature:", temp)
        print("RSSI:", rssi)
        print("SNR:", snr)
        print("-------------------------")

get_new_data()


