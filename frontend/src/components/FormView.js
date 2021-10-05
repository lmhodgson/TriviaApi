import React, { Component } from 'react';
import $ from 'jquery';
import { FormControl, Input, InputLabel, Select, MenuItem, Button } from '@material-ui/core';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {}
    }
  }

  componentDidMount(){
    $.ajax({
      url: '/categories',
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
            <FormControl>
                <InputLabel name="question-label" htmlFor="inputQuestion">Question</InputLabel>
                <Input id="inputQuestion" type="text" name="question" onChange={this.handleChange}/>
            </FormControl>
            <FormControl>
                <InputLabel name="answer-label" htmlFor="inputAnswer">Answer</InputLabel>
                <Input id="inputAnswer" type="text" name="answer" onChange={this.handleChange}/>
            </FormControl>
            <FormControl>
                <InputLabel id="difficulty-label">Difficulty</InputLabel>
                <Select labelId="difficulty-label" id="selectDifficulty" name="difficulty" onChange={this.handleChange}>
                    <MenuItem value={1}>1</MenuItem>
                    <MenuItem value={2}>2</MenuItem>
                    <MenuItem value={3}>3</MenuItem>
                    <MenuItem value={4}>4</MenuItem>
                    <MenuItem value={5}>5</MenuItem>
                </Select>
            </FormControl>
            <FormControl>
                <InputLabel id="category-label">Category</InputLabel>
                <Select labelId="category-label" id="selectCategory" name="category" onChange={this.handleChange}>
                    {Object.keys(this.state.categories).map(id => {
                        return (
                            <MenuItem value={id} key={id}>{this.state.categories[id]}</MenuItem>
                        )
                    })}
                </Select>
            </FormControl>
            <Button type="submit" variant="contained" size="large" color="primary">Submit</Button>
        </form>
      </div>
    );
  }
}

export default FormView;
