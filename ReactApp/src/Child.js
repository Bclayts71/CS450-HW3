import React, { Component } from 'react';

class Child1 extends Component {
  render() {
    return (
      <div>
        <p>{"Name is: " + this.props.name + "Age is: " + this.props.age}</p>
      </div>
    );
  }
}

export default Child1;
