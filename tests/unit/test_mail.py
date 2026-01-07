import pytest
from pytest_mock import MockFixture 
from src.personal_account import  Personal_Account
from src.company_account import Company_Account
from datetime import date

class TestMailSending:

    @pytest.fixture
    def today_date_str(self) -> str:
        return date.today().strftime("%Y-%m-%d")

    @pytest.fixture
    def mock_smtp_personal(self, mocker: MockFixture):
        mock_class = mocker.patch('src.personal_account.SMTPClient')
        return mock_class.return_value

    @pytest.fixture
    def mock_smtp_company(self, mocker: MockFixture):
        mock_class = mocker.patch('src.company_account.SMTPClient')
        return mock_class.return_value

    @pytest.fixture
    def mock_mf_api(self, mocker: MockFixture):
        mock_get = mocker.patch('src.company_account.requests.get')
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {"statusVat": "Czynny"},
                "requestId": "test-id"
            }
        }
        return mock_get

    def test_send_email_personal_account_success(self, mock_smtp_personal, today_date_str):
        email = "jan.kowalski@example.com"
        account = Personal_Account("Jan","Kowalski","12345678910")
        account.history = [100, -20, 50]
        mock_smtp_personal.send.return_value = True
        result = account.send_history_via_email(email)
        assert result is True
        expected_subject = f"Account Transfer History {today_date_str}"
        expected_body = f"Personal account history: [100, -20, 50]"
        mock_smtp_personal.send.assert_called_once_with(expected_subject, expected_body, email)

    def test_send_email_personal_account_failure(self, mock_smtp_personal):
        account = Personal_Account("Jan","Kowalski","12345678910")
        mock_smtp_personal.send.return_value = False
        result = account.send_history_via_email("fail@example.com")
        assert result is False

    def test_send_email_company_account_success(self, mock_mf_api, mock_smtp_company, today_date_str):
        email = "ceo@januszex.pl"
        account = Company_Account("Januszex", "1234567890")
        account.history = [10000, -500]
        mock_smtp_company.send.return_value = True
        result = account.send_history_via_email(email)
        assert result is True
        expected_subject = f"Account Transfer History {today_date_str}"
        expected_body = f"Company account history: [10000, -500]"
        mock_smtp_company.send.assert_called_once_with(expected_subject, expected_body, email)

    def test_send_email_company_account_failure(self, mock_mf_api, mock_smtp_company, today_date_str):
        account = Company_Account("Januszex", "1234567890")
        mock_smtp_company.send.return_value = False
        result = account.send_history_via_email("fail@example.com")
        assert result is False