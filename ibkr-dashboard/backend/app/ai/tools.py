TOOLS = [
    {
        "name": "get_portfolio_summary",
        "description": "Get the user's current portfolio summary including net liquidation, cash, buying power, and PnL.",
        "input_schema": {"type": "object", "properties": {"account_id": {"type": "string"}}, "required": []},
    },
    {
        "name": "get_positions",
        "description": "List current open positions for an account.",
        "input_schema": {"type": "object", "properties": {"account_id": {"type": "string"}, "symbol_filter": {"type": "string"}}, "required": []},
    },
    {
        "name": "get_open_orders",
        "description": "List open (working) orders for an account.",
        "input_schema": {"type": "object", "properties": {"account_id": {"type": "string"}}, "required": []},
    },
    {
        "name": "search_contract",
        "description": "Search Interactive Brokers for a tradable instrument by symbol or name.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "sec_type": {"type": "string", "enum": ["STK", "OPT", "FUT", "CASH", "IND"]}}, "required": ["query"]},
    },
    {
        "name": "get_quote",
        "description": "Get a real-time bid/ask/last quote for a contract.",
        "input_schema": {"type": "object", "properties": {"conid": {"type": "integer"}, "symbol": {"type": "string"}, "sec_type": {"type": "string"}, "exchange": {"type": "string"}, "currency": {"type": "string"}}, "required": []},
    },
    {
        "name": "preview_order",
        "description": "Run a what-if analysis on a candidate order to see margin impact and commission. Does NOT place the order.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"}, "symbol": {"type": "string"}, "sec_type": {"type": "string", "enum": ["STK", "OPT", "FUT", "CASH", "IND"], "default": "STK"},
                "exchange": {"type": "string", "default": "SMART"}, "currency": {"type": "string", "default": "USD"},
                "side": {"type": "string", "enum": ["BUY", "SELL"]}, "quantity": {"type": "number", "minimum": 0},
                "order_type": {"type": "string", "enum": ["MKT", "LMT"]}, "limit_price": {"type": "number"}, "tif": {"type": "string", "enum": ["DAY", "GTC", "IOC"], "default": "DAY"},
            },
            "required": ["symbol", "side", "quantity", "order_type"],
        },
    },
    {
        "name": "stage_order",
        "description": "Stage an order for the user to review and confirm in the UI. The order is NOT submitted to IBKR until the user clicks Confirm.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"}, "symbol": {"type": "string"}, "sec_type": {"type": "string", "enum": ["STK", "OPT", "FUT", "CASH", "IND"], "default": "STK"},
                "exchange": {"type": "string", "default": "SMART"}, "currency": {"type": "string", "default": "USD"},
                "side": {"type": "string", "enum": ["BUY", "SELL"]}, "quantity": {"type": "number", "minimum": 0},
                "order_type": {"type": "string", "enum": ["MKT", "LMT"]}, "limit_price": {"type": "number"},
                "tif": {"type": "string", "enum": ["DAY", "GTC", "IOC"], "default": "DAY"}, "rationale": {"type": "string"},
            },
            "required": ["symbol", "side", "quantity", "order_type"],
        },
    },
    {
        "name": "cancel_order",
        "description": "Cancel an existing open order by id.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
]
