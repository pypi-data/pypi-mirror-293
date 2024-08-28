import random
from typing import Any, Dict, List, Optional, Tuple, Union
from warnings import warn

from googletrans.constants import LANGUAGES

from ..core.transforms_interface import TextTransform
from ..corpora.types import Language, Text
from . import functional as F
from .utils import split_text_into_sentences


class AEDA(TextTransform):
    """Randomly inserts punctuation into the input text.

    Args:
        insertion_prob_range: The Range for probability of inserting a punctuation mark.
        punctuation: Punctuation to be inserted at random.
        p: The probability of applying this transform.

    References:
        https://arxiv.org/pdf/2108.13230.pdf
    """

    def __init__(
        self,
        insertion_prob_range: Tuple[float, float] = (0.0, 0.3),
        punctuation: Tuple[str, ...] = (".", ";", "?", ":", "!", ","),
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
        *,
        insertion_prob_limit: Optional[Union[float, Tuple[float, float]]] = None,
        punctuations: Optional[Tuple[str, ...]] = None,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        if insertion_prob_limit is not None:
            warn(
                "insertion_prob_limit is deprecated."
                " Use `insertion_prob_range` as tuple (lower limit, insertion_prob_limit) instead."
                " self.insertion_prob_range will be set to insertion_prob_limit.",
                DeprecationWarning,
                stacklevel=2,
            )
            insertion_prob_range = insertion_prob_limit  # type: ignore
        if not isinstance(insertion_prob_range, tuple):
            warn(
                "insertion_prob_range is should be a tuple with length 2."
                " The provided value will be automatically converted to a tuple (0, insertion_prob_range).",
                DeprecationWarning,
                stacklevel=2,
            )
            insertion_prob_range = (0.0, insertion_prob_range)
        if punctuations is not None:
            warn(
                "punctuations is deprecated. Use `punctuation` instead. self.punctuation will be set to punctuations.",
                DeprecationWarning,
                stacklevel=2,
            )
            punctuation = punctuations
        self._validate_transform_init_args(insertion_prob_range=insertion_prob_range, punctuation=punctuation)
        self.insertion_prob_range = insertion_prob_range
        self.punctuation = punctuation

    def _validate_transform_init_args(
        self, *, insertion_prob_range: Union[float, Tuple[float, float]], punctuation: Tuple[str, ...]
    ) -> None:
        if not isinstance(insertion_prob_range, (float, int, tuple)):
            raise TypeError(
                "insertion_prob_range must be a real number between 0 and 1 or a tuple with length 2. "
                f"Got: {type(insertion_prob_range)}"
            )
        if isinstance(insertion_prob_range, (float, int)):
            if not (0.0 <= insertion_prob_range <= 1.0):
                raise ValueError(
                    "If insertion_prob_range is a real number, "
                    f"it must be between 0 and 1. Got: {insertion_prob_range}"
                )
        elif isinstance(insertion_prob_range, tuple):
            if len(insertion_prob_range) != 2:
                raise ValueError(
                    f"If insertion_prob_range is a tuple, it's length must be 2. Got: {insertion_prob_range}"
                )
            if not (0.0 <= insertion_prob_range[0] <= insertion_prob_range[1] <= 1.0):
                raise ValueError(f"insertion_prob_range values must be between 0 and 1. Got: {insertion_prob_range}")
        if not isinstance(punctuation, tuple):
            raise TypeError(f"punctuation must be a tuple and all elements must be strings. Got: {type(punctuation)}")
        if not (punctuation and all(isinstance(punc, str) for punc in punctuation)):
            raise TypeError(f"All punctuation elements must be strings. Got: {punctuation}")

    def apply(self, text: Text, insertion_prob: float, **params: Any) -> Text:
        return F.insert_punctuation(text, insertion_prob, self.punctuation)

    def get_params(self) -> Dict[str, float]:
        return {"insertion_prob": random.uniform(self.insertion_prob_range[0], self.insertion_prob_range[1])}

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return ("insertion_prob_range", "punctuation")


class BackTranslation(TextTransform):
    """Back-translates the input text by translating it to the target language and then back to the original.

    Args:
        from_lang: The language of the input text.
        to_lang: The language to which the input text will be translated.
        p: The probability of applying this transform.
    """

    def __init__(
        self,
        from_lang: Language = "ko",
        to_lang: Language = "en",
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(from_lang=from_lang, to_lang=to_lang)
        self.from_lang = from_lang
        self.to_lang = to_lang

    def _validate_transform_init_args(self, *, from_lang: Language, to_lang: Language) -> None:
        if from_lang not in LANGUAGES:
            raise ValueError(f"from_lang must be one of ({list(LANGUAGES.keys())}). Got: {from_lang}")
        if to_lang not in LANGUAGES:
            raise ValueError(f"to_lang must be one of ({list(LANGUAGES.keys())}). Got: {to_lang}")

    def apply(self, text: Text, **params: Any) -> Text:
        return F.back_translate(text, self.from_lang, self.to_lang)

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return ("from_lang", "to_lang")


class RandomDeletion(TextTransform):
    """Randomly deletes words in the input text.

    Args:
        deletion_prob: The probability of deleting a word.
        min_words_per_sentence:
            If a `float`, it is the minimum proportion of words to retain in each sentence.
            If an `int`, it is the minimum number of words in each sentence.
        p: The probability of applying this transform.

    References:
        https://arxiv.org/pdf/1901.11196.pdf
    """

    def __init__(
        self,
        deletion_prob: float = 0.1,
        min_words_per_sentence: Union[float, int] = 0.8,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
        *,
        min_words_each_sentence: Optional[Union[float, int]] = None,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        if min_words_each_sentence is not None:
            warn(
                "min_words_each_sentence is deprecated. Use `min_words_per_sentence` instead."
                " self.min_words_per_sentence will be set to min_words_each_sentence.",
                DeprecationWarning,
                stacklevel=2,
            )
            min_words_per_sentence = min_words_each_sentence
        self._validate_transform_init_args(deletion_prob=deletion_prob, min_words_per_sentence=min_words_per_sentence)
        self.deletion_prob = deletion_prob
        self.min_words_per_sentence = min_words_per_sentence

    def _validate_transform_init_args(self, *, deletion_prob: float, min_words_per_sentence: Union[float, int]) -> None:
        if not isinstance(deletion_prob, (float, int)):
            raise TypeError(f"deletion_prob must be a real number between 0 and 1. Got: {type(deletion_prob)}")
        if not (0.0 <= deletion_prob <= 1.0):
            raise ValueError(f"deletion_prob must be between 0 and 1. Got: {deletion_prob}")
        if not isinstance(min_words_per_sentence, (float, int)):
            raise TypeError(
                f"min_words_per_sentence must be either an int or a float. Got: {type(min_words_per_sentence)}"
            )
        if isinstance(min_words_per_sentence, float):
            if not (0.0 <= min_words_per_sentence <= 1.0):
                raise ValueError(
                    f"If min_words_per_sentence is a float, it must be between 0 and 1. Got: {min_words_per_sentence}"
                )
        elif isinstance(min_words_per_sentence, int):
            if min_words_per_sentence < 0:
                raise ValueError(
                    f"If min_words_per_sentence is an int, it must be non negative. Got: {min_words_per_sentence}"
                )

    def apply(self, text: Text, **params: Any) -> Text:
        return F.delete_words(text, self.deletion_prob, self.min_words_per_sentence)

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return ("deletion_prob", "min_words_per_sentence")


class RandomDeletionSentence(TextTransform):
    """Randomly deletes sentences in the input text.

    Args:
        deletion_prob: The probability of deleting a sentence.
        min_sentences:
            If a `float`, it is the minimum proportion of sentences to retain in the text.
            If an `int`, it is the minimum number of sentences in the text.
        p: The probability of applying this transform.
    """

    def __init__(
        self,
        deletion_prob: float = 0.1,
        min_sentences: Union[float, int] = 0.8,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(deletion_prob=deletion_prob, min_sentences=min_sentences)
        self.deletion_prob = deletion_prob
        self.min_sentences = min_sentences

    def _validate_transform_init_args(self, *, deletion_prob: float, min_sentences: Union[float, int]) -> None:
        if not isinstance(deletion_prob, (float, int)):
            raise TypeError(f"deletion_prob must be a real number between 0 and 1. Got: {type(deletion_prob)}")
        if not (0.0 <= deletion_prob <= 1.0):
            raise ValueError(f"deletion_prob must be between 0 and 1. Got: {deletion_prob}")
        if not isinstance(min_sentences, (float, int)):
            raise TypeError(f"min_sentences must be either an int or a float. Got: {type(min_sentences)}")
        if isinstance(min_sentences, float):
            if not (0.0 <= min_sentences <= 1.0):
                raise ValueError(f"If min_sentences is a float, it must be between 0 and 1. Got: {min_sentences}")
        elif isinstance(min_sentences, int):
            if min_sentences < 0:
                raise ValueError(f"If min_sentences is an int, it must be non-negative. Got: {min_sentences}")

    def apply(self, text: Text, min_sentences: Union[float, int], **params: Any) -> Text:
        return F.delete_sentences(text, self.deletion_prob, min_sentences)

    @property
    def targets_as_params(self) -> List[str]:
        return ["text"]

    def get_params_dependent_on_targets(self, params: Dict[str, Text]) -> Dict[str, Union[float, int]]:
        if isinstance(self.min_sentences, int):
            return {"min_sentences": self.min_sentences - self.ignore_first}

        # When `min_sentences` is a float and `ignore_first` is True,
        # the proportion of sentences to retain in the text after deletion is grater than `min_sentences`
        # So, it is necessary to adjust `min_sentences` before passing it to the function's parameter
        # n: Length of original sentences (>= 2)
        # p: `min_sentences` ([0, 1]) If `ignore_first` is False
        # q: The minimum proportion of sentences to retain in the text after deletion if `ignore_first` is True
        # If `ignore_first` is False: p == q
        # If `ignore_first` is True: See below
        # If not `ignore_first`: The minimum number of sentences after deleting is n * p
        # If `ignore_first`: The minimum number of sentences after deleting is 1 + (n - 1)*q
        # Therefore, n * p == 1 + (n - 1)*q, ===> q = (n*p - 1) / (n - 1)
        text = params["text"]
        num_original_sentences = len(split_text_into_sentences(text)) + self.ignore_first
        if num_original_sentences < 2:
            return {"min_sentences": self.min_sentences}
        return {
            "min_sentences": (num_original_sentences * self.min_sentences - self.ignore_first)
            / (num_original_sentences - self.ignore_first)
        }

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return ("deletion_prob", "min_sentences")


class RandomInsertion(TextTransform):
    """Repeats n times the task of randomly inserting synonyms into the input text.

    Args:
        insertion_prob: The probability of inserting a synonym.
        n_times: The number of times to repeat the process.
        p: The probability of applying this transform.

    References:
        https://arxiv.org/pdf/1901.11196.pdf
    """

    def __init__(
        self,
        insertion_prob: float = 0.2,
        n_times: int = 1,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(insertion_prob=insertion_prob, n_times=n_times)
        self.insertion_prob = insertion_prob
        self.n_times = n_times

    def _validate_transform_init_args(self, *, insertion_prob: float, n_times: int) -> None:
        if not isinstance(insertion_prob, (float, int)):
            raise TypeError(f"insertion_prob must be a real number between 0 and 1. Got: {type(insertion_prob)}")
        if not (0.0 <= insertion_prob <= 1.0):
            raise ValueError(f"insertion_prob must be between 0 and 1. Got: {insertion_prob}")
        if not isinstance(n_times, int):
            raise TypeError(f"n_times must be a positive integer. Got: {type(n_times)}")
        if n_times <= 0:
            raise ValueError(f"n_times must be positive. Got: {n_times}")

    def apply(self, text: Text, **params: Any) -> Text:
        return F.insert_synonyms(text, self.insertion_prob, self.n_times)

    def get_transform_init_args_names(self) -> Tuple[str, str]:
        return ("insertion_prob", "n_times")


class RandomSwap(TextTransform):
    """Repeats n times the task of randomly swapping two words in a randomly selected sentence from the input text.

    Args:
        n_times: The number of times to repeat the process.
        p: The probability of applying this transform.

    References:
        https://arxiv.org/pdf/1901.11196.pdf
    """

    def __init__(
        self,
        n_times: int = 1,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(n_times=n_times)
        self.n_times = n_times

    def _validate_transform_init_args(self, *, n_times: int) -> None:
        if not isinstance(n_times, int):
            raise TypeError(f"n_times must be a positive integer. Got: {type(n_times)}")
        if n_times <= 0:
            raise ValueError(f"n_times must be positive. Got: {n_times}")

    def apply(self, text: Text, **params: Any) -> Text:
        return F.swap_words(text, self.n_times)

    def get_transform_init_args_names(self) -> Tuple[str]:
        return ("n_times",)


class RandomSwapSentence(TextTransform):
    """Repeats n times the task of randomly swapping two sentences in the input text.

    Args:
        n_times: The number of times to repeat the process.
        p: The probability of applying this transform.
    """

    def __init__(
        self,
        n_times: int = 1,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(n_times=n_times)
        self.n_times = n_times

    def _validate_transform_init_args(self, *, n_times: int) -> None:
        if not isinstance(n_times, int):
            raise TypeError(f"n_times must be a positive integer. Got: {type(n_times)}")
        if n_times <= 0:
            raise ValueError(f"n_times must be positive. Got: {n_times}")

    def apply(self, text: Text, **params: Any) -> Text:
        return F.swap_sentences(text, self.n_times)

    def get_transform_init_args_names(self) -> Tuple[str]:
        return ("n_times",)


class SynonymReplacement(TextTransform):
    """Randomly replaces words in the input text with synonyms.

    Args:
        replacement_prob: The probability of replacing a word with a synonym.
        p: The probability of applying this transform.

    References:
        https://arxiv.org/pdf/1901.11196.pdf
    """

    def __init__(
        self,
        replacement_prob: float = 0.2,
        ignore_first: bool = False,
        always_apply: bool = False,
        p: float = 0.5,
    ) -> None:
        super().__init__(ignore_first=ignore_first, always_apply=always_apply, p=p)
        self._validate_transform_init_args(replacement_prob=replacement_prob)
        self.replacement_prob = replacement_prob

    def _validate_transform_init_args(self, *, replacement_prob: float) -> None:
        if not isinstance(replacement_prob, (float, int)):
            raise TypeError(f"replacement_prob must be a real number between 0 and 1. Got: {type(replacement_prob)}")
        if not (0.0 <= replacement_prob <= 1.0):
            raise ValueError(f"replacement_prob must be between 0 and 1. Got: {replacement_prob}")

    def apply(self, text: Text, **params: Any) -> Text:
        return F.replace_synonyms(text, self.replacement_prob)

    def get_transform_init_args_names(self) -> Tuple[str]:
        return ("replacement_prob",)
