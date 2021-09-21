import React, { Component } from 'react';
import '../stylesheets/Question.css';

import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
        <Card variant="outlined">
            <CardContent>
                <img className="category" src={`${category.toLowerCase()}.svg`}/>
                {question}
                <div className="difficulty">Difficulty: {difficulty}</div>
            </CardContent>
            <CardActions>
                <Button variant="contained" size="medium" color="primary" onClick={() => this.flipVisibility()}>
                    {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
                </Button>
                <Button onClick={() => this.props.questionAction('DELETE')}><DeleteIcon /></Button>
            </CardActions>
            <CardContent>
                <div className="answer-holder">
                  <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
                </div>
            </CardContent>
        </Card>
    );
  }
}

export default Question;
