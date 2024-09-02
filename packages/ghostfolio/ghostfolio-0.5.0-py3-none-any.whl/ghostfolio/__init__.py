import logging
from datetime import datetime, timedelta

import requests
from requests.exceptions import HTTPError


class Ghostfolio:
    """Ghostfolio API client."""

    def __init__(self, token: str, host: str = "https://ghostfol.io/"):
        self.host = host
        self.token = token
        self._jwt_token: str | None = None
        self._jwt_token_expiry: datetime | None = None

    def _refresh_jwt_token(self):
        if self._jwt_token is not None and self._jwt_token_expiry < datetime.now():
            return

        self._jwt_token = self._process_response(
            requests.post(
                f"{self.host}/api/v1/auth/anonymous/", {"accessToken": self.token}
            )
        )["authToken"]
        self._jwt_token_expiry = datetime.now() + timedelta(days=30)

    def _get(self, endpoint: str, params=None, api_version: str = "v1"):
        self._refresh_jwt_token()

        return self._process_response(
            requests.get(
                f"{self.host}/api/{api_version}/{endpoint}/",
                headers={"Authorization": f"Bearer {self._jwt_token}"},
                params=params,
            )
        )

    def post(self, endpoint: str, data=None, api_version: str = "v1", object_id: str = None):
        self._refresh_jwt_token()

        return self._process_response(
            requests.post(
                f"{self.host}/api/{api_version}/{endpoint}/" + (object_id + "/" if object_id else ""),
                headers={"Authorization": f"Bearer {self._jwt_token}"},
                json=data,
            )
        )

    @staticmethod
    def _process_response(resp):
        try:
            resp.raise_for_status()
        except HTTPError as http_err:
            logging.error(resp.text)
            raise http_err

        return resp.json()

    def orders(self, account_id: str | None = None) -> dict:
        """Get all orders."""
        params = {"accounts": account_id} if account_id else None
        return self._get("order", params=params)

    def performance(self, date_range: str = "max") -> dict:
        return self._get(
            "portfolio/performance", params={"range": date_range}, api_version="v2"
        )

    def holdings(self, date_range: str = "max") -> dict:
        return self._get("portfolio/holdings", params={"range": date_range})

    def position(self, data_source: str, symbol: str):
        """Get position for a symbol from a data source."""
        return self._get(f"portfolio/position/{data_source}/{symbol}")

    def import_transactions(self, data: dict):
        """Import transactions."""
        self.post("import", data)

    def details(self) -> dict:
        """Get all details, including accounts, positions, and summary."""
        return self._get("portfolio/details")

    def investments(self, group_by: str = "month", date_range: str = "max") -> dict:
        """Get investments grouped by period."""
        return self._get(
            "portfolio/investments", params={"range": date_range, "groupBy": group_by}
        )

    def dividends(self, group_by: str = "month", date_range: str = "max") -> dict:
        """Get dividends grouped by period."""
        return self._get(
            "portfolio/dividends", params={"range": date_range, "groupBy": group_by}
        )

    def accounts(self) -> dict:
        return self._get("account")

    def market_data_admin(self) -> dict:
        """Overview of market data loaded"""
        return self._get("admin/market-data")

    def market_data(self, data_source: str, symbol: str):
        """Get market data for a symbol from a data source."""
        return self._get(f"admin/market-data/{data_source}/{symbol}")

    def __hash__(self) -> int:
        return hash((self.token, self.host))

    def __repr__(self):
        return f"Ghostfolio(host={self.host})"
