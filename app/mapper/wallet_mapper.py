def wallet_info_mapper(data):
    """
    input
    {
        "id": "0011b2fa-da4c-45e7-b2e0-b1f9a310cf96",
        "balance": 0.0,
        "token": "fecb1e1b-ebd1-4900-9700-ffd653f039fe",
        "customer_id": "dfjasdojgfaodsnfgasjdsssss",
        "status": "enabled",
        "created_at": "2023-08-04T04:46:31.080062",
        "enabled_at": "2023-08-04T04:47:10.874665",
        "updated_at": "2023-08-04T04:47:10.874665"
    }
    output
     {
     "id": "6ef31ed3-f396-4b6c-8049-674ddede1b16",
      "owned_by": "c4d7d61f-b702-44a8-af97-5dbdafa96551",
      "status": "enabled",
      "enabled_at": "1994-11-05T08:15:30-05:00",
      "balance": 0
      }
    """
    result = {
        "id": data["id"],
        "owned_by": data["customer_id"],
        "status": data["status"],
        "enabled_at": data["enabled_at"],
        "balance": data["balance"],
    }
    return result


def transactions_mapper(data):
    """
    [{
                "id": "19195df2-dcc6-416a-977a-ce447a60ef07",
                "wallet_id": "cb905c7e-b442-4cb4-b28b-6d7e087df20d",
                "created_at": "2023-08-04T06:42:32.105892",
                "type": "withdrawal",
                "reference_id": "dgsadfbdsfvafdbhdsfsddssss",
                "amount": 10.0,
                "status": "success"
    }]
    output
     [{
        "id": "c6dd5b25-d4fe-411c-a9c0-e2a9f1c724b3",
        "status": "success",
        "transacted_at": "1994-11-10T08:15:41-05:00",
        "type": "withdrawal",
        "amount": 890000,
        "reference_id": "57fa2a07-c1b7-40c8-8096-3736d1c8cfde"
      }]
    """
    result = []
    for row in data:
        result.append(
            {
                "id": row["id"],
                "status": row["status"],
                "transacted_at": row["created_at"],
                "type": row["type"],
                "amount": row["amount"],
                "reference_id": row["reference_id"],
            }
        )
    return result
