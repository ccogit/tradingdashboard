from app.schemas.contracts import ContractDTO
import logging

logger = logging.getLogger(__name__)


async def search_contracts(query: str, sec_type: str | None, ib_client) -> list[ContractDTO]:
    matches = await ib_client.ib.reqMatchingSymbolsAsync(query)
    results = []
    for m in (matches or []):
        c = m.contract
        if sec_type and c.secType != sec_type:
            continue
        results.append(ContractDTO(
            conid=c.conId,
            symbol=c.symbol,
            sec_type=c.secType,
            exchange=c.primaryExch or "SMART",
            primary_exchange=c.primaryExch,
            currency=c.currency,
            local_symbol=c.localSymbol,
            description=getattr(m, "companyName", None),
        ))
    return results[:20]


async def get_contract(conid: int, ib_client) -> ContractDTO:
    from ib_async import Contract
    contract = Contract(conId=conid)
    contracts = await ib_client.ib.qualifyContractsAsync(contract)
    if not contracts:
        from app.exceptions import ContractNotFound
        raise ContractNotFound(str(conid))
    c = contracts[0]
    return ContractDTO(
        conid=c.conId,
        symbol=c.symbol,
        sec_type=c.secType,
        exchange=c.exchange or "SMART",
        primary_exchange=c.primaryExch,
        currency=c.currency,
        local_symbol=c.localSymbol,
    )
