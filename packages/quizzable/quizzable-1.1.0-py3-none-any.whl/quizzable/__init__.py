"""# quizzable
`quizzable` provides an easy-to-implement interface to build a framework for
educational quiz apps built on top of Python. The `quizzable` library allows
you to create quizzes consisting of MCQ, FRQ, True-or-false, or Matching
questions, allowing you to build educational apps that leverage the power of
Python with great ease.
## Classes
* `Terms`: a list of terms
* `Quiz`: quiz object
* `Question`: question object
* `MCQQuestion`: MCQ-format question object
* `FRQQuestion`: FRQ-format question object
* `TrueFalseQuestion`: True-or-false format question object
* `MatchQuestion`: matching format question object
## Exceptions
* `BaseQuizzableException`: base exception for `quizzable` errors
* `InvalidLengthError`: quiz length is invalid
* `InvalidOptionsError`: number of options (for MCQs) is invalid
* `InvalidTermsError`: number of terms (for matching questions) is invalid
* `InvalidQuestionError`: type of question (for random questions) is invalid
* `DataIncompleteError`: data used to reconstruct a `Question` object is incomplete
"""

import random as _random
from copy import deepcopy as _deepcopy
from typing import Union as _Union

from . import exceptions as _exceptions


class Question:
    """A generic question object with a term, answer, and type.

    ## Parameters
    * `_type`: question type
    * `term`: question term
    * `answer`: question answer
    * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
    * `**kwargs`: other question data (e.g. `options`, `definition`, etc.)
    """

    def __init__(
        self,
        _type: str,
        term: _Union[str, list],
        answer: _Union[str, bool],
        prompt="{term}",
        **kwargs
    ):
        self._type = _type
        self.term = term
        self.answer = answer
        prompt_term = term
        if type(term) is list:
            prompt_term = ", ".join(term)
        self.prompt = prompt.format(term=prompt_term)
        self._data = {
            "_type": _type,
            "term": term,
            "answer": answer,
            "prompt": self.prompt,
            **kwargs,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Returns a reconstructed `Question` object made from `data`.

        ## Parameters
        * `data`: dictionary containing question data.
        """
        data_copy = _deepcopy(data)
        try:
            _type = data_copy.pop("_type")
            term = data_copy.pop("term")
            answer = data_copy.pop("answer")
            return cls(_type, term, answer, **data_copy)
        except KeyError as e:
            raise _exceptions.DataIncompleteError(e.args[0])

    def check_answer(self, answer: _Union[str, bool]):
        """Check if `answer` matches the question's answer."""
        return self.answer == answer, self.answer

    def to_dict(self):
        """Returns a dictionary representation of the question."""
        return self._data


class MCQQuestion(Question):
    """Representation of an MCQ-format question.
    ## Parameters
    * `term`: question term
    * `options`: question options
    * `answer`: question answer
    * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
    The dictionary representation returned by the `to_dict` method of an
    `MCQQuestion` object looks like this:
    ```py
    {
        "_type": "mcq",
        "term": "term",
        "options": {
            "option1": False,
            "option2": False,
            "option3": True,
            "option4": False,
        },
        "answer": "answer",
        "prompt": "term"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to choose a term's definition or vice/versa.
    * `options` is the list of potential answer choices.
    * `answer` is correct choice out of `options`.
    """

    def __init__(self, term: str, options: list[str], answer: str, prompt="{term}"):
        super().__init__("mcq", term, answer, prompt, options=options)
        self.options = options


class FRQQuestion(Question):
    """Representation of an FRQ-format question.
    ## Parameters
    * `term`: question term
    * `answer`: question answer
    * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
    The dictionary representation returned by the `to_dict` method of an
    `FRQQuestion` object looks like this:
    ```py
    {
        "_type": "frq",
        "term": "term",
        "answer": "answer",
        "prompt": "term"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to define a term's definition or vice/versa.
    * `answer` is the response that will be accepted as correct given the user's prompt.
    """

    def __init__(self, term: str, answer: str, prompt="{term}"):
        super().__init__("frq", term, answer, prompt)


class TrueFalseQuestion(Question):
    """Representation of a True-or-false format question.
    ## Parameters
    * `term`: question term
    * `definition`: question definition (what the user has to determine is True or False)
    * `answer`: question answer
    * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
    The dictionary representation returned by the `to_dict` method of a
    `TrueFalseQuestion` object looks like this:
    ```py
    {
        "_type": "tf",
        "term": "term",
        "definition": "definition",
        "answer": "answer",
        "prompt": "term"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to select True
    or False if the definition given matches with a specific term, or vice/versa.
    * `definition` is what the user has to determine is True or False.
    * `answer` is the actual definition that matches with the given `prompt`, or term.
    """

    def __init__(self, term: str, definition: str, answer: bool, prompt="{term}"):
        super().__init__("tf", term, answer, prompt, definition=definition)
        self.definition = definition


class MatchQuestion(Question):
    """Representation of a matching format question.
    ## Parameters
    * `term`: question term
    * `definitions`: question definitions (what the user has to match with the terms)
    * `answer`: question answer
    * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
    The dictionary representation returned by the `to_dict` method of a
    `MatchQuestion` object looks like this:
    ```py
    {
        "_type": "match",
        "term": [
            "term1",
            "term2",
            "term3",
            "term4"
        ],
        "definitions": [
            "definition4",
            "definition2",
            "definition1",
            "definition3",
        ],
        "answer": {
            "term1": "definition1",
            "term2": "definition2",
            "term3": "definition3",
            "term4": "definition4"
        },
        "prompt": "term"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to match the
    term with the definition, or vice/versa.
    * `definitions` is what the user has to match with the corresponding terms.
    * `answer` maps the terms `term` to their actual definitions `definitions`.
    """

    def __init__(
        self, term: str, definitions: list[str], answer: dict[str, str], prompt="{term}"
    ):
        super().__init__("match", term, answer, prompt, definitions=definitions)
        self.definitions = definitions


class Quiz:
    """An arbitrary quiz object."""

    def __init__(self, questions):
        self.questions = questions
        self._data = [q.to_dict() for q in self.questions]

    @classmethod
    def from_data(cls, data: list):
        """Reconstructs a `Quiz` object from a listlike representation.

        ## Parameters
        * `data`: list containing quiz data.
        """
        questions = []
        for question in data:
            questions.append(Question.from_dict(question))
        return cls(questions)

    def to_data(self):
        """Returns a listlike representation of the quiz, with each `Question`
        object being represented as its dictionary representation. For example,
        it could look like this:
        ```py
        [
            {
                "_type": "tf",
                "term": "la iglesia",
                "definition": "shop",
                "answer": "church",
                "prompt": "la iglesia"
            },
            {
                "_type": "mcq",
                "term": "la playa",
                "options": {
                    "beach": True,
                    "park": False,
                    "downtown": False,
                    "museum": False,
                },
                "prompt": "la playa"
            },
            {
                "_type": "frq",
                "term": "park",
                "answer": "el parque",
                "prompt": "park"
            }
        ]
        ```
        """
        return self._data


def _get_term_and_def(terms, term, answer_with="def"):
    """(for internal package use) retrieve a term and definition based on `answer_with`."""
    reverse = False
    if answer_with == "both":
        reverse = _random.random() < 0.5
    elif answer_with == "term":
        reverse = True
    if reverse:
        return terms[term], term
    return term, terms[term]


def _get_random_terms(terms, n_terms=1):
    """(for internal package use) retrieve `n_terms` terms from `terms`."""
    terms_copy = _deepcopy(terms)
    random_terms = []
    for i in range(n_terms):
        possible_terms = list(terms_copy.keys())
        try:
            random_term = _random.choice(possible_terms)
        except IndexError:
            return
        random_terms.append(random_term)
        del terms_copy[random_term]
    return random_terms


class Terms:
    """A list of terms.

    Should be a dictionary mapping _terms_ to _definitions_, where in this case
    a _term_ represents a question or vocabulary term, and a _definition_ is
    used to refer to the answer or vocabulary definition. For example, here is
    a list of terms in which each term is an English word, and its definition
    is its English translation:
    ```py
    {
        "painter": "la pintura",
        "brush": "el pincel",
        "sculpture": "la escultura",
        "palette:": "la paleta",
        "self-portrait": "el autorretrato",
        "abstract": "abstracto/a"
    }
    ```
    ## Functions
    * `to_dict`: get a dictionary representation of `self`
    * `get_terms`: get a modified list of `self`
    * `get_frq_question`: get a random FRQ question based on `self`
    * `get_mcq_question`: get a random MCQ question based on `self`
    * `get_true_false_question`: get a random True-or-false question based on `self`
    * `get_match_question`: get a random matching question based on `self`
    * `get_quiz`: get a quiz consisting of different types of questions randomly generated from `self`
    """

    def __init__(self, data: dict[str, str]):
        self._data = data

    def to_dict(self):
        return self._data

    def __getitem__(self, term):
        return self._data[term]

    def __setitem__(self, term, definition):
        self._data[term] = definition

    def __delitem__(self, term):
        del self._data[term]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def get_terms(self, answer_with="def"):
        """Returns the dictionary `terms` modified based on the value for `answer_with`.

        ## Parameters
        * `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered.
        """
        terms_copy = _deepcopy(self._data)
        for term in self:
            new_term, new_def = _get_term_and_def(self._data, term, answer_with)
            terms_copy[new_term] = new_def
        return Terms(terms_copy)

    def get_frq_question(self, prompt="{term}", **kwargs):
        """Returns an `FRQQuestion` object with a random FRQ-format question generated from `terms`.

        ## Parameters
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        """
        term = _get_random_terms(self._data)
        return FRQQuestion(term=term[0], answer=self[term[0]], prompt=prompt)

    def get_mcq_question(self, n_options=4, prompt="{term}", **kwargs):
        """Returns an `MCQQuestion` object with a random MCQ-format question generated from `terms`.

        ## Parameters
        * `n_options = 4`: number of options per question.
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        """
        if (not n_options) or (n_options > len(self)):
            raise _exceptions.InvalidOptionsError(n_options)

        options = _get_random_terms(self._data, n_options)
        term = _random.choice(options)
        answer_choices = [self[option] for option in options]
        return MCQQuestion(
            term=term, options=answer_choices, answer=self[term], prompt=prompt
        )

    def get_true_false_question(self, prompt="{term}", **kwargs):
        """Returns a `TrueFalseQuestion` object with a random True-or-false format question generated from `terms`.

        ## Parameters
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        """
        term = _get_random_terms(self._data, 2)
        definition, answer = self[term[0]], True
        if _random.random() < 0.5:
            definition, answer = self[term[1]], False
        return TrueFalseQuestion(
            term=term[0], definition=definition, answer=answer, prompt=prompt
        )

    def get_match_question(self, n_terms=5, prompt="{term}", **kwargs):
        """Returns a `MatchQuestion` object with a matching format question generated from `terms`.

        ## Parameters
        * `n_terms = 5`: how many terms have to be matched.
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        """
        if (not n_terms) or (n_terms > len(self)):
            raise _exceptions.InvalidTermsError(n_terms)

        term = _get_random_terms(self._data, n_terms)
        definitions = []
        for t in term:
            definitions.append(self[t])
        answer = dict(zip(term, definitions))
        _random.shuffle(definitions)
        return MatchQuestion(
            term=term, definitions=definitions, answer=answer, prompt=prompt
        )

    def get_random_question(
        self,
        types=["mcq", "frq", "tf"],
        n_options=4,
        n_terms=5,
        prompt="{term}",
        prompts: dict = {},
    ):
        """Returns a `Question` object of a random-format question generated from `terms`.

        ## Parameters
        * `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`;
        types of questions that appear on the quiz.
        * `n_options = 4`: (if MCQs are involved) number of options per MCQ question.
        * `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question.
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        * `prompts = {}`: prompt map to define specific prompts for specific questions
        """
        quiz_types = {
            "mcq": self.get_mcq_question,
            "frq": self.get_frq_question,
            "tf": self.get_true_false_question,
            "match": self.get_match_question,
        }
        try:
            question_type = _random.choice(types)
            if question_type in prompts:
                prompt = prompts[question_type]
            get_question = quiz_types[question_type]
        except KeyError as e:
            raise _exceptions.InvalidQuestionError(e.args[0])
        return get_question(prompt=prompt, n_options=n_options, n_terms=n_terms)

    def get_quiz(
        self,
        types: list[str] = ["mcq", "frq", "tf"],
        length=10,
        answer_with="def",
        n_options=4,
        n_terms=5,
        prompt="{term}",
        prompts: dict = {},
    ):
        """Returns a `Quiz` object with random questions based on the parameters below.

        ## Parameters
        * `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`;
        types of questions that appear on the quiz.
        * `length = 10`: number of questions on quiz.
        * `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered.
        * `n_options = 4`: (if MCQs are involved) number of options per MCQ question.
        * `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question.
        * `prompt = "{term}"`: question prompt (use `"{term}"` to reference question term in custom prompts)
        * `prompts = {}`: prompt map to define specific prompts for specific questions
        """
        if (not length) or (length > len(self)):
            raise _exceptions.InvalidLengthError(length)

        questions = []
        terms_copy = self.get_terms(answer_with)
        for i in range(length):
            question = terms_copy.get_random_question(
                types,
                n_options=n_options,
                n_terms=n_terms,
                prompt=prompt,
                prompts=prompts,
            )
            questions.append(question)
            if type(question.term) is list:
                for t in question.term:
                    del terms_copy[t]
            else:
                del terms_copy[question.term]
            if (len(terms_copy) < n_terms) or (len(terms_copy) < n_options):
                terms_copy = self.get_terms(answer_with)
        return Quiz(questions)
