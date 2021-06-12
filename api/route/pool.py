from flask import Blueprint,request,jsonify
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flasgger import swag_from
import math

pools = {}

pool_api = Blueprint('pools', __name__)

def insert_or_append_pool(pool_id, pool_values):
    if (pool_id in pools):
        pools[pool_id].extend(pool_values)
        pools[pool_id].sort()
        return 'appended'
    else:
        pools[pool_id] = sorted(pool_values)
        return 'inserted'

def find_quantile(pool_values, percentile):
    k = (len(pool_values) - 1) * float(percentile) / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(pool_values[int(f)])
    else:
        d0 = pool_values[int(f)] * (c - k)
        d1 = pool_values[int(c)] * (k - f)
        return float(d0+d1)

schema_insert_pool = {
    'type': 'object',
    'properties': {
        'pool_id': {'type': 'number'},
        'pool_values': {'type': 'array', 'items': {'type': 'number'}}
    },
    'required': ['pool_id', 'pool_values']
}

schema_query_pool = {
    'type': 'object',
    'properties': {
        'pool_id': {'type': 'number'},
        'percentile': {'type': 'number', 'minimum': 0, 'maximum': 100}
    },
    'required': ['pool_id', 'percentile']
}

@pool_api.route('/pools/append_pool', methods=['POST'])
@expects_json(schema_insert_pool)
def pools_insert_or_append():
    """
    Insert or update (if exists) a pool
    ---
    tags:
      - pool
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          properties:
            pool_id:
              type: number
              description: Id of the pool
              required: true
            pool_values:
              type: array
              description: values need to be add to pool
              required: true
              items:
                type: number

    responses:
      200:
        description: Status of request, "appended" if pool exists, "insterted" if pool is not exists
        schema:
          properties:
            pool_id:
              type: number
              description: The id of pool
            status:
              type: string
              description: The status of POST
      400:
        description: Incorrect format parameter
        schema:
          properties:
            error:
              type: string
              description: Details message error

    """

    posted_data = request.get_json()
    pool_id = posted_data['pool_id']
    pool_values = posted_data['pool_values']
    status = insert_or_append_pool(pool_id, pool_values)
    return jsonify({'status': status})


@pool_api.route('/pools/query_pool', methods=['POST'])
@expects_json(schema_query_pool)
def query_pool():
    """Query the size of pool and the quantile of pool with input percentile number
    ---
    tags:
      - pool
    parameters:
      - in: body
        name: payload
        required: true        
        schema:
          properties:
            pool_id:
              type: number
              description: Id of the pool
              required: true
            percentile:
              type: number
              description: A quantile (in percentile form)
              required: true
              minimum: 0
              maximum: 100
    responses:
      200:
        description: Return the size of pool and the quantile of pool with input percentile number. If the input pool does not exist in pools, the pool_size value is 0 and pool_quantile is null
        schema:
          properties:     
            pool_size:
              type: number
              description: Size of pool
            pool_quantile:
              type: string
              description: The quantile of pool with input percentile number
      400:
        description: Incorrect format parameter
        schema:
          properties:
            error:
              type: string
              description: Details message error              
    """
    posted_data = request.get_json()
    pool_id = posted_data['pool_id']
    percentile = posted_data['percentile']
    pool_size = len(pools[pool_id]) if pool_id in pools else 0
    quantile = find_quantile(pools[pool_id], percentile) if pool_size != 0 else None
    return jsonify({'pool_quantile': quantile, 'pool_size': pool_size})    


@pool_api.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return jsonify({'error': original_error.message}), 400
    return error