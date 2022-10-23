import $ from "jquery";
import { useEffect, useState } from "react";


const QuizView = () => {

	const questionsPerPlay = 5;

	const [quizCategory, setQuizCategory] = useState(null);
	const [previousQuestions, setPreviousQuestions] = useState([]);
	const [showAnswer, setShowAnswer] = useState(false);
	const [categories, setCategories] = useState({});
	const [numCorrect, setNumCorrect] = useState(0);
	const [currentQuestion, setCurrentQuestion] = useState({});
	const [guess, setGuess] = useState('');
	const [forceEnd, setForceEnd] = useState(false);

	useEffect(() =>{
		$.ajax({
			url: `/categories`, //TODO: update request URL
			type: 'GET',
			success: (result) => {

				setCategories(result.categories)

				return;
			},
			error: (error) => {
				alert('Unable to load categories. Please try your request again');
				return;
			},
		});
	}, [])

	useEffect(() => {
		getNextQuestion()
	}, [quizCategory])

	const selectCategory = ({ type, id = 0 }) => {
		setQuizCategory({type, id})
	};

	const handleChange = (event) => {
		if (event.target.name === "guess") setGuess(event.target.value)
	};

	const getNextQuestion = () => {
		const previousQuestions = [...previousQuestions];
		if (currentQuestion.id) {
			previousQuestions.push(currentQuestion.id);
		}

		$.ajax({
			url: '/quizzes', //TODO: update request URL
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				previous_questions: previousQuestions,
				quiz_category: quizCategory,
			}),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {

				setShowAnswer(false);
				setPreviousQuestions(previousQuestions);
				setCurrentQuestion(result.question);
				setGuess("");
				setForceEnd(result.question ? false : true);

				return;
			},
			error: (error) => {
				alert('Unable to load question. Please try your request again');
				return;
			},
		});
	};

	const submitGuess = (event) => {

		event.preventDefault();
		let evaluate = evaluateAnswer();
		setNumCorrect(!evaluate ? numCorrect : numCorrect + 1)
		setShowAnswer(true);
	};

	const restartGame = () => {

		setQuizCategory(null);
		setPreviousQuestions([]);
		setShowAnswer(false);
		setNumCorrect(0);
		setCurrentQuestion({});
		setGuess("");
		setForceEnd(false);
	};

	const renderPrePlay = () => {
		return (
			<div className = 'quiz-play-holder'>
				<div className = 'choose-header'>Choose Category</div>
				<div className = 'category-holder'>
					<div className = 'play-category' onClick = {selectCategory}>
						ALL
					</div>
					{Object.keys(categories).map((id) => {
						return (
							<div
								key = {id}
								value = {id}
								className = 'play-category'
								onClick = {() =>
									selectCategory({ type: categories[id], id })
								}
							>
								{categories[id]}
							</div>
						);
					})}
				</div>
			</div>
		);
	}

	const renderFinalScore = () =>{
		return (
			<div className = 'quiz-play-holder'>
				<div className = 'final-header'>
					Your Final Score is {numCorrect}
				</div>
				<div className = 'play-again button' onClick = {restartGame}>
					Play Again?
				</div>
			</div>
		);
	}

	const evaluateAnswer = () => {
		const formatGuess = guess
			// eslint-disable-next-line
			.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
			.toLowerCase();
		const answerArray = currentQuestion.answer
			.toLowerCase()
			.split(' ');
		return answerArray.every((el) => formatGuess.includes(el));
	};

	const renderCorrectAnswer = () => {
		let evaluate = evaluateAnswer();
		return (
			<div className = 'quiz-play-holder'>
				<div className = 'quiz-question'>
					{currentQuestion.question}
				</div>
				<div className = {`${evaluate ? 'correct' : 'wrong'}`}>
					{evaluate ? 'You were correct!' : 'You were incorrect'}
				</div>
				<div className = 'quiz-answer'>{currentQuestion.answer}</div>
				<div className = 'next-question button' onClick = {getNextQuestion}>
					{' '}
					Next Question{' '}
				</div>
			</div>
		);
	}

	const renderPlay = () => {

		return previousQuestions.length === questionsPerPlay ||
		forceEnd ? (
			renderFinalScore()
		) : showAnswer ? (
			renderCorrectAnswer()
		) : (
			<div className = 'quiz-play-holder'>
				<div className = 'quiz-question'>
					{currentQuestion.question}
				</div>
				<form onSubmit = {submitGuess}>
					<input type = 'text' name = 'guess' onChange = {handleChange}/>
					<input
						className = 'submit-guess button'
						type = 'submit'
						value = 'Submit Answer'
					/>
				</form>
			</div>
		);
	}

	if (quizCategory) {
		return (renderPlay)
	} else {
		return (renderPrePlay)
	}
}

export default QuizView;
