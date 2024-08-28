SOCIAL_INTELLIGENCE_DB_SECRET_ID = "social-intelligence-db"
QUICK_INTEL_API_KEY_SECRET_ID = "quick-intel-api-key"

HONEYPOT_FINDER_URL = "https://api.honeypot.is/legacy/aws/isHoneypot?chain={chain_id}&token={token_id}"
GO_PLUS_URL = "https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={token_id}"
GET_QUICK_AUDIT_URL = "https://api.quickintel.io/v1/getquickiauditfull"

INSERT_OR_UPDATE_ETH_SECURITY_DATA_QUERY = """
INSERT INTO social.token_properties 
(token_id, is_honeypot, sell_tax, buy_tax, holders_count, token_creator, owner_addr, 
lp_lock_percentage, lp_unlock_date, updated_by, is_contract_verified)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
is_honeypot=COALESCE(VALUES(is_honeypot), is_honeypot),
sell_tax=COALESCE(VALUES(sell_tax), sell_tax), 
buy_tax=COALESCE(VALUES(buy_tax), buy_tax),
holders_count=COALESCE(VALUES(holders_count), holders_count),
token_creator=COALESCE(VALUES(token_creator), token_creator),
owner_addr=COALESCE(VALUES(owner_addr), owner_addr),
lp_lock_percentage=COALESCE(VALUES(lp_lock_percentage), lp_lock_percentage),
lp_unlock_date=COALESCE(VALUES(lp_unlock_date), lp_unlock_date),
is_contract_verified=COALESCE(VALUES(is_contract_verified), is_contract_verified),
updated_by=VALUES(updated_by)
"""

UPDATE_OTHER_CHAIN_SECURITY_DATA_QUERY = """
UPDATE blockchains.tokens
SET 
    is_honeypot = COALESCE(%s, is_honeypot), 
    sell_tax = COALESCE(%s, sell_tax), 
    buy_tax = COALESCE(%s, buy_tax),
    lp_burned = COALESCE(%s, lp_burned), 
    is_scam = COALESCE(%s, is_scam), 
    can_burn = COALESCE(%s, can_burn), 
    can_mint = COALESCE(%s, can_mint),
    can_freeze = COALESCE(%s, can_freeze), 
    holders_count = COALESCE(%s, holders_count), 
    contract_creator = COALESCE(%s, contract_creator), 
    contract_owner = COALESCE(%s, contract_owner), 
    lp_lock_percentage = COALESCE(%s, lp_lock_percentage), 
    lp_unlock_date = COALESCE(%s, lp_unlock_date), 
    security_updated_at = %s,
    security_updated_by = %s,
    is_contract_verified = COALESCE(%s, is_contract_verified) 
WHERE address = %s
"""

CHAIN_TO_ID_MAP = {
    "ethereum": 1,
    "optimism": 10,
    "cronos": 25,
    "bsc": 56,
    "okex-chain": 66,
    "okt chain": 66,
    "gnosis": 100,
    "heco": 128,
    "polygon": 137,
    "fantom": 250,
    "kucoin": 321,
    "kcc": 321,
    "kucoin token": 321,
    "zksync": 324,
    "ethw": 10001,
    "fon": 201022,
    "arbitrum": 42161,
    "arbitrum-nova": 42161,
    "arbitrum-one": 42161,
    "avalanche": 43114,
    "linea": 59144,
    "base": 8453,
    "tron": "tron",
    "scroll": 534352,
    "solana": "solana",
    "eth": "eth",
    "core": "core",
    "polygonzkevm": "polygonzkevm",
    "loop": "loop",
    "kava": "kava",
    "metis": "metis",
    "astar": "astar",
    "oasis": "oasis",
    "iotex": "iotex",
    "conflux": "conflux",
    "canto": "canto",
    "energi": "energi",
    "velas": "velas",
    "grove": "grove",
    "pulse": "pulse",
    "besc": "besc",
    "shibarium": "shibarium",
    "opbnb": "opbnb",
    "bitrock": "bitrock",
    "mantle": "mantle",
    "lightlink": "lightlink",
    "klaytn": "klaytn",
    "injective": "injective",
    "radix": "radix",
    "sui": "sui",
    "manta": "manta",
    "zeta": "zeta"
}

ID_TO_CHAIN_MAP = {
    1: "eth",
    10: "optimism",
    25: "cronos",
    56: "bsc",
    100: "gnosis",
    128: "heco",
    137: "polygon",
    250: "fantom",
    324: "zksync",
    10001: "ethw",
    201022: "fon",
    42161: "arbitrum",
    43114: "avalanche",
    59144: "linea",
    8453: "base",
    534352: "scroll",
    "solana": "solana",
    "eth": "eth",
    "arbitrum": "arbitrum",
    "bac": "bsc",
    "polygon": "polygon",
    "fantom": "fantom",
    "avalanche": "avalanche",
    "core": "core",
    "zksync": "zksync",
    "polygonzkevm": "polygonzkevm",
    "loop": "loop",
    "kava": "kava",
    "metis": "metis",
    "astar": "astar",
    "oasis": "oasis",
    "iotex": "iotex",
    "conflux": "conflux",
    "canto": "canto",
    "energi": "energi",
    "velas": "velas",
    "grove": "grove",
    "pulse": "pulse",
    "besc": "besc",
    "linea": "linea",
    "base": "base",
    "shibarium": "shibarium",
    "opbnb": "opbnb",
    "bitrock": "bitrock",
    "optimism": "optimism",
    "mantle": "mantle",
    "lightlink": "lightlink",
    "klaytn": "klaytn",
    "injective": "injective",
    "radix": "radix",
    "sui": "sui",
    "manta": "manta",
    "zeta": "zeta",
}
