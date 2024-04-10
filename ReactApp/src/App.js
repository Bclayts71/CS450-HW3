import React, { Component } from 'react';
import Child1 from './Child';
import * as d3 from 'd3'
import './App.css'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = { 'count': 0 }
  }
  componentDidMount() {
    var data=[30,40]
    d3.selectAll('circle').attr('r',function(d,i){
      return data[i]
  }).classed("myclass", true)
  }
  componentDidUpdate() {
    console.log("component update")
  }
  render() {
    return (
      <svg x="400" width="1000" height="1000">
        <circle cx="50" cy="50" r="40" />
        <circle cx="150" cy="50" r="40" />
      </svg>
    );
  }
}

export default App;