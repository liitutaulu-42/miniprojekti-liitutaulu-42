import unittest
from unittest.mock import Mock, ANY, call

from transaction import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.database_handle = Mock()
        self.transaction = Transaction(self.database_handle)

    def test_initialize_with_no_transactions(self):
        self.database_handle.commit.assert_not_called()

    def test_insert_article_values_are_same(self):
        self.database_handle.create_entry.return_value = 1
        self.transaction.insert_article(
                author="Isaac Newton",
                title="Title of the Article",
                journal="A",
                year="2024",
            )

        self.database_handle.create_entry \
                .assert_called_once_with("article", "Isaac-Title-2024")
        self.database_handle.add_field.assert_has_calls([
            call(1, "author", "Isaac Newton"),
            call(1, "title", "Title of the Article"),
            call(1, "journal", "A"),
            call(1, "year", "2024"),
        ], any_order=True)
        self.database_handle.commit.assert_called_once()

    def test_fail_author_syntax(self):
        with self.assertRaises(AssertionError):
            self.transaction.insert_article(
                    author="3",
                    title="Title of the Article",
                    journal="A",
                    year="2024",
                    )

    def test_insert_article_values_same_as_bibtex(self):
        self.database_handle.get_references.return_value = ((0, "testi"),)
        self.database_handle.get_fields_of.return_value = {
                "author": "Kirjoittaja Nimi",
                "journal": "J",
                "title": "Testi Otsikko",
                "year": "2024",
                }

        bibtex = self.transaction.get_bibtex()

        self.assertIn("@article{testi,", bibtex)
        self.assertIn("author = {Kirjoittaja Nimi}", bibtex)
        self.assertIn("title = {Testi Otsikko}", bibtex)
        self.assertIn("journal = {J}", bibtex)
        self.assertIn("year = 2024", bibtex)
        self.assertIn(",\n\t", bibtex)
        self.assertIn("\n}", bibtex)
