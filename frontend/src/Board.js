import {is_defined_row_value} from './App'
import Row from './Row'
import React from 'react';

class Board extends React.Component {
  constructor(props){
    super(props);

  }
  render_row(i){
    return(
        <div>
            <Row id = {i}
             handle_render = {this.props.handle_render}
             values = {is_defined_row_value(
                this.props.values, "row".concat(i))} />
        </div>
    );

  }
  render(){
      return (
        <div>
            {this.render_row(0)}
            {this.render_row(1)}
            {this.render_row(2)}
            {this.render_row(3)}
            {this.render_row(4)}
            {this.render_row(5)}
            {this.render_row(6)}
            {this.render_row(7)}
        </div>
      );
  }


}

export default Board;
