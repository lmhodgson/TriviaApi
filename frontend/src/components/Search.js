import React, { Component } from 'react'
import { FormControl, Input, InputLabel, OutlinedInput, Button } from '@material-ui/core';

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <FormControl>
            <InputLabel name="search-label" htmlFor="inputSearch">Search questions...</InputLabel>
            <Input id="inputSearch" type="text" name="search"
                ref={input => this.search = input}
                onChange={this.handleInputChange}/>
        </FormControl>
        <Button type="submit" variant="contained" size="large" color="primary">Submit</Button>
      </form>
    )
  }
}

export default Search
