from flask import request, jsonify

def paginate_query(query, schema, limit_default=10, limit_max=100):
    try:
        limit = int(request.args.get('limit', limit_default))
        offset = int(request.args.get('offset', 0))

        if limit < 1 or offset < 0:
            return jsonify({"error": "Invalid parameters. Limit must be greater than 0 and offset must be non-negative."}), 400

        # Cap the maximum limit value
        limit = min(limit, limit_max)

        # Apply limit and offset to query
        items = query.limit(limit).offset(offset).all()

        # Serialize the items using the given schema
        return jsonify(schema.dump(items)), 200

    except ValueError:
        return jsonify({"error": "Limit and offset must be integers."}), 400
