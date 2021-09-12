import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';

const theme = createTheme({
  palette: {
    primary: {
      main: "#537fe4",
    },
    secondary: {
      main: green[500],
    },
  },
});


class App extends Component {
  render() {
    return (
    <ThemeProvider theme={theme}>
        <div className="App">
          <Router>
            <Header />
            <Switch>
              <Route path="/" exact component={QuestionView} />
              <Route path="/add" component={FormView} />
              <Route path="/play" component={QuizView} />
              <Route component={QuestionView} />
            </Switch>
          </Router>
        </div>
    </ThemeProvider>
  );

  }
}

export default App;
