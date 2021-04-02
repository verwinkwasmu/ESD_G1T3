    # # 5. Put into dictionary for item_names
    # facility_names = {}
    # for facility in all_facilities['data']['facilities']:
    #     facility_names[facility['item_id']] = facility['item_name']

    # room_service_names = {}
    # for room_service in all_room_services['data']['room_services']:
    #     room_service_names[room_service['item_id']] = room_service['item_name']

    # # 6. return all cart purchases with item_name
    # for booking in cart_result['data']['bookings']:
    #     if 'rs' in booking['item_id']:
    #         booking['item_name'] = room_service_names[booking['item_id']]
    #     else:
    #         booking['item_name'] = facility_names[booking['item_id']]
    
    return {
        "code": 201,
        "booking_result": booking_result['data']
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for ordering room service...")
    app.run(host="0.0.0.0", port=5200, debug=True)