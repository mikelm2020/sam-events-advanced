import boto3

location_client = boto3.client('location')

def get_place_from_address(address, place_index):
    params = {
        'IndexName': place_index,
        'Text': address
    }
    response = location_client.search_place_index_for_text(**params)
    print(response)
    return response['Results'][0]['Place']

def get_route_for_address(destination_address, start_address_place, route_calculator):
    destination_place = get_place_from_address(destination_address, place_index)
    
    params = {
        'CalculatorName': route_calculator,
        'DeparturePosition': start_address_place['Geometry']['Point'],
        'DestinationPosition': destination_place['Geometry']['Point']
    }

    response = location_client.calculate_route(**params)
    print(response)
    return response