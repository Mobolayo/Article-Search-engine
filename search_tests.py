from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

	##############
	# UNIT TESTS #
	##############

	def test_example_unit_test(self):
		dummy_keyword_dict = {
			'cat': ['title1', 'title2', 'title3'],
			'dog': ['title3', 'title4']
		}
		expected_search_results = ['title3', 'title4']
		self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

	def test_keyword_to_titles(self):
		metadata = [
			['Vogue', 'Anna Wintour', 226432972367, 17, ['met', 'gala', 'drama', 'party']], 
			['OpenAI', 'Sam Altman', 1675629067, 13, ['chat', 'work', 'learn']],
			['Documetary', 'Mobolayo', 902736367, 20, ['drama', 'party', 'money', 'learn']]
		]
		metadata2 = [
			['Vogue', 'Anna Wintour', 226432972367, 17, []], 
			['OpenAI', 'Sam Altman', 1675629067, 13, []],
			['Documetary', 'Mobolayo', 902736367, 20, []]
		]
		expected = {
			'met': ['Vogue'],
			'gala': ['Vogue'],
			'drama': ['Vogue', 'Documetary'],
			'chat': ['OpenAI'],
			'work': ['OpenAI'],
			'money': ['Documetary'],
			'party': ['Vogue', 'Documetary'],
			'learn': ['OpenAI', 'Documetary']
		}
		self.assertEqual(keyword_to_titles(metadata), expected)
		self.assertEqual(keyword_to_titles(metadata2), {})
		self.assertEqual(keyword_to_titles([[]]), {})

	def test_title_to_info(self):
		metadata = [
			['Vogue', 'Anna Wintour', 226432972367, 17, ['met', 'gala', 'drama', 'party']], 
			['OpenAI', 'Sam Altman', 1675629067, 13, ['chat', 'work', 'learn']],
			['Documetary', 'Mobolayo', 902736367, 20, ['drama', 'party', 'money', 'learn']]
		]
		metadata2 = [
			['Vogue', 'Anna Wintour', 226432972367, 17, []], 
			['OpenAI', 'Sam Altman', 1675629067, 13, []],
			['Documetary', 'Mobolayo', 902736367, 20, []]
		]
		metadata3 = [
			['', 'Anna Wintour', 226432972367, 17, []], 
			['OpenAI', '', 1675629067, 13, []],
			['', '', 902736367, 20, []]
		]
		expected = {
			'Vogue': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': 'Sam Altman', 'timestamp': 1675629067, 'length': 13},
			'Documetary': {'author': 'Mobolayo','timestamp': 902736367, 'length': 20}
		}
		expected2 = {
			'': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': '', 'timestamp': 1675629067, 'length': 13},
			'': {'author': '','timestamp': 902736367, 'length': 20}
		}
		self.assertEqual(title_to_info(metadata), expected)
		self.assertEqual(title_to_info([[]]), {})
		self.assertEqual(title_to_info(metadata2), expected)
		self.assertEqual(title_to_info(metadata3), expected2)

	def test_search(self):
		keyword_to_titles = {
			'met': ['Vogue'],
			'gala': ['Vogue'],
			'drama': ['Vogue', 'Documetary'],
			'chat': ['OpenAI'],
			'work': ['OpenAI'],
			'money': ['Documetary'],
			'party': ['Vogue', 'Documetary'],
			'learn': ['OpenAI', 'Documetary']
		}
		self.assertEqual(search('dRamA', keyword_to_titles), [])
		self.assertEqual(search('drama', keyword_to_titles), keyword_to_titles['drama'])
		self.assertEqual(search('house', keyword_to_titles), [])
		self.assertEqual(search('', keyword_to_titles), [])
		self.assertEqual(search('baby', []), [])

	def test_article_length(self):
		article_titles = ['Vogue', 'OpenAI', 'Documetary']
		title_to_info = {
			'Vogue': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': 'Sam Altman', 'timestamp': 1675629067, 'length': 13},
			'Documetary': {'author': 'Mobolayo','timestamp': 902736367, 'length': 20},
			'The Economist': {'author': 'Andrea','timestamp': 90286367, 'length': 27}
		}
		self.assertEqual(article_length(5, article_titles, title_to_info), [])
		self.assertEqual(article_length(25, article_titles, title_to_info), ['Vogue', 'OpenAI', 'Documetary'])
		self.assertEqual(article_length(30, article_titles, title_to_info), ['Vogue', 'OpenAI', 'Documetary'])
		self.assertEqual(article_length(15, article_titles, title_to_info), ['OpenAI'])

	def test_key_by_author(self):
		article_titles = ['Vogue', 'OpenAI', 'Documetary', 'The Economist']
		title_to_info = {
			'Vogue': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': 'Sam Altman', 'timestamp': 1675629067, 'length': 13},
			'Documetary': {'author': 'Mobolayo','timestamp': 902736367, 'length': 20},
			'The Economist': {'author': 'Sam Altman','timestamp': 90286367, 'length': 27},
			'Crypto News': {'author': 'Zhang', 'timestamp': 1683084767, 'length': 13}
		}
		expected = {
			'Anna Wintour': ['Vogue'],
			'Sam Altman': ['OpenAI', 'The Economist'],
			'Mobolayo': ['Documetary']
		}
		self.assertEqual(key_by_author(article_titles, title_to_info), expected)
		self.assertEqual(key_by_author([], title_to_info), {})
		self.assertEqual(key_by_author(article_titles, []), {})
		self.assertEqual(key_by_author([], []), {})

	def test_filter_to_author(self):
		article_titles = ['Vogue', 'OpenAI', 'Documetary', 'The Economist']
		title_to_info = {
			'Vogue': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': 'Sam Altman', 'timestamp': 1675629067, 'length': 13},
			'Documetary': {'author': 'Mobolayo','timestamp': 902736367, 'length': 20},
			'The Economist': {'author': 'Sam Altman','timestamp': 90286367, 'length': 27},
			'Crypto News': {'author': 'Sam Altman', 'timestamp': 1683084767, 'length': 13}
		}
		self.assertEqual(filter_to_author('Mariam', article_titles, title_to_info), [])
		self.assertEqual(filter_to_author('Sam Altman', [], title_to_info), [])
		self.assertEqual(filter_to_author('', article_titles, title_to_info), ['Vogue', 'OpenAI', 'Documetary', 'The Economist'])
		self.assertEqual(filter_to_author('Sam', article_titles, title_to_info), ['OpenAI', 'The Economist'])
		self.assertEqual(filter_to_author('Sam Altman', article_titles, title_to_info), ['OpenAI', 'The Economist'])
       
	def test_filter_out(self):
		article_titles = ['Vogue', 'OpenAI', 'Documetary']
		keyword_info = {
			'met': ['Vogue'],
			'gala': ['Vogue'],
			'drama': ['Vogue', 'Documetary'],
			'chat': ['OpenAI'],
			'work': ['OpenAI'],
			'money': ['Documetary'],
			'party': ['Vogue', 'Documetary'],
			'learn': ['OpenAI', 'Documetary']
		}
		self.assertEqual(filter_out('party', [], title_to_info), [])
		self.assertEqual(filter_out('madam', [], title_to_info), [])
		self.assertEqual(filter_out('Mariam', article_titles, keyword_info), ['Vogue', 'OpenAI', 'Documetary'])
		self.assertEqual(filter_out('madam', article_titles, keyword_info), ['Vogue', 'OpenAI', 'Documetary'])
		self.assertEqual(filter_out('drama', article_titles, keyword_info), ['OpenAI'])

	def test_articles_from_year(self):
		article_titles = ['Vogue', 'OpenAI', 'Documetary', 'The Economist', 'Crypto News']
		title_to_info = {
			'Vogue': {'author': 'Anna Wintour', 'timestamp': 226432972367, 'length': 17},
			'OpenAI': {'author': 'Sam Altman', 'timestamp': 1175629067, 'length': 13},
			'Documetary': {'author': 'Mobolayo','timestamp': 902736367, 'length': 20},
			'The Economist': {'author': 'Sam Altman','timestamp': 90286367, 'length': 27},
			'Crypto News': {'author': 'Sam Altman', 'timestamp': 1183084767, 'length': 13}
		}
		self.assertEqual(articles_from_year(2006, [], title_to_info), [])
		self.assertEqual(articles_from_year(2023, article_titles, title_to_info), [])
		self.assertEqual(articles_from_year(2007, article_titles, title_to_info), ['OpenAI', 'Crypto News'])

	#####################
	# INTEGRATION TESTS #
	#####################

	@patch('builtins.input')
	def test_example_integration_test(self, input_mock):
		keyword = 'soccer'
		advanced_option = 5
		advanced_response = 2009

		output = get_print(input_mock, [keyword, advanced_option, advanced_response])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

		self.assertEqual(output, expected)

	@patch('builtins.input')
	def test_integration_title_to_info(self, input_mock):
		keyword = 'soccer'
		advanced_option = 6

		output = get_print(input_mock, [keyword, advanced_option])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

		self.assertEqual(output, expected)

	@patch('builtins.input')
	def test_integration_article_length(self, input_mock):
		keyword = 'soccer'
		advanced_option = 1
		advanced_response = 3500

		output = get_print(input_mock, [keyword, advanced_option, advanced_response])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

		self.assertEqual(output, expected)

	@patch('builtins.input')
	def test_integration_key_by_author(self, input_mock):
		keyword = 'dog'
		advanced_option = 2

		output = get_print(input_mock, [keyword, advanced_option])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: {'Pegship': ['Black dog (ghost)'], 'Mack Johnson': ['Mexican dog-faced bat'], 'Mr Jake': ['Dalmatian (dog)', 'Sun dog'], 'Jack Johnson': ['Guide dog']}\n"

		self.assertEqual(output, expected)

	@patch('builtins.input')
	def test_integration_filter_to_author(self, input_mock):
		keyword = 'dog'
		advanced_option = 3
		advanced_response = 'Jack'

		output = get_print(input_mock, [keyword, advanced_option, advanced_response])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Guide dog']\n"

		self.assertEqual(output, expected)

	@patch('builtins.input')
	def test_integration_filter_out(self, input_mock):
		keyword = 'pop'
		advanced_option = 4
		advanced_response = 'dog'

		output = get_print(input_mock, [keyword, advanced_option, advanced_response])
		expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['List of Canadian musicians', 'French pop music', '2009 in music', 'Rock music', 'Arabic music']\n"

		self.assertEqual(output, expected)
# Write tests above this line. Do not remove.
if __name__ == "__main__":
	main()
