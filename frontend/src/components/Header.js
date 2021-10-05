import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';

import '../stylesheets/Header.css';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  }
}));

export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
          <AppBar position="static" color="primary">
            <Toolbar>
              <Typography variant="h6" className={classes.title}>
                Udacitrivia
              </Typography>
              <ul className="menu-list">
                  <li>
                    <Link to="/"><Button>List</Button></Link>
                    <Link to="/add"><Button>Add</Button></Link>
                    <Link to="/play"><Button>Play</Button></Link>
                  </li>
                </ul>
            </Toolbar>
          </AppBar>
        </div>
  );
}
