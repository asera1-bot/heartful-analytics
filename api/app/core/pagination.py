from fastapi import Query


def pagination_params(
    limit: int = Query(50, ge=1, le=200, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    return limit, offset
