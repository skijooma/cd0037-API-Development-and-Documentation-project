import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import './stylesheets/App.css';
import FormView from "./components/FormView";
import Header from "./components/Header";
import QuestionView from "./components/QuestionView";
import QuizView from "./components/QuizView";


const App = () => {

	return (
		<div className = "App">
			<Header path/>
			<Router>
				<Routes>
					<Route path = '/' exact element = {<QuestionView />}/>
					<Route path = '/add' element = {<FormView />}/>
					<Route path = '/play' element = {<QuizView />}/>
					<Route element = {<QuestionView />}/>
				</Routes>
			</Router>
		</div>
	)
}

export default App;
