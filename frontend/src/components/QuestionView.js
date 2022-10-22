import $ from "jquery";
import React, { useEffect, useState } from "react";
import Question from "./Question";
import Search from "./Search";
import '../stylesheets/App.css';


const QuestionView = () => {

	const [questions, setQuestions] = useState([]);
	const [page, setPage] = useState(1);
	const [totalQuestions, setTotalQuestions] = useState(0);
	const [categories, setCategories] = useState({});
	const [currentCategory, setCurrentCategory] = useState(null);

	useEffect(() => {
		getQuestions();
	},[])

	const getQuestions = () => {

		$.ajax({
			url: `/questions?page=${1}`, //TODO: update request URL
			type: 'GET',
			success: (result) => {
				console.log("GET /questions => ", result)
				setQuestions(result.questions)
				setTotalQuestions(result.totalQuestions)
				setCategories(result.categories)
				setCurrentCategory(currentCategory)

				return;
			},
			error: (error) => {
				console.log("GET /questions ERROR => ", error)
				alert('Unable to load questions. Please try your request again');
				return;
			},
		});
	};

	const selectPage = (num) => {
		setPage(num);
		getQuestions();
	}

	const createPagination = () => {

		let pageNumbers = [];
		let maxPage = Math.ceil(totalQuestions / 10);
		for (let i = 1; i <= maxPage; i++) {
			pageNumbers.push(
				<span
					key = {i}
					className = { `page-num ${i === page ? 'active' : ''}`}
					onClick = { () => {
						selectPage(i);
					}}
				>
					{i}
				</span>
			);
		}

		return pageNumbers;
	}


	const getByCategory = (id) => {
		$.ajax({
			url: `/categories/${id}/questions`, //TODO: update request URL
			type: 'GET',
			success: (result) => {

				setQuestions(result.questions);
				setTotalQuestions(result.totalQuestions);
				setCurrentCategory(result.currentCategory);

				return;
			},
			error: (error) => {
				alert('Unable to load questions. Please try your request again');
				return;
			},
		});
	};

	const submitSearch = (searchTerm) => {
		$.ajax({
			url: `/questions`, //TODO: update request URL
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({ searchTerm: searchTerm }),
			xhrFields: {
				withCredentials: true,
			},
			crossDomain: true,
			success: (result) => {

				setQuestions(result.questions);
				setTotalQuestions(result.totalQuestions);
				setCurrentCategory(result.currentCategory);

				return;
			},
			error: (error) => {
				alert('Unable to load questions. Please try your request again');

				return;
			},
		});
	};

	const questionAction = (id) => (action) => {
		if (action === 'DELETE') {
			if (window.confirm('are you sure you want to delete the question?')) {
				$.ajax({
					url: `/questions/${id}`, //TODO: update request URL
					type: 'DELETE',
					success: (result) => {

						getQuestions();
					},
					error: (error) => {
						alert('Unable to load questions. Please try your request again');

						return;
					},
				});
			}
		}
	};

	return (
		<div className = 'question-view'>
			<div className = 'categories-list'>
				<h2
					onClick = {() => {
						getQuestions();
					}}
				>
					Categories
				</h2>
				<ul>
					{Object.keys(categories).map((id) => (
						<li
							key = {id}
							onClick = {() => {
								getByCategory(id);
							}}
						>
							{categories[id]}
							<img
								className = 'category'
								alt = {`${categories[id].toLowerCase()}`}
								src = {`${categories[id].toLowerCase()}.svg`}
							/>
						</li>
					))}
				</ul>
				<Search submitSearch = {submitSearch}/>
			</div>
			<div className = 'questions-list'>
				<h2>Questions</h2>
				{questions.map((q, ind) => (
					<Question
						key = {q.id}
						question = {q.question}
						answer = {q.answer}
						category = {categories[q.category]}
						difficulty = {q.difficulty}
						questionAction = {questionAction(q.id)}
					/>
				))}
				<div className = 'pagination-menu'>{createPagination()}</div>
			</div>
		</div>
	);
}

export default QuestionView;
