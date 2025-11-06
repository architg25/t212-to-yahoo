# Trading212 API Reference

## Base URLs

- **Live Environment**: `https://live.trading212.com`
- **Demo Environment**: `https://demo.trading212.com`

## Authentication

The API uses **HTTP Basic Authentication** with your API key as the username and API secret as the password.

**Format**: Base64-encode `API_KEY:API_SECRET` and prepend with `Basic `

```
Authorization: Basic base64(API_KEY:API_SECRET)
```

**Example (Python)**:
```python
import base64

api_key = "your_api_key"
api_secret = "your_api_secret"
credentials = f"{api_key}:{api_secret}"
encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
auth_header = f"Basic {encoded}"
```

**Example (cURL)**:
```bash
# Encode credentials
CREDENTIALS=$(echo -n "YOUR_API_KEY:YOUR_API_SECRET" | base64)

# Make request
curl -H "Authorization: Basic $CREDENTIALS" \
     https://demo.trading212.com/api/v0/equity/account/cash
```

## Account Data Endpoints

### Get Account Cash

**Endpoint**: `GET /api/v0/equity/account/cash`

Retrieves account cash balance information.

**Request**:
```http
GET /api/v0/equity/account/cash HTTP/1.1
Host: demo.trading212.com
Authorization: Basic <base64_encoded_credentials>
Content-Type: application/json
```

**Response** (200 OK):
```json
{
  "free": 10000.00,
  "total": 10000.00,
  "ppl": 0.00,
  "result": 10000.00,
  "cash": 10000.00
}
```

**Response Fields**:
- `free`: Available cash for trading
- `total`: Total account value
- `ppl`: Unrealised profit and loss (open positions)
- `result`: Realised profit and loss (closed positions)
- `cash`: Cash balance

**Error Responses**:
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: API key doesn't have required permissions
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Other Account Endpoints

### Get Account Metadata

**Endpoint**: `GET /api/v0/equity/account/info`

**Expected Response**:
```json
{
  "currencyCode": "USD",
  "id": 12345
}
```

## Portfolio/Position Endpoints

### Get All Positions

**Endpoint**: `GET /api/v0/equity/portfolio`

Lists all open positions.

**Expected Response**:
```json
[
  {
    "code": "AAPL_US_EQ",
    "frontend": "AAPL",
    "quantity": 10.0,
    "averagePrice": 150.00,
    "currentPrice": 155.00,
    "ppl": 50.00
  }
]
```

## Rate Limiting

The Trading212 API implements rate limiting. Specific limits vary by endpoint and account type.

**Best Practices**:
- Implement exponential backoff on 429 responses
- Cache responses when appropriate
- Avoid polling - use webhooks when available

## Error Handling

All error responses follow this format:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error description"
}
```

## Notes

- API keys are environment-specific (demo vs live)
- All monetary values are in the account's base currency
- Timestamps are in ISO 8601 format
- The API may change - always refer to the official [Trading212 API docs](https://docs.trading212.com/api)

## Resources

- **Official API Documentation**: https://docs.trading212.com/api
- **How to Get API Key**: https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-Trading-212-API-key
- **API Environments**: https://docs.trading212.com/api/section/general-information/api-environments
